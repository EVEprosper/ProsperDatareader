=======================
prosper.datareader.news
=======================

Fetching news feeds should be easy.  These endpoints return dataframes with articles, links, and some metadata.  These feeds save you from a few pitfalls.

- Non-compliant JSON 
- Weird single-character identifiers
- Strange tree-shaped feeds

company_news_rh()
-----------------

    ``news_dataframe = news.company_news_rh('TICKER')``

Fetches articles from `Robinhood`_ for desired ticker.  NOTE: ``page_limit`` may be needed for popular stocks.

**NOTE**: Google datasources have been deprecated