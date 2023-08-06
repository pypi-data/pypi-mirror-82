The `setup.params` recipe
=========================

All material folders can contain a `params.json`-file. This file
specifies new defaults and take precedence over the standard defaults
that are specified in the actual recipes.

This file can be edited manually or the `setup.params` recipe can be
used to generate and manipulate it. The general syntax when using the
`setup.params` recipe is given from the help

.. doctest:: console
   :hide:

   >>> from asr.setup.params import main
   >>> main.cli(args=['-h'])
   Usage: asr run asr.setup.params [OPTIONS] recipe:option arg recipe:option arg
   ...


.. code-block:: console

   $ asr run "setup.params -h"
   Usage: asr run asr.setup.params [OPTIONS] recipe:option arg recipe:option arg
   ...

For example, to set custom default of the `asr.gs@calculate` recipe we
can run

.. code-block:: console

   $ asr run "setup.params asr.gs@calculate:calculator {'kpts':{...,'density':8.0},...}"

.. doctest::
   :hide:

   >>> from asr.setup.params import main
   >>> main(params=['asr.gs@calculate:calculator', "{'kpts':{...,'density':8.0},...}"])
   Running...asr.setup.params...'density':8.0...

This generates a file `params.json` with the contents printed above.',
i.e.,

.. code-block:: json
   :caption: params.json

   {
    "asr.gs@calculate": {
     "calculator": {
      "kpts": {
       "density": 8.0,
       "gamma": true
      },
      "name": "gpaw",
      "mode": {
       "name": "pw",
       "ecut": 800
      },
      "xc": "PBE",
      "basis": "dzp",
      "occupations": {
       "name": "fermi-dirac",
       "width": 0.05
      },
      "convergence": {
       "bands": "CBM+3.0"
      },
      "nbands": "200%",
      "txt": "gs.txt",
      "charge": 0
     }
    }
   }


.. note::
   
   The ellipsis operator ("...") is used for recipe arguments which
   dict-type defaults and indicates that the only the default values
   of the specified keys should be updated.

.. warning::

   Note that when running the command using the CLI it is imperative
   that there is no whitespace in the dict-representation as they
   would then be interpreted as different arguments.

   For example, the following is WRONG (note the whitespace)

   .. code-block:: console

      $ asr run "setup.params asr.gs@calculate:calculator {'kpts': {..., 'density': 8.0}, ...}"

The `setup.params` recipe can be run multiple times to specify
multiple defaults. For example, running

.. code-block:: console

   $ asr run "setup.params asr.gs@calculate:calculator {'kpts':{...,'density':8.0},...}"
   $ asr run "setup.params asr.gs@calculate:calculator {'mode':{'ecut':600,...},...}"

would set both the `kpts` and `mode` keys of the
`asr.gs@calculate:calculator` argument. Two parameters can also be
specified simultaneously by using

.. code-block:: console

   $ asr run "setup.params asr.relax:d3 True asr.gs@calculate:calculator {'kpts':{...,'density':8.0},...}"


In this way all default parameters exposed through the CLI of a recipe
can be corrected.
