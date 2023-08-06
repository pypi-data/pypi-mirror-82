"""Bethe Salpeter absorption spectrum."""
from asr.core import command, option, file_barrier, ASRResult, prepare_result
from click import Choice
import typing


def get_kpts_size(atoms, kptdensity):
    """Try to get a reasonable monkhorst size which hits high symmetry points."""
    from gpaw.kpt_descriptor import kpts2sizeandoffsets as k2so
    size, offset = k2so(atoms=atoms, density=kptdensity)
    size[2] = 1
    for i in range(2):
        if size[i] % 6 != 0:
            size[i] = 6 * (size[i] // 6 + 1)
    kpts = {'size': size, 'gamma': True}
    return kpts


@command(creates=['bse_polx.csv', 'bse_eigx.dat',
                  'bse_poly.csv', 'bse_eigy.dat',
                  'bse_polz.csv', 'bse_eigz.dat'],
         requires=['gs.gpw'],
         dependencies=['asr.gs@calculate'],
         resources='480:20h')
@option('--gs', help='Ground state on which BSE is based', type=str)
@option('--kptdensity', help='K-point density', type=float)
@option('--ecut', help='Plane wave cutoff', type=float)
@option('--nv_s', help='Valence bands included', type=float)
@option('--nc_s', help='Conduction bands included', type=float)
@option('--mode', help='Irreducible response',
        type=Choice(['RPA', 'BSE', 'TDHF']))
@option('--bandfactor', type=int,
        help='Number of unoccupied bands = (#occ. bands) * bandfactor)')
def calculate(gs: str = 'gs.gpw', kptdensity: float = 6.0, ecut: float = 50.0,
              mode: str = 'BSE', bandfactor: int = 6,
              nv_s: float = -2.3, nc_s: float = 2.3) -> ASRResult:
    """Calculate BSE polarizability."""
    import os
    from ase.io import read
    from ase.dft.bandgap import bandgap
    from gpaw import GPAW
    from gpaw.mpi import world
    from gpaw.response.bse import BSE
    from gpaw.occupations import FermiDirac
    from pathlib import Path
    import numpy as np

    atoms = read('structure.json')
    pbc = atoms.pbc.tolist()
    ND = np.sum(pbc)
    if ND == 3:
        eta = 0.1
        kpts = {'density': kptdensity, 'gamma': True, 'even': True}
        truncation = None
    elif ND == 2:
        eta = 0.05
        kpts = get_kpts_size(atoms=atoms, kptdensity=20)
        truncation = '2D'

    else:
        raise NotImplementedError(
            'asr for BSE not implemented for 0D and 1D structures')

    calc_gs = GPAW(gs, txt=None)
    spin = calc_gs.get_spin_polarized()
    nval = calc_gs.wfs.nvalence
    nocc = int(nval / 2)
    nbands = bandfactor * nocc
    Nk = len(calc_gs.get_ibz_k_points())
    gap, v, c = bandgap(calc_gs, direct=True, output=None)

    if isinstance(nv_s, float):
        ev = calc_gs.get_eigenvalues(kpt=v[1], spin=v[0])[v[2]]
        nv_sk = np.zeros((spin + 1, Nk), int)
        for s in range(spin + 1):
            for k in range(Nk):
                e_n = calc_gs.get_eigenvalues(kpt=k, spin=s)
                e_n -= ev
                x = e_n[np.where(e_n < 0)]
                x = x[np.where(x > nv_s)]
                nv_sk[s, k] = len(x)
        nv_s = np.max(nv_sk, axis=1)
    if isinstance(nc_s, float):
        ec = calc_gs.get_eigenvalues(kpt=c[1], spin=c[0])[c[2]]
        nc_sk = np.zeros((spin + 1, Nk), int)
        for s in range(spin + 1):
            for k in range(Nk):
                e_n = calc_gs.get_eigenvalues(kpt=k, spin=s)
                e_n -= ec
                x = e_n[np.where(e_n > 0)]
                x = x[np.where(x < nc_s)]
                nc_sk[s, k] = len(x)
        nc_s = np.max(nc_sk, axis=1)

    nv_s = [np.max(nv_s), np.max(nv_s)]
    nc_s = [np.max(nc_s), np.max(nc_s)]
    print('nv_s, nc_s', nv_s, nc_s)
    valence_bands = []
    conduction_bands = []
    for s in range(spin + 1):
        gap, v, c = bandgap(calc_gs, direct=True, spin=s, output=None)
        valence_bands.append(range(c[2] - nv_s[s], c[2]))
        conduction_bands.append(range(c[2], c[2] + nc_s[s]))

    print(valence_bands)
    print(conduction_bands)

    if not Path('gs_bse.gpw').is_file():
        calc = GPAW(
            gs,
            txt='gs_bse.txt',
            fixdensity=True,
            nbands=int(nbands * 1.5),
            convergence={'bands': nbands},
            occupations=FermiDirac(width=1e-4),
            kpts=kpts)
        calc.get_potential_energy()
        with file_barrier(['gs_bse.gpw']):
            calc.write('gs_bse.gpw', mode='all')

    # if spin:
    #     f0 = calc.get_occupation_numbers(spin=0)
    #     f1 = calc.get_occupation_numbers(spin=1)
    #     n0 = np.where(f0 < 1.0e-6)[0][0]
    #     n1 = np.where(f1 < 1.0e-6)[0][0]
    #     valence_bands = [range(n0 - nv, n0), range(n1 - nv, n1)]
    #     conduction_bands = [range(n0, n0 + nc), range(n1, n1 + nc)]
    # else:
    #     valence_bands = range(nocc - nv, nocc)
    #     conduction_bands = range(nocc, nocc + nc)

    world.barrier()

    bse = BSE('gs_bse.gpw',
              spinors=True,
              ecut=ecut,
              valence_bands=valence_bands,
              conduction_bands=conduction_bands,
              nbands=nbands,
              mode=mode,
              truncation=truncation,
              txt='bse.txt')

    w_w = np.linspace(-2.0, 8.0, 10001)

    w_w, alphax_w = bse.get_polarizability(eta=eta,
                                           filename='bse_polx.csv',
                                           direction=0,
                                           write_eig='bse_eigx.dat',
                                           pbc=pbc,
                                           w_w=w_w)

    w_w, alphay_w = bse.get_polarizability(eta=eta,
                                           filename='bse_poly.csv',
                                           direction=1,
                                           write_eig='bse_eigy.dat',
                                           pbc=pbc,
                                           w_w=w_w)

    w_w, alphaz_w = bse.get_polarizability(eta=eta,
                                           filename='bse_polz.csv',
                                           direction=2,
                                           write_eig='bse_eigz.dat',
                                           pbc=pbc,
                                           w_w=w_w)
    if world.rank == 0:
        os.system('rm gs_bse.gpw')
        os.system('rm gs_nosym.gpw')


def absorption(row, filename, direction='x'):
    import numpy as np
    import matplotlib.pyplot as plt
    from ase.units import alpha, Ha, Bohr

    atoms = row.toatoms()
    pbc = atoms.pbc.tolist()
    dim = np.sum(pbc)

    magstate = row.magstate

    gap_dir = row.gap_dir
    gap_dir_nosoc = row.gap_dir_nosoc

    for method in ['_gw', '_hse', '_gllbsc', '']:
        gapkey = f'gap_dir{method}'
        if gapkey in row:
            gap_dir_x = row.get(gapkey)
            delta_bse = gap_dir_x - gap_dir
            delta_rpa = gap_dir_x - gap_dir_nosoc
            break

    qp_gap = gap_dir + delta_bse

    if magstate != 'NM':
        qp_gap = gap_dir_nosoc + delta_rpa
        delta_bse = delta_rpa

    ax = plt.figure().add_subplot(111)

    data = row.data['results-asr.bse.json'][f'bse_alpha{direction}_w']
    wbse_w = data[:, 0] + delta_bse
    absbse_w = 4 * np.pi * data[:, 2]
    if dim == 2:
        absbse_w *= wbse_w * alpha / Ha / Bohr * 100
    ax.plot(wbse_w, absbse_w, '-', c='0.0', label='BSE')
    xmax = wbse_w[-1]

    # TODO: Sometimes RPA pol doesn't exist, what to do?
    data = row.data.get('results-asr.polarizability.json')
    if data:
        wrpa_w = data['frequencies'] + delta_rpa
        absrpa_w = 4 * np.pi * data[f'alpha{direction}_w'].imag
        if dim == 2:
            absrpa_w *= wrpa_w * alpha / Ha / Bohr * 100
        ax.plot(wrpa_w, absrpa_w, '-', c='C0', label='RPA')
        ymax = max(np.concatenate([absbse_w[wbse_w < xmax],
                                   absrpa_w[wrpa_w < xmax]])) * 1.05
    else:
        ymax = max(absbse_w[wbse_w < xmax]) * 1.05
    ax.plot([qp_gap, qp_gap], [0, ymax], '--', c='0.5',
            label='Direct QP gap')

    ax.set_xlim(0.0, xmax)
    ax.set_ylim(0.0, ymax)
    ax.set_title(f'{direction}-polarization')
    ax.set_xlabel('Energy [eV]')
    if dim == 2:
        ax.set_ylabel('Absorbance [%]')
    else:
        ax.set_ylabel(r'$\varepsilon(\omega)$')
    ax.legend()
    plt.tight_layout()
    plt.savefig(filename)

    return ax


def webpanel(result, row, key_descriptions):
    import numpy as np
    from functools import partial
    from asr.database.browser import fig, table

    E_B = table(row, 'Property', ['E_B'], key_descriptions)

    atoms = row.toatoms()
    pbc = atoms.pbc.tolist()
    dim = np.sum(pbc)

    if dim == 2:
        funcx = partial(absorption, direction='x')
        funcz = partial(absorption, direction='z')

        panel = {'title': 'Optical absorption (BSE and RPA)',
                 'columns': [[fig('absx.png'), E_B],
                             [fig('absz.png')]],
                 'plot_descriptions': [{'function': funcx,
                                        'filenames': ['absx.png']},
                                       {'function': funcz,
                                        'filenames': ['absz.png']}]}
    else:
        funcx = partial(absorption, direction='x')
        funcy = partial(absorption, direction='y')
        funcz = partial(absorption, direction='z')

        panel = {'title': 'Optical absorption (BSE and RPA)',
                 'columns': [[fig('absx.png'), fig('absz.png')],
                             [fig('absy.png'), E_B]],
                 'plot_descriptions': [{'function': funcx,
                                        'filenames': ['absx.png']},
                                       {'function': funcy,
                                        'filenames': ['absy.png']},
                                       {'function': funcz,
                                        'filenames': ['absz.png']}]}
    return [panel]


@prepare_result
class Result(ASRResult):

    E_B: float
    bse_alphax_w: typing.List[float]
    bse_alphay_w: typing.List[float]
    bse_alphaz_w: typing.List[float]

    key_descriptions = {"E_B": "Exciton binding energy from BSE [eV].",
                        'bse_alphax_w': 'BSE polarizability x-direction.',
                        'bse_alphay_w': 'BSE polarizability y-direction.',
                        'bse_alphaz_w': 'BSE polarizability z-direction.'}

    formats = {"ase_webpanel": webpanel}


@command(module='asr.bse',
         requires=['bse_polx.csv', 'results-asr.gs.json'],
         dependencies=['asr.bse@calculate', 'asr.gs'],
         returns=Result)
def main() -> Result:
    import numpy as np
    from pathlib import Path
    from asr.core import read_json

    alphax_w = np.loadtxt('bse_polx.csv', delimiter=',')
    data = {'bse_alphax_w': alphax_w.astype(np.float32)}

    if Path('bse_poly.csv').is_file():
        alphay_w = np.loadtxt('bse_poly.csv', delimiter=',')
        data['bse_alphay_w'] = alphay_w.astype(np.float32)
    if Path('bse_polz.csv').is_file():
        alphaz_w = np.loadtxt('bse_polz.csv', delimiter=',')
        data['bse_alphaz_w'] = alphaz_w.astype(np.float32)

    if Path('bse_eigx.dat').is_file():
        E = np.loadtxt('bse_eigx.dat')[0, 1]

        magstateresults = read_json('results-asr.magstate.json')
        magstate = magstateresults['magstate']

        gsresults = read_json('results-asr.gs.json')
        if magstate == 'NM':
            E_B = gsresults['gap_dir'] - E
        else:
            E_B = gsresults['gap_dir_nosoc'] - E

        data['E_B'] = E_B

    return data


if __name__ == '__main__':
    main.cli()
