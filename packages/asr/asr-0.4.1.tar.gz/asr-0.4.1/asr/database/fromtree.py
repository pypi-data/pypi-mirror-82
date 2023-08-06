"""Convert a folder tree to an ASE database."""

from typing import Union, List
from ase import Atoms
from ase.io import read
from ase.db import connect
from asr.core import command, option, argument, chdir, read_json, ASRResult
from asr.database.key_descriptions import key_descriptions as asr_kd
from asr.database.material_fingerprint import main as mf
from asr.database.material_fingerprint import get_uid_of_atoms, \
    get_hash_of_atoms
from asr.database.check import main as check_database
import multiprocessing
from pathlib import Path
import os
import glob
import sys
import traceback


class MissingUIDS(Exception):
    pass


def parse_key_descriptions(key_descriptions):
    """Parse key descriptions.

    This function parses a dictionary of key descriptions. A valid key
    description looks like::

        `KVP: Long description !short description! [unit]`

    - KVP: marks a key as a key-value-pair.
    - !short description!: gives a short description of the key.
    - [unit]: Marks the unit of the key.
    - The rest of the text will be interpreted as the long description
      of the key.

    """
    import re

    tmpkd = {}

    for key, desc in key_descriptions.items():
        descdict = {'type': None,
                    'iskvp': False,
                    'shortdesc': '',
                    'longdesc': '',
                    'units': ''}
        if isinstance(desc, dict):
            descdict.update(desc)
            tmpkd[key] = desc
            continue

        assert isinstance(desc, str), \
            f'Key description has to be dict or str. ({desc})'
        # Get key type
        desc, *keytype = desc.split('->')
        if keytype:
            descdict['type'] = keytype

        # Is this a kvp?
        iskvp = desc.startswith('KVP:')
        descdict['iskvp'] = iskvp
        desc = desc.replace('KVP:', '').strip()

        # Find units
        m = re.search(r"\[(.*)\]", desc)
        unit = m.group(1) if m else ''
        if unit:
            descdict['units'] = unit
        desc = desc.replace(f'[{unit}]', '').strip()

        # Find short description
        m = re.search(r"\!(.*)\!", desc)
        shortdesc = m.group(1) if m else ''
        if shortdesc:
            descdict['shortdesc'] = shortdesc

        # Everything remaining is the long description
        longdesc = desc.replace(f'!{shortdesc}!', '').strip()
        if longdesc:
            descdict['longdesc'] = longdesc
            if not shortdesc:
                descdict['shortdesc'] = descdict['longdesc']
        tmpkd[key] = descdict

    return tmpkd


tmpkd = parse_key_descriptions(
    {key: value
     for dct in asr_kd.values()
     for key, value in dct.items()})


def get_key_value_pairs(resultsdct: dict):
    """Extract key-value-pairs from results dictionary.

    Note to determine which key in the results dictionary is a
    key-value-pair we parse the data in `asr.database.key_descriptions`.

    Parameters
    ----------
    resultsdct: dict
        Dictionary containing asr results file.

    Returns
    -------
    kvp: dict
        key-value-pairs.
    """
    kvp = {}
    for key, desc in tmpkd.items():
        if (key in resultsdct and desc['iskvp']
           and resultsdct[key] is not None):
            kvp[key] = resultsdct[key]

    return kvp


def collect_file(filename: Path):
    """Collect a single file.

    Parameters
    ----------
    filename: str

    Returns
    -------
    kvp: dict
        Key-value pairs
    data: dict
        Dict with keys=filenames where filenames is the input filename
        and any additional files that were created or required by this recipe.
    links: dict
        Dict with keys

    """
    from asr.core import read_json
    data = {}
    results = read_json(filename)
    if isinstance(results, ASRResult):
        dct = results.format_as('dict')
    else:
        dct = results

    data[str(filename)] = dct

    # Find and try to collect related files for this resultsfile
    files = results.get('__files__', {})
    extra_files = results.get('__requires__', {}).copy()
    extra_files.update(results.get('__creates__', {}))

    for extrafile, checksum in extra_files.items():
        assert extrafile not in data, f'{extrafile} already collected!'

        if extrafile in files:
            continue
        file = Path(extrafile)

        if not file.is_file():
            print(f'Warning: Required file {file.absolute()}'
                  ' doesn\'t exist.')
            continue

        if file.suffix == '.json':
            extra = read_json(extrafile)
            if isinstance(extra, ASRResult):
                dct = extra.format_as('dict')
            else:
                dct = extra
        else:
            dct = {'pointer': str(file.absolute())}

        data[extrafile] = dct

    kvp = get_key_value_pairs(results)
    return kvp, data


def collect_links_to_child_folders(folder: Path, atomsname):
    """Collect links to all subfolders.

    Parameters
    ----------
    folder: Path
        Path to folder.
    atomsname: str
        Name of file containing atoms, i.e. 'structure.json'.

    Returns
    -------
    children: dict
        Dictionary with key=relative path to child material and
        value=uid of child material, i.e.: {'strains':
        'Si2-abcdefghiklmn'}.

    """
    children = {}

    for root, dirs, files in os.walk(folder, topdown=True, followlinks=False):
        this_folder = Path(root).resolve()

        if atomsname in files:
            with chdir(this_folder):
                atoms = read(atomsname, parallel=False)
                uid = get_material_uid(atoms)
                children[root] = uid
    return children


def get_material_uid(atoms: Atoms):
    """Get UID of atoms."""
    if not mf.done:
        try:
            mf()
        except PermissionError:
            pass
    try:
        return read_json(
            'results-asr.database.material_fingerprint.json')['uid']
    except FileNotFoundError:
        # FileNotFoundError happens some times on Gitlab CI
        # and I have not been able to reproduce it on any of
        # my own devices. The problem started when we started
        # to use multiprocessing so I suspect that it is somehow
        # related to that. Somehow, writing and IMMEDIATELY reading
        # a file gives problems on gitlab CI.
        hash = get_hash_of_atoms(atoms)
        return get_uid_of_atoms(atoms, hash)


def collect_folder(folder: Path, atomsname: str, patterns: List[str],
                   children_patterns=[]):
    """Collect data from a material folder.

    Parameters
    ----------
    folder: Path
        Path to folder.
    atomsname: str
        Name of file containing atoms, i.e. 'structure.json'.
    patterns: List[str]
        List of patterns marking which files to include.

    Returns
    -------
    atoms: Atoms
        Atomic structure.
    kvp: dict
        Key-value-pairs.
    data: dict
        Dictionary containing data files and links.

    """
    from fnmatch import fnmatch

    with chdir(folder.resolve()):
        if not Path(atomsname).is_file():
            return None, None, None

        atoms = read(atomsname, parallel=False)

        uid = get_material_uid(atoms)
        kvp = {'folder': str(folder),
               'uid': uid}
        data = {'__children__': {}}
        data[atomsname] = read_json(atomsname)
        for name in Path().glob('*'):
            if name.is_dir() and any(fnmatch(name, pattern)
                                     for pattern in children_patterns):
                children = collect_links_to_child_folders(name, atomsname)
                data['__children__'].update(children)
            elif name.is_file() and any(fnmatch(name, pattern) for pattern in patterns):
                tmpkvp, tmpdata = collect_file(name)
                kvp.update(tmpkvp)
                data.update(tmpdata)

        if not data['__children__']:
            del data['__children__']

    return atoms, kvp, data


def make_data_identifiers(filenames: List[str]):
    """Make key-value-pairs for identifying data files.

    This function looks at the keys of `data` and identifies any
    result files. If a result file has been identified a key value
    pair with name has_asr_name=True will be returned. I.e. if
    results-asr.gs@calculate.json is in `data` a key-value-pair with
    name `has_asr_gs_calculate=True` will be generated

    Parameters
    ----------
    filenames: List[str]
        List of file names.

    Returns
    -------
    dict
        Dict containing identifying key-value-pairs,
        i.e. {'has_asr_gs_calculate': True}.
    """
    kvp = {}
    for key in filter(lambda x: x.startswith('results-'), filenames):
        recipe = key[8:-5].replace('.', '_').replace('@', '_')
        name = f'has_{recipe}'
        kvp[name] = True
    return kvp


def recurse_through_folders(folder, atomsname):
    """Find all folders from folder that contain atomsname."""
    folders = []
    for root, dirs, files in os.walk(folder, topdown=True, followlinks=False):
        if atomsname in files:
            folders.append(root)
    return folders


def _collect_folders(folders: List[str],
                     atomsname: str = None,
                     patterns: List[str] = None,
                     children_patterns: List[str] = None,
                     dbname: str = None,
                     jobid: int = None):
    """Collect `myfolders` to `mydbname`."""
    nfolders = len(folders)
    with connect(dbname, serial=True) as db:
        for ifol, folder in enumerate(folders):
            string = f'Collecting folder {folder} ({ifol + 1}/{nfolders})'
            if jobid is not None:
                print(f'Subprocess #{jobid} {string}', flush=True)
            else:
                print(string)

            atoms, key_value_pairs, data = collect_folder(
                Path(folder),
                atomsname,
                patterns,
                children_patterns=children_patterns)

            if atoms is None:
                continue

            identifier_kvp = make_data_identifiers(data.keys())
            key_value_pairs.update(identifier_kvp)
            try:
                db.write(atoms, data=data, **key_value_pairs)
            except Exception:
                print(f'folder={folder}')
                print(f'atoms={atoms}')
                print(f'data={data}')
                print(f'kvp={key_value_pairs}')
                raise


def collect_folders(folders: List[str],
                    atomsname: str = None,
                    patterns: List[str] = None,
                    children_patterns: List[str] = None,
                    dbname: str = None,
                    jobid: int = None):
    """Collect `myfolders` to `mydbname`.

    This wraps _collect_folders and handles printing exception traceback, which
    is broken using multiproces.

    """
    try:
        return _collect_folders(folders=folders, atomsname=atomsname,
                                patterns=patterns,
                                children_patterns=children_patterns,
                                dbname=dbname,
                                jobid=jobid)
    except Exception:
        # Put all exception text into an exception and raise that
        raise Exception("".join(traceback.format_exception(*sys.exc_info())))


def delegate_to_njobs(njobs, dbpath, name, folders, atomsname,
                      patterns, children_patterns, dbname):
    print(f'Delegating database collection to {njobs} subprocesses.')
    processes = []
    for jobid in range(njobs):
        jobdbname = dbpath.parent / f'{name}.{jobid}.db'
        proc = multiprocessing.Process(
            target=collect_folders,
            args=(folders[jobid::njobs], ),
            kwargs={
                'jobid': jobid,
                'dbname': jobdbname,
                'atomsname': atomsname,
                'patterns': patterns,
                'children_patterns': children_patterns
            })
        processes.append(proc)
        proc.start()

    for jobid, proc in enumerate(processes):
        proc.join()
        assert proc.exitcode == 0, f'Error in Job #{jobid}.'

    # Then we have to collect the separately collected databases
    # to a single final database file.
    print(f'Merging separate database files to {dbname}',
          flush=True)
    nmat = 0
    with connect(dbname, serial=True) as db2:
        for jobid in range(njobs):
            jobdbname = f'{dbname}.{jobid}.db'
            assert Path(jobdbname).is_file()
            print(f'Merging {jobdbname} into {dbname}', flush=True)
            with connect(f'{jobdbname}', serial=True) as db:
                for row in db.select():
                    kvp = row.get('key_value_pairs', {})
                    data = row.get('data')
                    db2.write(row.toatoms(), data=data, **kvp)
                    nmat += 1
    print('Done.', flush=True)
    nmatdb = len(db2)
    assert nmatdb == nmat, \
        ('Merging of databases went wrong, '
         f'number of materials changed: {nmatdb} != {nmat}')

    for name in Path().glob(f'{dbname}.*.db'):
        name.unlink()


@command('asr.database.fromtree', save_results_file=False)
@argument('folders', nargs=-1, type=str)
@option('-r', '--recursive', is_flag=True,
        help='Recurse and collect subdirectories.')
@option('--children-patterns', type=str)
@option('--patterns', help='Only select files matching pattern.', type=str)
@option('--dbname', help='Database name.', type=str)
@option('--njobs', type=int,
        help='Delegate collection of database to NJOBS subprocesses. '
        'Can significantly speed up database collection.')
def main(folders: Union[str, None] = None,
         recursive: bool = False,
         children_patterns: str = '*',
         patterns: str = 'info.json,params.json,results-asr.*.json',
         dbname: str = 'database.db',
         njobs: int = 1) -> ASRResult:
    """Collect ASR data from folder tree into an ASE database."""
    from asr.database.key_descriptions import main as set_key_descriptions

    def item_show_func(item):
        return str(item)

    atomsname = 'structure.json'
    if not folders:
        folders = ['.']
    else:
        tmpfolders = []
        for folder in folders:
            tmpfolders.extend(glob.glob(folder))
        folders = tmpfolders

    if recursive:
        print('Recursing through folder tree...')
        newfolders = []
        for folder in folders:
            newfolders += recurse_through_folders(folder, atomsname)
        folders = newfolders
        print('Done.')

    folders.sort()
    patterns = patterns.split(',')
    children_patterns = children_patterns.split(',')

    # We use absolute path because of chdir in collect_folder()!
    dbpath = Path(dbname).absolute()
    name = dbpath.name

    # Delegate collection of database to subprocesses to reduce I/O time.
    if njobs > 1:
        delegate_to_njobs(njobs, dbpath, name, folders, atomsname,
                          patterns, children_patterns, dbname)
    else:
        _collect_folders(folders,
                         jobid=None,
                         dbname=dbname,
                         atomsname=atomsname,
                         patterns=patterns,
                         children_patterns=children_patterns)

    set_key_descriptions(dbname)
    results = check_database(dbname)
    missing_child_uids = results['missing_child_uids']
    duplicate_uids = results['duplicate_uids']

    if missing_child_uids:
        raise MissingUIDS(
            'Missing child uids in collected database. '
            'Did you collect all subfolders?')

    if duplicate_uids:
        raise MissingUIDS(
            'Duplicate uids in database.')


if __name__ == '__main__':
    main.cli()
