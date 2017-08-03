======================
Contributing New Feeds
======================

The goal of ProsperDatareader is to be an easy stop for common data.  We cover the testing/fetching/crunching so users can more quickly **use** the data they're after.

Making A New Feed
=================

Dev Checklist
-------------

- Add new fetchers
- Add schemas to ``tests/schemas/[my_feed]`` for sources
- Add tests 
    - Schema tests: make sure source doesn't change
    - Unit tests: make sure API returns expected data
- Add doc explaining top-level interfaces

Requirements - MUST HAVE
------------------------

- `Napoleon Style`_ docstrings
- 95% Test Coverage
- 100% schema coverage for dependent REST calls
- Main functs return ``pandas.DataFrame`` 
- PEP8 style compliance
- ``prosper.common.prosper_logging`` logging hooks

Testing Notes
=============

Half of the reason this package exists is to use `Travis-CI`_ as a monitor for dependency changes.  Schema testing is a critical part of adding feeds to ProsperDatareader.  

Check out `Spacetelescope Tutorial`_ for JSON Schema writing

.. _Napoleon Style: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
.. _Travis-CI: https://travis-ci.org/
.. _Spacetelescope Tutorial: https://spacetelescope.github.io/understanding-json-schema/index.html