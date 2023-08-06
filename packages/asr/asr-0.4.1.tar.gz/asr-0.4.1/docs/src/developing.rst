Development
===========


Run tests
---------

.. code-block::

   $ tox -e flake8 doctest py36 py36-gpaw


Build documentation
-------------------

.. code-block::

   $ tox -e docs

Make a new release
------------------

Preferably make a new branch

.. code-block:: console

   $ git checkout -b release-DATE

Make a minor release

.. code-block:: console

   $ bumpversion minor

Make a major release

.. code-block:: console

   $ bumpversion major


Implementing new recipes
------------------------

TODO: Make tutorial on writing recipes.

In the following you will find the necessary information needed to
implement new recipes into the ASR framework. The first section gives
an ultra short description of how to implement new recipes, and the
following sections go into more detail.
