=========================
prosper.datareader.stocks
=========================

Meant as an extension of `pandas-datareader`_, ``prosper.datareader.stocks`` provides utilities for collecting news and quotes from other sources.

``prosper.datareader.stocks`` relies on services from `Google`_ and `Robinhood`_ to collect data.

News
====

Fetching news feeds should be easy.  These endpoints return dataframes with articles, links, and some metadata.

`company_news_google()`_ 
------------------------

``news_dataframe = stocks.news.company_news_google('TICKER')``

Fetches all the news articles for a single ticker.  

`company_news_rh()`_
--------------------

``news_dataframe = stocks.news.company_news_rh('TICKER')``

Fetches articles from `Robinhood`_ for desired ticker.  NOTE: ``page_limit`` may be needed for popular stocks.

`market_news_google()`_
-----------------------

``news_dataframe = stocks.news.market_news_google()``

Fetches all articles on `Google`_ general market feed

Prices
======

Though `pandas-datareader`_ is a powerful tool for generic data fetching, it lacks some support for `Robinhood`_.

`get_quote_rh()`_
-----------------

``quote_dataframe = stocks.prices.get_quote_rh('TICKER')``

Default quote data:

- symbol
- simple_name
- pe_ratio
- pct_change
- current_price
- updated_at

.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _Google: https://www.google.com/finance
.. _Robinhood: https://support.robinhood.com/hc/en-us
.. _company_news_google(): source/datareader.stocks.html#datareader.stocks.news.fetch_company_news_google
.. _company_news_rh(): source/datareader.stocks.html#datareader.stocks.news.fetch_company_news_rh
.. _market_news_google(): source/datareader.stocks.html#datareader.stocks.news.fetch_market_news_google
.. _get_quote_rh(): source/datareader.stocks.html#datareader.stocks.prices.get_quote_rh