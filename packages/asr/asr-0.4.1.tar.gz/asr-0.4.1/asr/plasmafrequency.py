"""Plasma frequency."""
from asr.core import command, option, ASRResult, prepare_result
import typing


def get_kpts_size(atoms, density):
    """Try to get a reasonable monkhorst size which hits high symmetry points."""
    from gpaw.kpt_descriptor import kpts2sizeandoffsets as k2so
    size, offset = k2so(atoms=atoms, density=density)
    size[2] = 1
    for i in range(2):
        if size[i] % 6 != 0:
            size[i] = 6 * (size[i] // 6 + 1)
    kpts = {'size': size, 'gamma': True}
    return kpts


@command('asr.plasmafrequency',
         creates=['es_plasma.gpw'],
         dependencies=['asr.gs@calculate'],
         requires=['gs.gpw'])
@option('--kptdensity', help='k-point density', type=float)
def calculate(kptdensity: float = 20) -> ASRResult:
    """Calculate excited states for polarizability calculation."""
    from gpaw import GPAW
    from ase.parallel import world
    from pathlib import Path

    calc_old = GPAW('gs.gpw', txt=None)
    kpts = get_kpts_size(atoms=calc_old.atoms, density=kptdensity)
    nval = calc_old.wfs.nvalence
    try:
        calc = GPAW('gs.gpw', fixdensity=True, kpts=kpts,
                    nbands=2 * nval, txt='gsplasma.txt')
        calc.get_potential_energy()
        calc.write('es_plasma.gpw', 'all')
    except Exception:
        if world.rank == 0:
            es_file = Path("es_plasma.gpw")
            if es_file.is_file():
                es_file.unlink()
        world.barrier()


def webpanel(result, row, key_descriptions):
    from asr.database.browser import table

    if row.get('gap', 1) > 0.01:
        return []

    plasmatable = table(row, 'Property', [
        'plasmafrequency_x', 'plasmafrequency_y'], key_descriptions)

    panel = {'title': 'Optical polarizability (RPA)',
             'columns': [[], [plasmatable]]}
    return [panel]


@prepare_result
class Result(ASRResult):

    plasmafreq_vv: typing.List[typing.List[float]]
    plasmafrequency_x: float
    plasmafrequency_y: float

    key_descriptions = {
        "plasmafreq_vv": "Plasma frequency tensor [Hartree]",
        "plasmafrequency_x": "KVP: 2D plasma frequency (x)"
        "[`eV/Ang^0.5`]",
        "plasmafrequency_y": "KVP: 2D plasma frequency (y)"
        "[`eV/Ang^0.5`]",
    }
    formats = {"ase_webpanel": webpanel}


@command('asr.plasmafrequency',
         returns=Result,
         dependencies=['asr.plasmafrequency@calculate'])
@option('--tetra', is_flag=True,
        help='Use tetrahedron integration')
def main(tetra: bool = True) -> Result:
    """Calculate polarizability."""
    from gpaw.response.df import DielectricFunction
    from ase.io import read
    import numpy as np
    from ase.units import Hartree, Bohr
    from pathlib import Path
    from ase.parallel import world

    atoms = read('structure.json')
    nd = sum(atoms.pbc)
    if not nd == 2:
        raise AssertionError('Plasmafrequency recipe only implemented for 2D')

    if tetra:
        kwargs = {'truncation': '2D',
                  'eta': 0.05,
                  'domega0': 0.2,
                  'integrationmode': 'tetrahedron integration',
                  'ecut': 1,
                  'pbc': [True, True, False]}
    else:
        kwargs = {'truncation': '2D',
                  'eta': 0.05,
                  'domega0': 0.2,
                  'ecut': 1}

    try:
        df = DielectricFunction('es_plasma.gpw', **kwargs)
        df.get_polarizability(q_c=[0, 0, 0], direction='x',
                              pbc=[True, True, False],
                              filename=None)
    finally:
        world.barrier()
        if world.rank == 0:
            es_file = Path("es_plasma.gpw")
            es_file.unlink()
    plasmafreq_vv = df.chi0.plasmafreq_vv.real
    data = {'plasmafreq_vv': plasmafreq_vv}

    if nd == 2:
        wp2_v = np.linalg.eigvalsh(plasmafreq_vv[:2, :2])
        L = atoms.cell[2, 2] / Bohr
        plasmafreq_v = (np.sqrt(wp2_v * L / 2) * Hartree * Bohr**0.5)
        data['plasmafrequency_x'] = plasmafreq_v[0].real
        data['plasmafrequency_y'] = plasmafreq_v[1].real

    return data


if __name__ == '__main__':
    main.cli()
