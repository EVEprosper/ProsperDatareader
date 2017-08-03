===============
Getting Started
===============

ProsperDatareader is a group of libraries designed to help get common data.  Additional data-sources should be easy to extend as long as the result data can be returned by `Pandas`_.  Inspiration taken from `pandas-datareader`_ 

Using ProsperDatareader
=======================

    ``pip install ProsperDatareader``

It is encouraged to install the smallest scope required.

.. code-block:: python
   :linenos:

   import prosper.datareader.stocks as stocks

   todays_news = stocks.news.company_news_google('MU')

   todays_quote = stocks.prices.get_quote_rh('MU')

.. _Pandas: http://pandas.pydata.org/
.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html