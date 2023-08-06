"""Phonon band structure and dynamical stability."""
from pathlib import Path
import typing

import numpy as np

from ase.parallel import world
from ase.io import read
from ase.phonons import Phonons
from ase.dft.kpoints import BandPath

from asr.core import command, option, ASRResult, prepare_result


def creates():
    atoms = read('structure.json')
    natoms = len(atoms)
    filenames = ['phonon.eq.pckl']
    for a in range(natoms):
        for v in 'xyz':
            for pm in '+-':
                # Atomic forces for a displacement of atom a in direction v
                filenames.append(f'phonon.{a}{v}{pm}.pckl')
    return filenames


def todict(filename):
    from ase.utils import pickleload
    with open(filename, 'rb') as fd:
        content = pickleload(fd)
    return {'content': content}


def topckl(filename, dct):
    from ase.utils import opencew
    import pickle
    if Path(filename).is_file():
        return
    contents = dct['content']
    fd = opencew(filename)
    if world.rank == 0:
        pickle.dump(contents, fd, protocol=2)
        fd.close()


@command('asr.phonons',
         requires=['structure.json', 'gs.gpw'],
         dependencies=['asr.gs@calculate'],
         creates=creates)
@option('-n', help='Supercell size', type=int)
@option('--ecut', help='Energy cutoff', type=float)
@option('--kptdensity', help='Kpoint density', type=float)
@option('--fconverge', help='Force convergence criterium', type=float)
def calculate(n: int = 2, ecut: float = 800, kptdensity: float = 6.0,
              fconverge: float = 1e-4) -> ASRResult:
    """Calculate atomic forces used for phonon spectrum."""
    from asr.calculators import get_calculator
    # Remove empty files:
    if world.rank == 0:
        for f in Path().glob('phonon.*.pckl'):
            if f.stat().st_size == 0:
                f.unlink()
    world.barrier()

    atoms = read('structure.json')
    gsold = get_calculator()('gs.gpw', txt=None)

    # Set initial magnetic moments
    from asr.utils import is_magnetic
    if is_magnetic():
        magmoms_m = gsold.get_magnetic_moments()
        # Some calculators return magnetic moments resolved into their
        # cartesian components
        if len(magmoms_m.shape) == 2:
            magmoms_m = np.linalg.norm(magmoms_m, axis=1)
        atoms.set_initial_magnetic_moments(magmoms_m)

    params = gsold.parameters.copy()  # TODO: remove fix density from gs params
    if 'fixdensity' in params:
        params.pop('fixdensity')
    params.update({'mode': {'name': 'pw', 'ecut': ecut},
                   'kpts': {'density': kptdensity, 'gamma': True}})

    # Set essential parameters for phonons
    params['symmetry'] = {'point_group': False}

    # Make sure to converge forces! Can be important
    params['convergence'] = {'forces': fconverge}

    fd = open('phonons.txt'.format(n), 'a')
    params['txt'] = fd
    calc = get_calculator()(**params)

    nd = sum(atoms.get_pbc())
    if nd == 3:
        supercell = (n, n, n)
    elif nd == 2:
        supercell = (n, n, 1)
    elif nd == 1:
        supercell = (n, 1, 1)

    p = Phonons(atoms=atoms, calc=calc, supercell=supercell)
    p.run()

    # Read creates files
    files = {}
    for filename in creates():
        dct = todict(filename)
        dct['__tofile__'] = 'asr.phonons@topckl'
        files[filename] = dct
    data = {'__files__': files}
    fd.close()
    return data


def requires():
    return creates() + ['results-asr.phonons@calculate.json']


def webpanel(result, row, key_descriptions):
    from asr.database.browser import table, fig
    phonontable = table(row, 'Property', ['minhessianeig'], key_descriptions)

    panel = {'title': 'Phonons',
             'columns': [[fig('phonon_bs.png')], [phonontable]],
             'plot_descriptions': [{'function': plot_bandstructure,
                                    'filenames': ['phonon_bs.png']}],
             'sort': 3}

    dynstab = row.get('dynamic_stability_phonons')
    high = 'Min. Hessian eig. > -0.01 meV/Ang^2'
    low = 'Min. Hessian eig. <= -0.01 meV/Ang^2'
    row = ['Dynamical (phonons)',
           '<a href="#" data-toggle="tooltip" data-html="true" '
           + 'title="LOW: {}&#13;HIGH: {}">{}</a>'.format(
               low, high, dynstab.upper())]

    summary = {'title': 'Summary',
               'columns': [[{'type': 'table',
                             'header': ['Stability', 'Category'],
                             'rows': [row]}]],
               'sort': 2}
    return [panel, summary]


@prepare_result
class Result(ASRResult):

    minhessianeig: float
    dynamic_stability_phonons: str
    q_qc: typing.List[typing.Tuple[float, float, float]]
    omega_kl: typing.List[typing.List[float]]
    path: BandPath
    modes_kl: typing.List[typing.List[float]]
    interp_freqs_kl: typing.List[typing.List[float]]

    key_descriptions = {
        "minhessianeig": "KVP: Minimum eigenvalue of Hessian [`eV/Ang^2`]",
        "dynamic_stability_phonons": "Phonon dynamic stability (low/high)",
        "q_qc": "List of momenta consistent with supercell.",
        "omega_kl": "Phonon frequencies.",
        "modes_kl": "Phonon modes.",
        "interp_freqs_kl": "Interpolated phonon frequencies.",
        "path": "Interpolated phonon bandstructure path.",
    }
    formats = {"ase_webpanel": webpanel}


@command('asr.phonons',
         requires=requires,
         returns=Result,
         dependencies=['asr.phonons@calculate'])
@option('--mingo/--no-mingo', is_flag=True,
        help='Perform Mingo correction of force constant matrix')
def main(mingo: bool = True) -> Result:
    from asr.core import read_json
    calculateresult = read_json('results-asr.phonons@calculate.json')
    atoms = read('structure.json')
    n = calculateresult.metadata.params['n']
    nd = sum(atoms.get_pbc())
    if nd == 3:
        supercell = (n, n, n)
    elif nd == 2:
        supercell = (n, n, 1)
    elif nd == 1:
        supercell = (n, 1, 1)
    p = Phonons(atoms=atoms, supercell=supercell)
    p.read(symmetrize=0)

    if mingo:
        # We correct the force constant matrix and
        # dynamical matrix
        C_N = mingocorrection(p.C_N, atoms, supercell)
        p.C_N = C_N

        # Calculate dynamical matrix
        D_N = C_N.copy()
        m_a = atoms.get_masses()
        m_inv_x = np.repeat(m_a**-0.5, 3)
        M_inv = np.outer(m_inv_x, m_inv_x)
        for D in D_N:
            D *= M_inv
            p.D_N = D_N

    # First calculate the exactly known q-points
    q_qc = np.indices(p.N_c).reshape(3, -1).T / p.N_c
    out = p.band_structure(q_qc, modes=True, born=False, verbose=False)
    omega_kl, u_kl = out

    R_cN = p.lattice_vectors()
    eigs = []
    for q_c in q_qc:
        phase_N = np.exp(-2j * np.pi * np.dot(q_c, R_cN))
        C_q = np.sum(phase_N[:, np.newaxis, np.newaxis] * p.C_N, axis=0)
        eigs.append(np.linalg.eigvalsh(C_q))

    eigs = np.array(eigs)
    mineig = np.min(eigs)

    if mineig < -0.01:
        dynamic_stability = 'low'
    else:
        dynamic_stability = 'high'

    results = {'omega_kl': omega_kl,
               'q_qc': q_qc,
               'modes_kl': u_kl,
               'minhessianeig': mineig,
               'dynamic_stability_phonons': dynamic_stability}

    # Next calculate an approximate phonon band structure
    path = atoms.cell.bandpath(npoints=100, pbc=atoms.pbc)
    freqs_kl = p.band_structure(path.kpts, modes=False, born=False,
                                verbose=False)
    results['interp_freqs_kl'] = freqs_kl
    results['path'] = path

    return results


def plot_phonons(row, fname):
    import matplotlib.pyplot as plt

    data = row.data.get('results-asr.phonons.json')
    if data is None:
        return

    omega_kl = data['omega_kl']
    gamma = omega_kl[0]
    fig = plt.figure(figsize=(6.4, 3.9))
    ax = fig.gca()

    x0 = -0.0005  # eV
    for x, color in [(gamma[gamma < x0], 'r'),
                     (gamma[gamma >= x0], 'b')]:
        if len(x) > 0:
            markerline, _, _ = ax.stem(x * 1000, np.ones_like(x), bottom=-1,
                                       markerfmt=color + 'o',
                                       linefmt=color + '-')
            plt.setp(markerline, alpha=0.4)
    ax.set_xlabel(r'phonon frequency at $\Gamma$ [meV]')
    ax.axis(ymin=0.0, ymax=1.3)
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()


def plot_bandstructure(row, fname):
    from matplotlib import pyplot as plt
    from ase.spectrum.band_structure import BandStructure
    data = row.data.get('results-asr.phonons.json')
    path = data['path']
    energies = data['interp_freqs_kl'] * 1e3
    exact_indices = []
    for q_c in data['q_qc']:
        diff_kc = path.kpts - q_c
        diff_kc -= np.round(diff_kc)
        inds = np.argwhere(np.all(np.abs(diff_kc) < 1e-3, 1))
        exact_indices.extend(inds.tolist())

    en_exact = np.zeros_like(energies) + np.nan
    for ind in exact_indices:
        en_exact[ind] = energies[ind]

    bs = BandStructure(path=path, energies=en_exact[None])
    bs.plot(ax=plt.gca(), ls='', marker='o', colors=['C1'],
            emin=np.min(energies * 1.1), emax=np.max([np.max(energies * 1.15),
                                                      0.0001]),
            ylabel='Phonon frequencies [meV]')
    plt.tight_layout()
    plt.savefig(fname)


def mingocorrection(Cin_NVV, atoms, supercell):
    na = len(atoms)
    nc = np.prod(supercell)
    dimension = nc * na * 3

    Cin = (Cin_NVV.reshape(*supercell, na, 3, na, 3).
           transpose(3, 4, 0, 1, 2, 5, 6))

    C = np.empty((*supercell, na, 3, *supercell, na, 3))

    from itertools import product
    for n1, n2, n3 in product(range(supercell[0]),
                              range(supercell[1]),
                              range(supercell[2])):
        inds1 = (np.arange(supercell[0]) - n1) % supercell[0]
        inds2 = (np.arange(supercell[1]) - n2) % supercell[1]
        inds3 = (np.arange(supercell[2]) - n3) % supercell[2]
        C[n1, n2, n3] = Cin[:, :, inds1][:, :, :, inds2][:, :, :, :, inds3]

    C.shape = (dimension, dimension)
    C += C.T.copy()
    C *= 0.5

    # Mingo correction.
    #
    # See:
    #
    #    Phonon transmission through defects in carbon nanotubes
    #    from first principles
    #
    #    N. Mingo, D. A. Stewart, D. A. Broido, and D. Srivastava
    #    Phys. Rev. B 77, 033418 – Published 30 January 2008
    #    http://dx.doi.org/10.1103/PhysRevB.77.033418

    R_in = np.zeros((dimension, 3))
    for n in range(3):
        R_in[n::3, n] = 1.0
    a_in = -np.dot(C, R_in)
    B_inin = np.zeros((dimension, 3, dimension, 3))
    for i in range(dimension):
        B_inin[i, :, i] = np.dot(R_in.T, C[i, :, np.newaxis]**2 * R_in) / 4
        for j in range(dimension):
            B_inin[i, :, j] += np.outer(R_in[i], R_in[j]).T * C[i, j]**2 / 4

    L_in = np.dot(np.linalg.pinv(B_inin.reshape((dimension * 3,
                                                 dimension * 3))),
                  a_in.reshape((dimension * 3,))).reshape((dimension, 3))
    D_ii = C**2 * (np.dot(L_in, R_in.T) + np.dot(L_in, R_in.T).T) / 4
    C += D_ii

    C.shape = (*supercell, na, 3, *supercell, na, 3)
    Cout = C[0, 0, 0].transpose(2, 3, 4, 0, 1, 5, 6).reshape(nc,
                                                             na * 3,
                                                             na * 3)
    return Cout


if __name__ == '__main__':
    main.cli()
