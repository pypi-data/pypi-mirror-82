Introduction to the ASR run command
===================================
As you have just seen, the `run` command is used to execute run the recipes of ASR.
In most cases the run command is identical to executing the recipes as modules, ie.,
`asr run relax` is equivalent to `python -m asr.relax`. However, another usecase 
encountered frequently enough is to want to run a recipe in multiple directories.

The asr run command enables this with the following syntax::

  $ asr run relax folder1/ folder1/

which makes it easy to run commands in multiple folders. If you want to provide
arguments for the recipe (the relax recipe in this example) you can use::

  $ asr run "relax --ecut 100" folder1/ folder1/

The last option that the run commands provides is to execute other python modules
like `ase`. For example, suppose you have a lot of folders with a `structure.traj`
that you want to convert to `structure.json`. This can be done with the ase command
`ase convert structure.traj structure.json`. `run` can run this script in
many folders for you with::

  $ asr run --shell "ase convert structure.traj structure.json" materials/*/

where the `command` `asr run command` is used to tell ASR that the command you
wish to run is not a recipe.
