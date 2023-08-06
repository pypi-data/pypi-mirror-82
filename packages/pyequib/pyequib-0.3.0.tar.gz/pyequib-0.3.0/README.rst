======================
pyEQUIB Python Package
======================

.. image:: https://img.shields.io/pypi/v/pyequib.svg?style=flat
    :target: https://pypi.python.org/pypi/pyequib/
    :alt: PyPI Version
    
.. image:: https://travis-ci.org/equib/pyEQUIB.svg?branch=master
    :target: https://travis-ci.org/equib/pyEQUIB
    :alt: Build Status

.. image:: https://ci.appveyor.com/api/projects/status/b3gw6vgf8s0vu8nv?svg=true
    :target: https://ci.appveyor.com/project/danehkar/pyequib
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/equib/pyEQUIB/badge.svg?
    :target: https://coveralls.io/github/equib/pyEQUIB?branch=master
    :alt: Coverage Status

.. image:: https://img.shields.io/badge/license-GPL-blue.svg
    :target: https://github.com/equib/pyEQUIB/blob/master/LICENSE
    :alt: GitHub license

.. image:: https://img.shields.io/badge/python-2.7%2C%203.8-blue.svg
    :alt: Support Python versions 2.7 and 3.8


Description
===========

The **pyEQUIB** library is a collection of Python programs developed to perform plasma diagnostics and abundance analysis using emission line fluxes measured in ionzed nebulae. It uses the AtomNeb Python Package to read collision strengths and transition probabilities for collisionally excited lines (CEL), and recombination coefficients for recombination lines (RL). This Python package can be used to determine interstellar extinctions, electron temperatures, electron densities, and ionic abundances from the measured fluxes of emission lines. It mainly contains the follwing API functions written purely in Python.

Installation
============

Dependent Python Packages
-------------------------

 This package requires the following packages:

    - `NumPy <https://numpy.org/>`_
    - `SciPy <https://scipy.org/scipylib/>`_
    - `AtomNeb <https://github.com/atomneb/AtomNeb-py/>`_
    
* To get this package with the AtomNeb FITS files, you can simply use ``git`` command as follows::

        git clone --recursive https://github.com/equib/pyEQUIB

To install the last version, all you should need to do is

.. code-block::

    $ python setup.py install

To install the stable version, you can use the preferred installer program (pip):

.. code-block::

    $ pip install pyequib


References
==========
* Danehkar, A. (2018). proEQUIB: IDL Library for Plasma Diagnostics and Abundance Analysis. *J. Open Source Softw.*, **3**, 899. doi:`10.21105/joss.00899 <https://doi.org/10.21105/joss.00899>`_  ads:`2018JOSS....3..899D <https://ui.adsabs.harvard.edu/abs/2018JOSS....3..899D>`_.

