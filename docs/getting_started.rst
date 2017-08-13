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

   todays_news = stocks.news.company_news_google('MU')

   todays_quote = stocks.prices.get_quote_rh('MU')

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
