"""Unique hash of atomic structure."""
from asr.core import command, ASRResult


def todict(atoms):
    import numpy as np
    d = dict(atoms.arrays)
    d['cell'] = np.asarray(atoms.cell)
    d['pbc'] = atoms.pbc
    if atoms._celldisp.any():
        d['celldisp'] = atoms._celldisp
    # if atoms.constraints:
    #     d['constraints'] = atoms.constraints
    if atoms.info:
        d['info'] = atoms.info
    return d


def get_hash_of_atoms(atoms):
    import numpy as np
    from hashlib import md5
    import json
    from collections import OrderedDict

    dct = todict(atoms)

    for key, value in dct.items():
        if isinstance(value, np.ndarray):
            value = value.tolist()
        dct[key] = value

    # Make sure that that keys appear in order
    orddct = OrderedDict()
    keys = list(dct.keys())
    keys.sort()
    for key in keys:
        orddct[key] = dct[key]

    hash = md5(json.dumps(orddct).encode()).hexdigest()
    return hash


def get_uid_of_atoms(atoms, hash):
    formula = atoms.symbols.formula
    return f'{formula:abc}-' + hash[:12]


@command(module='asr.database.material_fingerprint')
def main() -> ASRResult:
    from ase.io import read
    atoms = read('structure.json')
    hash = get_hash_of_atoms(atoms)
    uid = get_uid_of_atoms(atoms, hash)
    results = {'asr_id': hash,
               'uid': uid}
    return results


if __name__ == '__main__':
    main.cli()
