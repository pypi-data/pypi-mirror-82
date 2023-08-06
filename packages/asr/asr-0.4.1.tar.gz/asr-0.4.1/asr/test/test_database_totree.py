import pytest
from .materials import std_test_materials


@pytest.mark.ci
def test_database_totree(asr_tmpdir_w_params):
    from ase.db import connect
    from asr.database.totree import main
    from pathlib import Path

    dbname = 'database.db'
    db = connect(dbname)
    for atoms in std_test_materials:
        db.write(atoms)

    main(database=dbname,
         tree_structure='tree/{stoi}/{spg}/{formula:abc}')

    assert not Path('tree').is_dir()

    main(database=dbname, run=True, atomsfile='structure.json',
         tree_structure='tree/{stoi}/{spg}/{formula:abc}')

    assert Path('tree').is_dir()
    assert Path('tree/A/123/Ag/structure.json').is_file()
    assert Path('tree/A/227/Si2/structure.json').is_file()
    assert Path('tree/AB/187/BN/structure.json').is_file()


@pytest.fixture
def make_test_db(asr_tmpdir):
    """Make a database that contains data in various forms."""
    from .materials import BN
    from pathlib import Path
    from ase.db import connect

    dbname = 'database.db'
    db = connect(dbname)
    p = Path('hardlinkedfile.txt')
    p.write_text('Some content.')

    data = {'file.json': {'key': 'value'},
            'hardlinkedfile.txt': {'pointer': str(p.absolute())}}

    db.write(BN, data=data)
    return db


@pytest.mark.ci
def test_database_totree_files_and_hard_links(make_test_db):
    """Test that hard links are correctly reproduced."""
    from asr.core import read_json
    from asr.database.totree import main
    from pathlib import Path
    import os

    dbname = 'database.db'
    main(database=dbname, run=True, copy=True, atomsfile='structure.json',
         tree_structure='tree/{stoi}/{spg}/{formula:abc}')
    hardlink = Path('tree/AB/187/BN/hardlinkedfile.txt')
    filejson = Path('tree/AB/187/BN/file.json')
    assert Path('tree/AB/187/BN/structure.json').is_file()
    assert filejson.is_file()
    assert hardlink.is_file()

    contents = read_json(filejson)
    assert contents['key'] == 'value'

    # Check that link is not symlink
    assert not os.path.islink(hardlink)
    assert os.stat(hardlink).st_ino == os.stat('hardlinkedfile.txt').st_ino
