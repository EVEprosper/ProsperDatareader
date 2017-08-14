=========================
prosper.datareader.stocks
=========================

Meant as an extension of `pandas-datareader`_, ``prosper.datareader.stocks`` provides utilities for collecting news and quotes from other sources.

``prosper.datareader.stocks`` relies on services from `Google`_ and `Robinhood`_ to collect data.

News
====

Fetching news feeds should be easy.  These endpoints return dataframes with articles, links, and some metadata.  These feeds save you from a few pitfalls.

- Non-compliant JSON 
- Weird single-character identifiers
- Strange tree-shaped feeds

company_news_google()
---------------------

    ``news_dataframe = stocks.news.company_news_google('TICKER')``

Fetches all the news articles for a single ticker.  Human readable headers are enabled by default, but ``pretty=False`` will return columns to original short-names

market_news_google()
--------------------

    ``news_dataframe = stocks.news.market_news_google()``

Fetches all articles on `Google`_ general market feed.  Technically wrapped around ``company_news_google()`` function.  

company_news_rh()
-----------------

    ``news_dataframe = stocks.news.company_news_rh('TICKER')``

Fetches articles from `Robinhood`_ for desired ticker.  NOTE: ``page_limit`` may be needed for popular stocks.


Prices
======

Though `pandas-datareader`_ is a powerful tool for generic data fetching, it lacks some support for `Robinhood`_.

get_quote_rh()
--------------

    ``quote_dataframe = stocks.prices.get_quote_rh('TICKER')``

Default quote data:

- symbol
- simple_name
- pe_ratio
- pct_change
- current_price
- updated_at

Designed to mirror ``pandas_datareader.data.get_quote_yahoo()`` from `pandas-datareader`_

.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _Google: https://www.google.com/finance
.. _Robinhood: https://support.robinhood.com/hc/en-us
.. _company_news_google(): source/datareader.stocks.html#datareader.stocks.news.fetch_company_news_google
.. _company_news_rh(): source/datareader.stocks.html#datareader.stocks.news.fetch_company_news_rh
.. _market_news_google(): source/datareader.stocks.html#datareader.stocks.news.fetch_market_news_google
.. _get_quote_rh(): source/datareader.stocks.html#datareader.stocks.prices.get_quote_rh