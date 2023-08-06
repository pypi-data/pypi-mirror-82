KM3NeT TestData
===============

.. image:: https://git.km3net.de/km3py/km3net-testdata/badges/master/pipeline.svg
    :target: https://git.km3net.de/km3py/km3net-testdata/pipelines

.. image:: https://git.km3net.de/km3py/km3net-testdata/badges/master/coverage.svg
    :target: https://km3py.pages.km3net.de/km3net-testdata/coverage

.. image:: https://examples.pages.km3net.de/km3badges/docs-latest-brightgreen.svg
    :target: https://km3py.pages.km3net.de/km3net-testdata


A package to get access to KM3NeT sample files for testing and development
purposes.

Installation and usage
----------------------

    pip install km3net-testdata

The file paths can be access in Python scripts using the ``data_path()`` function:

.. code-block:: python

    from km3net_testdata import data_path()

    filename = data_path("offline/km3net_offline.root")

Notice the underscore in the Python package name (PyPI forces ``-`` but Python
package names are not allowed to use ``-``).

To use the module in e.g. shell scripts, the module can be called directly and
print the filepath:

.. code-block:: shell

   $ python -m km3net_testdata offline/km3net_offline.root
   /full/path/to/offline/km3net_offline.root


Acknowledgements
----------------

The project idea and implementation were inspired by the Scikit-HEP Project https://github.com/scikit-hep/scikit-hep-testdata
