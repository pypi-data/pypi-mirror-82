"""Generate magnetic atomic structures."""
from asr.core import command, option, ASRResult


@command('asr.setup.magnetize')
@option('--state', type=str,
        help='Comma separated string of magnetic states to create.')
@option('--name', help='Atomic structure', type=str)
@option('--copy-params', is_flag=True,
        help='Also copy params.json from this dir (if exists).', type=bool)
def main(state: str = 'all', name: str = 'unrelaxed.json',
         copy_params: bool = False) -> ASRResult:
    """Set up folders with magnetic moments.

    This recipe can be used to test different magnetic configurations
    of an atomic structure. The recipe creates new folder using acronyms
    for the magnetic configutions. Supported magnetic configurations at the
    moment:

    * nm/  <- non-magnetic
    * fm/  <- ferro-magnetic
    * afm/ <- anti-ferro-magnetic (only works with exactly two-magnetic atoms
      in the unit cell)

    To test a specific magnetic configution, for example ferromagnetic,
    simply use the --state switch: --state fm.

    Use the 'all' identifier to test all magnetic configuration: --state all
    This is the default option.

    By default this recipe looks for a structure in the current directory named
    'unrelaxed.json'. Use the --name switch to change this name.

    An atomic structure with the correct initial magnetic moments
    named as '--name' is saved in each folder, which can be relaxed
    using the relax recipe.

    If you also want to copy the params.json file in the current directory into
    all newly created directories use the --copy-params switch.

    Examples
    --------
    Set up all known magnetic configurations (assuming existence of 'unrelaxed.json')
    $ asr run setup.magnetize

    Only set up ferromagnetic configuration

    $ asr run "setup.magnetic --state fm"

    Set up multiple specific magnetic configurations

    $ asr run "setup.magnetic --state nm,fm"

    """
    from pathlib import Path
    from ase.io import read, write
    from ase.parallel import world
    from asr.utils import magnetic_atoms
    import numpy as np
    known_states = ['nm', 'fm', 'afm']

    states = state.split(',')

    if 'all' in states:
        assert len(states) == 1, \
            'Cannot combine "all" with other magnetic states.'
        states = known_states

    for state in states:
        msg = f'{state} is not a known state!'
        assert state in known_states, msg

    # Non-magnetic:
    if 'nm' in states:
        atoms = read(name)
        atoms.set_initial_magnetic_moments(None)
        assert not Path('nm').is_dir(), 'nm/ already exists!'
        if world.rank == 0:
            Path('nm').mkdir()
            write(f'nm/{name}', atoms)
            if copy_params:
                p = Path('params.json')
                if p.is_file:
                    Path('nm/params.json').write_text(p.read_text())

    # Ferro-magnetic:
    if 'fm' in states:
        atoms = read(name)
        atoms.set_initial_magnetic_moments([1] * len(atoms))
        assert not Path('fm').is_dir(), 'fm/ already exists!'
        if world.rank == 0:
            Path('fm').mkdir()
            write(f'fm/{name}', atoms)
            if copy_params:
                p = Path('params.json')
                if p.is_file:
                    Path('fm/params.json').write_text(p.read_text())

    # Antiferro-magnetic:
    if 'afm' in states:
        atoms = read(name)
        magnetic = magnetic_atoms(atoms)
        nmag = sum(magnetic)
        if nmag == 2:
            magmoms = np.zeros(len(atoms))
            a1, a2 = np.where(magnetic)[0]
            magmoms[a1] = 1.0
            magmoms[a2] = -1.0
            atoms.set_initial_magnetic_moments(magmoms)
            assert not Path('afm').is_dir(), 'afm/ already exists!'
            if world.rank == 0:
                Path('afm').mkdir()
                write(f'afm/{name}', atoms)
                if copy_params:
                    p = Path('params.json')
                    if p.is_file:
                        Path('afm/params.json').write_text(p.read_text())
        else:
            print('Warning: Did not produce afm state. '
                  f'The number of magnetic atoms is {nmag}. '
                  'At the moment, I only know how to do AFM '
                  'state for 2 magnetic atoms.')


if __name__ == '__main__':
    main.cli()
