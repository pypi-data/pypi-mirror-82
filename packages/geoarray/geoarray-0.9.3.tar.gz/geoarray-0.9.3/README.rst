========
geoarray
========


Fast Python interface for geodata - either on disk or in memory.

The geoarray package facilitates reading and writing of all GDAL compatible image file formats
and provides functions for geospatial processing.


* Free software: GNU General Public License v3 or later (GPLv3+)
* Documentation: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/doc/


Status
------

.. .. image:: https://img.shields.io/travis/danschef/geoarray.svg
        :target: https://travis-ci.org/danschef/geoarray

.. .. image:: https://readthedocs.org/projects/geoarray/badge/?version=latest
        :target: https://geoarray.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. .. image:: https://pyup.io/repos/github/danschef/geoarray/shield.svg
     :target: https://pyup.io/repos/github/danschef/geoarray/
     :alt: Updates

.. image:: https://gitext.gfz-potsdam.de/danschef/geoarray/badges/master/pipeline.svg
        :target: https://gitext.gfz-potsdam.de/danschef/geoarray/commits/master
.. image:: https://gitext.gfz-potsdam.de/danschef/geoarray/badges/master/coverage.svg
        :target: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/coverage/
.. image:: https://img.shields.io/pypi/v/geoarray.svg
        :target: https://pypi.python.org/pypi/geoarray
.. image:: https://img.shields.io/pypi/l/geoarray.svg
        :target: https://gitext.gfz-potsdam.de/danschef/geoarray/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/geoarray.svg
        :target: https://img.shields.io/pypi/pyversions/geoarray.svg
.. image:: https://img.shields.io/pypi/dm/geoarray.svg
        :target: https://pypi.python.org/pypi/geoarray


See also the latest coverage_ report and the nosetests_ HTML report.


Features and usage
------------------

* There is an example notebook that shows how to use geoarray: here_.


Installation
------------
geoarray depends on some open source packages which are usually installed without problems by the automatic install
routine. However, for some projects, we strongly recommend resolving the dependency before the automatic installer
is run. This approach avoids problems with conflicting versions of the same software.
Using conda_, the recommended approach is:

 .. code-block:: console

    # create virtual environment for geoarray, this is optional
    conda create -c conda-forge --name geoarray python=3
    source activate geoarray
    conda install -c conda-forge numpy gdal scikit-image matplotlib pandas pyproj cartopy shapely geopandas
    conda install -c conda-forge holoviews  # optional, in case you want to use interactive plotting


To install geoarray, use the pip installer:

.. code-block:: console

    pip install geoarray


* Or clone the repository via GIT and update the PATH environment variable:

.. code-block:: console

    cd /your/installation/folder
    git clone https://gitext.gfz-potsdam.de/danschef/geoarray.git
    PATH=$PATH:~/path/to/your/installation/folder/geoarray


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _coverage: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/coverage/
.. _nosetests: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/nosetests_reports/nosetests.html
.. _conda: https://conda.io/docs/
.. _here: examples/notebooks/features_and_usage.ipynb
