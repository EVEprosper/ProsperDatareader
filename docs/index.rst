.. ProsperDatareader documentation master file, created by
   sphinx-quickstart on Mon Jul 31 09:30:33 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
ProsperDatareader
=================

|Build Status| |Coverage Status| |PyPI Badge| |Docs|

Helper libraries for reading/parsing common data used in `Prosper`_ tools.  Drawing inspiration from `pandas-datareader`_ library as a companion.

Quickstart
==========

Install ProsperDatareader:

    ``pip install ProsperDatareader``

Supported Feeds
===============

* `Utils`_: General utilities for additional insights
* `Stocks`_: Parse IRL stock quote data
* `Coins`_: Data utilities for cryptocoin price quotes

Index
=====

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started.rst
   stocks_help.rst
   coins_help.rst
   utils_help.rst
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Prosper: http://www.eveprosper.com
.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _Stocks: stocks_help.html
.. _Utils: utils_help.html
.. _Coins: coins_help.html

.. |Build Status| image:: https://travis-ci.org/EVEprosper/ProsperDatareader.svg?branch=master
   :target: https://travis-ci.org/EVEprosper/ProsperDatareader
.. |Coverage Status| image:: https://coveralls.io/repos/github/EVEprosper/ProsperDatareader/badge.svg?branch=master
   :target: https://coveralls.io/github/EVEprosper/ProsperDatareader?branch=master
.. |PyPI Badge| image:: https://badge.fury.io/py/ProsperDatareader.svg
   :target: https://badge.fury.io/py/ProsperDatareader
.. |Docs| image:: https://readthedocs.org/projects/prosperdatareader/badge/?version=latest