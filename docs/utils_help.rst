=========================
prosper.datareader.utils
=========================

General utilities for additional data management.  Useful functions and classes for getting even more out of generic data sources.

NLTK Utilities
==============

`NLTK`_ provides a platform for building `NLP`_ tools; granting easier access to cutting edge plain-language parsing.

**NOTE**: requires ``pip install prosperdatareader[nltk]`` to enable.  Not downloaded by default to trim down optional libraries.

vader_sentiment()
-----------------

Designed originally for use with `stocks.news`_, ``vader_sentiment()`` allows for basic application of the `Vader sentiment analyzer`_.  This provides a basic breakdown of english speech on a [-1.0, 1.0] scale:

* positive
* negative
* neutral
* compound

.. code-block:: python

    import prosper.datareader.stocks as stocks
    import prosper.datareader.utils as utils

    ## load a pandas.DataFrame with today's market news
    ## Expected columns: TODO
    market_news_df = stocks.news.market_news_google(pretty=True)

    ## grade article titles
    ## Expected columns: TODO
    market_news_df = utils.vader_sentiment(
        market_news_df, #DataFrame full of data
        'title'         #which column to grade
    )

    worst_article = market_news_df[max(market_news_df['neg'])] 
    bleakest_article = market_news_df[min(market_news_df['compound'])]
    brightest_article = market_news_df[max(market_news_df['compound'])]
    best_article = market_news_df[max(market_news_df['pos'])]

**NOTE**: for running ``vader_sentiment()`` over the same DataFrame twice, note that ``vader_columns`` is available.  Requires strict equivalence for column count and order.

    ``COLUMN_NAMES = ['neu', 'pos', 'compound', 'neg']``

.. code-block:: python

    market_news_df = utils.vader_sentiment(
        market_news_df,
        'title'
        vader_columns=['title_neu', 'title_pos', 'title_compound', 'title_neg']
    )

    market_news_df = utils.vader_sentiment(
        market_news_df,
        'blurb',
        vader_columns=['blurb_neu', 'blurb_pos', 'blurb_compound', 'blurb_neg']
    )

.. _`NLTK`: http://www.nltk.org/
.. _`NLP`: https://en.wikipedia.org/wiki/Natural_language_processing
.. _`stocks.news`: stocks_help.html
.. _`Vader sentiment analyzer`: http://www.nltk.org/api/nltk.sentiment.html#module-nltk.sentiment.vader