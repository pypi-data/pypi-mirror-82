"""Database web application."""
from typing import List
from asr.core import command, option, argument, ASRResult

import tempfile
from pathlib import Path

from ase.db import connect
from ase.db.app import app, projects
from flask import render_template, send_file, Response, jsonify
import flask.json
import asr
from ase import Atoms
from ase.calculators.calculator import kptdensity2monkhorstpack
from ase.geometry import cell_to_cellpar
from ase.formula import Formula
import warnings

tmpdir = Path(tempfile.mkdtemp(prefix="asr-app-"))  # used to cache png-files

path = Path(asr.__file__).parent.parent
app.jinja_loader.searchpath.append(str(path))


def create_key_descriptions(db=None):
    from asr.database.key_descriptions import key_descriptions
    from asr.database.fromtree import parse_key_descriptions
    from ase.db.web import create_key_descriptions

    flatten = {key: value
               for recipe, dct in key_descriptions.items()
               for key, value in dct.items()}

    if db is not None:
        metadata = db.metadata
        if 'keys' not in metadata:
            raise KeyError('Missing list of keys for database. '
                           'To fix this either: run database.fromtree again. '
                           'or python -m asr.database.set_metadata DATABASEFILE.')
        keys = metadata.get('keys')
    else:
        keys = list(flatten.keys())

    kd = {}
    for key in keys:
        description = flatten.get(key)
        if description is None:
            warnings.warn(f'Missing key description for {key}')
            continue
        kd[key] = description

    kd = {key: (desc['shortdesc'], desc['longdesc'], desc['units']) for
          key, desc in parse_key_descriptions(kd).items()}

    return create_key_descriptions(kd)


class Summary:
    def __init__(self, row, key_descriptions, create_layout, prefix=''):
        self.row = row

        atoms = Atoms(cell=row.cell, pbc=row.pbc)
        self.size = kptdensity2monkhorstpack(atoms,
                                             kptdensity=1.8,
                                             even=False)

        self.cell = [['{:.3f}'.format(a) for a in axis] for axis in row.cell]
        par = ['{:.3f}'.format(x) for x in cell_to_cellpar(row.cell)]
        self.lengths = par[:3]
        self.angles = par[3:]

        self.stress = row.get('stress')
        if self.stress is not None:
            self.stress = ', '.join('{0:.3f}'.format(s) for s in self.stress)

        self.formula = Formula(
            Formula(row.formula).format('metal')).format('html')

        kd = key_descriptions
        self.layout = create_layout(row, kd, prefix)

        self.dipole = row.get('dipole')
        if self.dipole is not None:
            self.dipole = ', '.join('{0:.3f}'.format(d) for d in self.dipole)

        self.data = row.get('data')
        if self.data:
            self.data = ', '.join(self.data.keys())

        self.constraints = row.get('constraints')
        if self.constraints:
            self.constraints = ', '.join(c.__class__.__name__
                                         for c in self.constraints)


def setup_app():

    @app.route("/")
    def index():
        return render_template(
            "asr/database/templates/projects.html",
            projects=sorted(
                [
                    (name, proj["title"], proj["database"].count())
                    for name, proj in projects.items()
                ]
            ),
        )

    @app.route("/<project>/file/<uid>/<name>")
    def file(project, uid, name):
        assert project in projects
        path = tmpdir / f"{project}/{uid}-{name}"  # XXXXXXXXXXX
        return send_file(str(path))

    setup_data_endpoints()


def setup_data_endpoints():
    """Set endpoints for downloading data."""
    from ase.io.jsonio import MyEncoder
    app.json_encoder = MyEncoder

    @app.route('/<project_name>/row/<uid>/all_data')
    def get_all_data(project_name: str, uid: str):
        """Show details for one database row."""
        project = projects[project_name]
        uid_key = project['uid_key']
        row = project['database'].get('{uid_key}={uid}'
                                      .format(uid_key=uid_key, uid=uid))
        content = flask.json.dumps(row.data)
        return Response(
            content,
            mimetype='application/json',
            headers={'Content-Disposition':
                     f'attachment;filename={uid}_data.json'})

    @app.route('/<project_name>/row/<uid>/data')
    def show_row_data(project_name: str, uid: str):
        """Show details for one database row."""
        project = projects[project_name]
        uid_key = project['uid_key']
        row = project['database'].get('{uid_key}={uid}'
                                      .format(uid_key=uid_key, uid=uid))
        sorted_data = {key: value for key, value
                       in sorted(row.data.items(), key=lambda x: x[0])}
        return render_template('asr/database/templates/data.html',
                               data=sorted_data, uid=uid, project_name=project_name)

    @app.route('/<project_name>/row/<uid>/data/<filename>')
    def get_row_data_file(project_name: str, uid: str, filename: str):
        """Show details for one database row."""
        project = projects[project_name]
        uid_key = project['uid_key']
        row = project['database'].get('{uid_key}={uid}'
                                      .format(uid_key=uid_key, uid=uid))
        return jsonify(row.data.get(filename))


@app.template_filter()
def asr_sort_key_descriptions(value):
    """Sort column drop down menu."""
    def sort_func(item):
        return item[1][1]

    return sorted(value.items(), key=sort_func)


def handle_query(args):
    return args["query"]


def row_to_dict(row, project, layout_function, tmpdir):
    project_name = project['name']
    uid = row.get(project['uid_key'])
    s = Summary(row,
                create_layout=layout_function,
                key_descriptions=project['key_descriptions'],
                prefix=str(tmpdir / f'{project_name}/{uid}-'))
    return s


def initialize_project(database):
    from asr.database import browser
    from functools import partial

    db = connect(database, serial=True)
    metadata = db.metadata
    name = metadata.get("name", Path(database).name)

    # Make temporary directory
    (tmpdir / name).mkdir()

    metadata = db.metadata
    projects[name] = {
        "name": name,
        "title": metadata.get("title", name),
        "key_descriptions": create_key_descriptions(db),
        "uid_key": metadata.get("uid", "uid"),
        "database": db,
        "handle_query_function": handle_query,
        "row_to_dict_function": partial(
            row_to_dict, layout_function=browser.layout, tmpdir=tmpdir
        ),
        "default_columns": metadata.get("default_columns", ["formula", "uid"]),
        "table_template": str(
            metadata.get(
                "table_template", f"asr/database/templates/table.html",
            )
        ),
        "search_template": str(
            metadata.get(
                "search_template", "asr/database/templates/search.html"
            )
        ),
        "row_template": str(
            metadata.get("row_template", "asr/database/templates/row.html")
        ),
    }


@command()
@argument("databases", nargs=-1, type=str)
@option("--host", help="Host address.", type=str)
@option("--test", is_flag=True, help="Test the app.")
def main(databases: List[str], host: str = "0.0.0.0",
         test: bool = False) -> ASRResult:
    for database in databases:
        initialize_project(database)

    setup_app()

    if test:
        import traceback
        app.testing = True
        with app.test_client() as c:
            for name in projects:
                print(f'Testing {name}')
                c.get(f'/{name}/').data.decode()
                project = projects[name]
                db = project['database']
                uid_key = project['uid_key']
                n = len(db)
                uids = []
                for row in db.select(include_data=False):
                    uids.append(row.get(uid_key))
                    if len(uids) == n:
                        break
                print(len(uids))

                for i, uid in enumerate(uids):
                    url = f'/{name}/row/{uid}'
                    print(f'\rRows: {i + 1}/{len(uids)} {url}',
                          end='', flush=True)
                    try:
                        c.get(url).data.decode()
                    except KeyboardInterrupt:
                        raise
                    except Exception:
                        print()
                        row = db.get(uid=uid)
                        exc = traceback.format_exc()
                        exc += (f'Problem with {uid}: '
                                f'Formula={row.formula} '
                                f'Prototype={row.crystal_prototype}\n'
                                + '-' * 20 + '\n')
                        with Path('errors.txt').open(mode='a') as fid:
                            fid.write(exc)
                            print(exc)
    else:
        app.run(host=host, debug=True)


if __name__ == "__main__":
    main.cli()
