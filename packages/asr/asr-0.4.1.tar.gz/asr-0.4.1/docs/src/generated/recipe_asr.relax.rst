.. _recipe_asr.relax:

asr.relax
=========


.. contents:: Contents
   :local:

Summary
-------

This is the documentation for :py:mod:`asr.relax`-recipe.
This recipe is comprised of a single step, namely:

  - :py:func:`asr.relax.main`

Run this recipe through the CLI interface

.. code-block:: console

   $ asr run asr.relax

or as a python module

.. code-block:: console

   $ python -m asr.relax

Detailed description
--------------------
Relax atomic structures.

By defaults read from "unrelaxed.json" from disk and relaxes
structures and saves the final relaxed structure in "structure.json".

The relax recipe has a couple of note-worthy features:

  - It automatically handles structures of any dimensionality
  - It tries to enforce symmetries
  - It continously checks after each step that no symmetries are broken,
    and raises an error if this happens.


The recipe also supports relaxing structure with vdW forces using DFTD3.
To install DFTD3 do

.. code-block:: console

   $ mkdir ~/DFTD3 && cd ~/DFTD3
   $ wget chemie.uni-bonn.de/pctc/mulliken-center/software/dft-d3/dftd3.tgz
   $ tar -zxf dftd3.tgz
   $ make
   $ echo 'export ASE_DFTD3_COMMAND=$HOME/DFTD3/dftd3' >> ~/.bashrc
   $ source ~/.bashrc

Examples
--------
Relax without using DFTD3

.. code-block:: console

   $ ase build -x diamond Si unrelaxed.json
   $ asr run "relax --nod3"

Relax using the LDA exchange-correlation functional

.. code-block:: console

   $ ase build -x diamond Si unrelaxed.json
   $ asr run "relax --calculator {'xc':'LDA',...}"




Steps
-----


asr.relax
^^^^^^^^^
.. autofunction:: asr.relax.main
   