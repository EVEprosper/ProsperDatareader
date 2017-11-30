===============
Getting Started
===============

ProsperDatareader is a group of libraries designed to help get common data.  Additional data-sources should be easy to extend as long as the result data can be returned by `Pandas`_.  Inspiration taken from `pandas-datareader`_ 

Using ProsperDatareader
=======================

    ``pip install ProsperDatareader``

It is encouraged to import the smallest scope required.

.. code-block:: python
   :linenos:

   import prosper.datareader.stocks as stocks

   todays_quote = stocks.prices.get_quote_rh('MU')

Contributing Data Sources
=========================

The purpose of this project is to provide a common framework to fetch/parse data and put appropriate testing scaffolding around feeds.  New data sources are always encouraged!

The template for adding new functions is:

Consider Top-Level Needs
------------------------

If you are extending an existing framework, think of the common questions/data returned.  More stock functions should go with ``prosper.datareader.stocks``.  

Adding a wild new segment?  A new top-level module should be considered.  EX: adding `Albion`_ data parsing should be added to ``prosper.datareader.albion``.  

All functions in top-level scopes should return ``pandas.DataFrame``.

Consider Data Sources
---------------------

Though functionality might be mixed between scopes, sources should be split by API provider.  ``prosper.datareader.cryptocompare`` contains all the API parsing required to interface with `CryptoCompare`_.  These individual REST interfaces should then be imported into their useage scope like ``prosper.datareader.coins`` to return the data users expect.

Most data-source feeds should probably have `jsonschema`_ tests.

Developing ProsperDatareader
============================

Support for additional data sources is greatly encouraged.  Please feel free to submit a `pull request on GitHub`_ to help us support the feeds you use!

**Requirements for Code**

1. Please follow `pylint`_ guidelines.  
2. All functions need `Napoleon Style`_ docstrings.
3. 95% test coverage expected.
    * Please add `jsonschema`_ files to test new endpoints.
    * ``logger.error()`` messages encouraged where coverage is infeasible
4. Docs for new features.
5. Top-level functions should return ``pandas.DataFrame`` objects.

Testing
-------

    ``python setup.py test``

`Py.Test`_ is automatically integrated into the project.  Test requirements remain separate, but can be expanded with ``tests_require`` in ``setup.py``.

The most important part of our testing suite is `jsonschema`_ coverage for data sources.  Using `Travis-CI`_ + `jsonschema`_ we can stay ahead of breaking API changes.  This also helps us guarantee reliability for everyone who uses our tools!

Coverage requirements are in place to offload worry.  Though ``#pragma: no cover`` should be used sparingly, there are situations we cannot design for.  Please use ``logger.error()`` messaging in sticky spaces so `ProsperCommon`_ users can be alerted when something unexpected fails.

Docs
----

    ``sphinx-build -b html docs/ webpage/``

We use `Sphinx`_ to generate both pages and auto-documentation for `Napoleon Style`_ docstrings.  This allows us to upload to `readthedocs.io`_.

Documentation gives us a chance to show users how our utilities work.  Though we do not expect every function to have a paragraph in docs, we do expect top-level user functions to describe their use with ``..code-block: python`` samples where appropriate.

**WARNING**: Due to dependencies, auto-documentation is `currently broken`_

Release
-------

Release is handled by tagging + `Travis-CI`_.  Tagged versions are automatically pushed to `PyPI`_.  

Release message should include useful update notes, and versions should follow `Semantic Versioning`_ standard.

.. _Pandas: http://pandas.pydata.org/
.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _pull request on GitHub: https://github.com/EVEprosper/ProsperDatareader/pulls
.. _pylint: https://www.pylint.org/
.. _Napoleon Style: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
.. _jsonschema: https://spacetelescope.github.io/understanding-json-schema/index.html
.. _Py.Test: https://docs.pytest.org/en/latest/
.. _Travis-CI: https://travis-ci.org/EVEprosper/ProsperDatareader
.. _ProsperCommon: http://prospercommon.readthedocs.io/en/latest/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _readthedocs.io: https://readthedocs.org/
.. _currently broken: https://github.com/EVEprosper/ProsperUtilities/issues/2
.. _PyPI: https://pypi.python.org/pypi/ProsperDatareader
.. _Semantic Versioning: http://semver.org/
.. _CryptoCompare: https://www.cryptocompare.com/api/#introduction
.. _Albion: https://albion-data.com/