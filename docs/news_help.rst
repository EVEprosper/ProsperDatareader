=======================
prosper.datareader.news
=======================

Fetching news feeds should be easy.  These endpoints return dataframes with articles, links, and some metadata.  These feeds save you from a few pitfalls.

- Non-compliant JSON 
- Weird single-character identifiers
- Strange tree-shaped feeds

**NOTE**: Google datasources have been deprecated

company_news_rh()
-----------------

    ``news_dataframe = news.company_news_rh('TICKER')``

Fetches articles from `Robinhood`_ for desired ticker.  NOTE: ``page_limit`` may be needed for popular stocks.

company_news_intrinino()
------------------------

    ``news_dataframe = news.company_news_intrinino('ticker', ...)``

Fetches articles for `Intrinino`_ for desired ticker.  This feed is authenticated, and will require credentials from an `Intrinino account`_.

**NOTE**: authentication patterns.  Either/or, not both

- Direct auth: use special account/password combo in account info (not personal login credentials)
- Public-Key Auth: (**BROKEN**) use public-key api to authenticate

company_headlines_yahoo()
-------------------------

    ``news_dataframe = news.company_headlines_yahoo('ticker')``

Process `Yahoo Finance - Company News`_ feed for desired ticker.

.. _Robinhood: https://www.robinhood.com/
.. _Intrinino: https://intrinio.com/
.. _Intrinino account: https://intrinio.com/account
.. _Yahoo Finance - Company News: https://developer.yahoo.com/finance/company.html