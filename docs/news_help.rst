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

Fetches articles from `Robinhood`_ for desired ticker.  

**NOTE**: ``page_limit`` may be needed for popular stocks.

company_news_intrinio()
------------------------

    ``news_dataframe = news.company_news_intrinino('ticker', ...)``

Fetches articles for `Intrinio`_ for desired ticker.  This feed is authenticated, and will require credentials from an `Intrinio account`_.

**NOTE**: authentication patterns.  Either/or, not both

- Direct auth: use special account/password combo in account info (not personal login credentials)
- Public-Key Auth: (*BROKEN*) use public-key api to authenticate

company_headlines_yahoo()
-------------------------

    ``news_dataframe = news.company_headlines_yahoo('ticker')``

Process `Yahoo Finance - Company News`_ feed for desired ticker.

industry_headlines_yahoo()
--------------------------

    ``news_dataframe = news.industry_headlines_yahoo('ticker')``

Process `Yahoo Finance - Industry News`_ feed for a desired ticker.  

**NOTE**: only accepts company tickers, not industry segments.  Yahoo dictates the blend given the tickers, and gives no easy access to reverse engineer who's in what group.

.. _Robinhood: https://www.robinhood.com/
.. _Intrinio: https://intrinio.com/
.. _Intrinio account: https://intrinio.com/account
.. _Yahoo Finance - Company News: https://developer.yahoo.com/finance/company.html
.. _Yahoo Finance - Industry News: https://developer.yahoo.com/finance/industry.html
