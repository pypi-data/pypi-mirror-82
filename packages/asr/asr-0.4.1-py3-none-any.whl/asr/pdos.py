"""Projected density of states."""
from asr.core import command, option, read_json, ASRResult, prepare_result
from collections import defaultdict
import typing

import numpy as np
from ase import Atoms

from asr.utils import magnetic_atoms


# Recipe tests:

params = "{'mode':{'ecut':200,...},'kpts':{'density':2.0},...}"
ctests = []
ctests.append({'description': 'Test the refined ground state of Si',
               'name': 'test_asr.pdos_Si_gpw',
               'tags': ['gitlab-ci'],
               'cli': ['asr run "setup.materials -s Si2"',
                       'ase convert materials.json structure.json',
                       'asr run "setup.params '
                       f'asr.gs@calculate:calculator {params} '
                       'asr.pdos@calculate:kptdensity 3.0 '
                       'asr.pdos@calculate:emptybands 5"',
                       'asr run gs',
                       'asr run pdos@calculate',
                       'asr run database.fromtree',
                       'asr run "database.browser --only-figures"']})

tests = []
tests.append({'description': 'Test the pdos of Si (cores=1)',
              'name': 'test_asr.pdos_Si_serial',
              'cli': ['asr run "setup.materials -s Si2"',
                      'ase convert materials.json structure.json',
                      'asr run "setup.params '
                      f'asr.gs@calculate:calculator {params} '
                      'asr.pdos@calculate:kptdensity 3.0 '
                      'asr.pdos@calculate:emptybands 5"',
                      'asr run gs',
                      'asr run pdos',
                      'asr run database.fromtree',
                      'asr run "database.browser --only-figures"']})
tests.append({'description': 'Test the pdos of Si (cores=2)',
              'name': 'test_asr.pdos_Si_parallel',
              'cli': ['asr run "setup.materials -s Si2"',
                      'ase convert materials.json structure.json',
                      'asr run "setup.params '
                      f'asr.gs@calculate:calculator {params} '
                      'asr.pdos@calculate:kptdensity 3.0 '
                      'asr.pdos@calculate:emptybands 5"',
                      'asr run gs',
                      'asr run -p 2 pdos',
                      'asr run database.fromtree',
                      'asr run "database.browser --only-figures"']})


# ---------- Webpanel ---------- #


def webpanel(result, row, key_descriptions):
    from asr.database.browser import fig
    # PDOS without spin-orbit coupling
    panel = {'title': 'Projected band structure and DOS (PBE)',
             'columns': [[],
                         [fig('pbe-pdos_nosoc.png', link='empty')]],
             'plot_descriptions': [{'function': plot_pdos_nosoc,
                                    'filenames': ['pbe-pdos_nosoc.png']}],
             'sort': 13}

    return [panel]


# ---------- Main functionality ---------- #


# ----- Slow steps ----- #


@command(module='asr.pdos',
         creates=['pdos.gpw'],
         tests=ctests,
         requires=['gs.gpw'],
         dependencies=['asr.gs'])
@option('-k', '--kptdensity', type=float, help='K-point density')
@option('--emptybands', type=int, help='number of empty bands to include')
def calculate(kptdensity: float = 20.0, emptybands: int = 20) -> ASRResult:
    from asr.utils.refinegs import refinegs
    refinegs(selfc=False,
             kptdensity=kptdensity, emptybands=emptybands,
             gpw='pdos.gpw', txt='pdos.txt')


# ----- Fast steps ----- #


@prepare_result
class Result(ASRResult):

    pdos_nosoc: typing.List[float]
    pdos_soc: typing.List[float]
    dos_at_ef_nosoc: float
    dos_at_ef_soc: float

    key_descriptions = {
        "pdos_nosoc": "Projected density of states w/o soc.",
        "pdos_soc": "Projected density of states",
        "dos_at_ef_nosoc":
        "Density of states at the Fermi "
        "level w/o soc [states/(eV * unit cell)]",
        "dos_at_ef_soc":
        "Density of states at the Fermi level [states/(eV * unit cell)]",
    }
    formats = {"ase_webpanel": webpanel}


@command(module='asr.pdos',
         requires=['results-asr.gs.json', 'pdos.gpw'],
         tests=tests,
         dependencies=['asr.gs', 'asr.pdos@calculate'],
         returns=Result)
def main() -> Result:
    from gpaw import GPAW
    from asr.core import singleprec_dict
    from ase.parallel import parprint
    from asr.magnetic_anisotropy import get_spin_axis

    # Get refined ground state with more k-points
    calc = GPAW('pdos.gpw')

    dos1 = calc.dos(shift_fermi_level=False)
    theta, phi = get_spin_axis()
    dos2 = calc.dos(soc=True, theta=theta, phi=phi, shift_fermi_level=False)

    results = {}

    # Calculate the dos at the Fermi energy
    parprint('\nComputing dos at Ef', flush=True)
    results['dos_at_ef_nosoc'] = dos1.raw_dos([dos1.fermi_level],
                                              width=0.0)[0]
    parprint('\nComputing dos at Ef with spin-orbit coupling', flush=True)
    results['dos_at_ef_soc'] = dos2.raw_dos([dos2.fermi_level],
                                            width=0.0)[0]

    # Calculate pdos
    parprint('\nComputing pdos', flush=True)
    results['pdos_nosoc'] = singleprec_dict(pdos(dos1, calc))
    parprint('\nComputing pdos with spin-orbit coupling', flush=True)
    results['pdos_soc'] = singleprec_dict(pdos(dos2, calc))

    return results


# ---------- Recipe methodology ---------- #


# ----- PDOS ----- #


def pdos(dos, calc):
    """Do a single pdos calculation.

    Main functionality to do a single pdos calculation.
    """
    # Do calculation
    e_e, pdos_syl, symbols, ef = calculate_pdos(dos, calc)

    return {'pdos_syl': pdos_syl, 'symbols': symbols,
            'energies': e_e, 'efermi': ef}


def calculate_pdos(dos, calc):
    """Calculate the projected density of states.

    Returns
    -------
    energies : nd.array
        energies 10 eV under and above Fermi energy
    pdos_syl : defaultdict
        pdos for spin, symbol and orbital angular momentum
    symbols : list
        chemical symbols in Atoms object
    efermi : float
        Fermi energy

    """
    import gpaw.mpi as mpi
    from gpaw.utilities.progressbar import ProgressBar
    from ase.utils import DevNull

    zs = calc.atoms.get_atomic_numbers()
    chem_symbols = calc.atoms.get_chemical_symbols()
    efermi = calc.get_fermi_level()
    l_a = get_l_a(zs)

    ns = calc.get_number_of_spins()
    gaps = read_json('results-asr.gs.json').get('gaps_nosoc')
    e1 = gaps.get('vbm') or gaps.get('efermi')
    e2 = gaps.get('cbm') or gaps.get('efermi')
    e_e = np.linspace(e1 - 3, e2 + 3, 500)

    # We distinguish in (spin(s), chemical symbol(y), angular momentum (l)),
    # that is if there are multiple atoms in the unit cell of the same chemical
    # species, their pdos are added together.
    pdos_syl = defaultdict(float)
    s_i = [s for s in range(ns) for a in l_a for l in l_a[a]]
    a_i = [a for s in range(ns) for a in l_a for l in l_a[a]]
    l_i = [l for s in range(ns) for a in l_a for l in l_a[a]]
    sal_i = [(s, a, l) for (s, a, l) in zip(s_i, a_i, l_i)]

    # Set up progressbar
    if mpi.world.rank == 0:
        pb = ProgressBar()
    else:
        devnull = DevNull()
        pb = ProgressBar(devnull)

    for _, (spin, a, l) in pb.enumerate(sal_i):
        symbol = chem_symbols[a]

        p = dos.raw_pdos(e_e, a, 'spdfg'.index(l), None, spin, 0.0)

        # Store in dictionary
        key = ','.join([str(spin), str(symbol), str(l)])
        pdos_syl[key] += p

    return e_e, pdos_syl, calc.atoms.get_chemical_symbols(), efermi


def get_l_a(zs):
    """Define which atoms and angular momentum to project onto.

    Parameters
    ----------
    zs : [z1, z2, ...]-list or array
        list of atomic numbers (zi: int)

    Returns
    -------
    l_a : {int: str, ...}-dict
        keys are atomic indices and values are a string such as 'spd'
        that determines which angular momentum to project onto or a
        given atom

    """
    lantha = range(58, 72)
    acti = range(90, 104)

    zs = np.asarray(zs)
    l_a = {}
    atoms = Atoms(numbers=zs)
    mag_elements = magnetic_atoms(atoms)
    for a, (z, mag) in enumerate(zip(zs, mag_elements)):
        if z in lantha or z in acti:
            l_a[a] = 'spdf'
        else:
            l_a[a] = 'spd' if mag else 'sp'
    return l_a


# ---------- Plotting ---------- #


def get_ordered_syl_dict(dct_syl, symbols):
    """Order a dictionary with syl keys.

    Parameters
    ----------
    dct_syl : dict
        Dictionary with keys f'{s},{y},{l}'
        (spin (s), chemical symbol (y), angular momentum (l))
    symbols : list
        Sort symbols after index in this list

    Returns
    -------
    outdct_syl : OrderedDict
        Sorted dct_syl

    """
    from collections import OrderedDict

    # Setup ssili (spin, symbol index, angular momentum index) key
    def ssili(syl):
        s, y, L = syl.split(',')
        # Symbols list can have multiple entries of the same symbol
        # ex. ['O', 'Fe', 'O']. In this case 'O' will have index 0 and
        # 'Fe' will have index 1.
        si = symbols.index(y)
        li = ['s', 'p', 'd', 'f'].index(L)
        return f'{s}{si}{li}'

    return OrderedDict(sorted(dct_syl.items(), key=lambda t: ssili(t[0])))


def get_yl_colors(dct_syl):
    """Get the color indices corresponding to each symbol and angular momentum.

    Parameters
    ----------
    dct_syl : OrderedDict
        Ordered dictionary with keys f'{s},{y},{l}'
        (spin (s), chemical symbol (y), angular momentum (l))

    Returns
    -------
    color_yl : OrderedDict
        Color strings for each symbol and angular momentum

    """
    from collections import OrderedDict

    color_yl = OrderedDict()
    c = 0
    for key in dct_syl:
        # Do not differentiate spin by color
        if int(key[0]) == 0:  # if spin is 0
            color_yl[key[2:]] = 'C{}'.format(c)
            c += 1
            c = c % 10  # only 10 colors available in cycler

    return color_yl


def plot_pdos_nosoc(*args, **kwargs):
    return plot_pdos(*args, soc=False, **kwargs)


def plot_pdos_soc(*args, **kwargs):
    return plot_pdos(*args, soc=True, **kwargs)


def plot_pdos(row, filename, soc=True,
              figsize=(5.5, 5), lw=1):

    def smooth(y, npts=3):
        return np.convolve(y, np.ones(npts) / npts, mode='same')

    # Check if pdos data is stored in row
    results = 'results-asr.pdos.json'
    pdos = 'pdos_soc' if soc else 'pdos_nosoc'
    if results in row.data and pdos in row.data[results]:
        data = row.data[results][pdos]
    else:
        return

    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    import matplotlib.patheffects as path_effects

    # Extract raw data
    symbols = data['symbols']
    pdos_syl = get_ordered_syl_dict(data['pdos_syl'], symbols)
    e_e = data['energies'].copy() - row.get('evac', 0)
    ef = data['efermi']

    # Find energy range to plot in
    if soc:
        emin = row.get('vbm', ef) - 3 - row.get('evac', 0)
        emax = row.get('cbm', ef) + 3 - row.get('evac', 0)
    else:
        nosoc_data = row.data['results-asr.gs.json']['gaps_nosoc']
        vbmnosoc = nosoc_data.get('vbm', ef)
        cbmnosoc = nosoc_data.get('cbm', ef)

        if vbmnosoc is None:
            vbmnosoc = ef

        if cbmnosoc is None:
            cbmnosoc = ef

        emin = vbmnosoc - 3 - row.get('evac', 0)
        emax = cbmnosoc + 3 - row.get('evac', 0)

    # Set up energy range to plot in
    i1, i2 = abs(e_e - emin).argmin(), abs(e_e - emax).argmin()

    # Get color code
    color_yl = get_yl_colors(pdos_syl)

    # Figure out if pdos has been calculated for more than one spin channel
    spinpol = False
    for k in pdos_syl.keys():
        if int(k[0]) == 1:
            spinpol = True
            break

    # Set up plot
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # Plot pdos
    pdosint_s = defaultdict(float)
    for key in pdos_syl:
        pdos = pdos_syl[key]
        spin, symbol, lstr = key.split(',')
        spin = int(spin)
        sign = 1 if spin == 0 else -1

        # Integrate pdos to find suiting pdos range
        pdosint_s[spin] += np.trapz(y=pdos[i1:i2], x=e_e[i1:i2])

        # Label atomic symbol and angular momentum
        if spin == 0:
            label = '{} ({})'.format(symbol, lstr)
        else:
            label = None

        ax.plot(smooth(pdos) * sign, e_e,
                label=label, color=color_yl[key[2:]])

    ax.axhline(ef - row.get('evac', 0), color='k', ls=':')

    # Set up axis limits
    ax.set_ylim(emin, emax)
    if spinpol:  # Use symmetric limits
        xmax = max(pdosint_s.values())
        ax.set_xlim(-xmax * 0.5, xmax * 0.5)
    else:
        ax.set_xlim(0, pdosint_s[0] * 0.5)

    # Annotate E_F
    xlim = ax.get_xlim()
    x0 = xlim[0] + (xlim[1] - xlim[0]) * 0.01
    text = plt.text(x0, ef - row.get('evac', 0),
                    r'$E_\mathrm{F}$',
                    fontsize=rcParams['font.size'] * 1.25,
                    ha='left',
                    va='bottom')

    text.set_path_effects([
        path_effects.Stroke(linewidth=3, foreground='white', alpha=0.5),
        path_effects.Normal()
    ])

    ax.set_xlabel('projected dos [states / eV]')
    if row.get('evac') is not None:
        ax.set_ylabel(r'$E-E_\mathrm{vac}$ [eV]')
    else:
        ax.set_ylabel(r'$E$ [eV]')

    # Set up legend
    plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.), loc='lower left',
               ncol=3, mode="expand", borderaxespad=0.)

    plt.savefig(filename, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main.cli()
