=========================
prosper.datareader.stocks
=========================

Meant as an extension of `pandas-datareader`_, ``prosper.datareader.stocks`` provides utilities for collecting news and quotes from other sources.

``prosper.datareader.stocks`` relies on services from `Robinhood`_ to collect data.

Though `pandas-datareader`_ is a powerful tool for generic data fetching, it lacks some support for `Robinhood`_.

get_quote_rh()
--------------

    ``quote_dataframe = stocks.get_quote_rh('TICKER')``

Default quote data:

- symbol
- simple_name
- pe_ratio
- pct_change
- current_price
- updated_at

Designed to mirror ``pandas_datareader.data.get_quote_yahoo()`` from `pandas-datareader`_

.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _Robinhood: https://support.robinhood.com/hc/en-us
.. _company_news_google(): source/datareader.stocks.html#datareader.stocks.news.fetch_company_news_google
.. _company_news_rh(): source/datareader.stocks.html#datareader.stocks.news.fetch_company_news_rh
.. _market_news_google(): source/datareader.stocks.html#datareader.stocks.news.fetch_market_news_google
.. _get_quote_rh(): source/datareader.stocks.html#datareader.stocks.prices.get_quote_rh