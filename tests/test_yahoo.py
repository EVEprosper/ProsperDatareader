"""test_yahoo: exercise prosper.datareader.yahoo functions"""
import pytest
import helpers

import prosper.datareader.yahoo as yahoo
import prosper.datareader.exceptions as exceptions

def test_fetch_finance_headlines_happypath():
    """validate expected layout from yahoo raw feeds"""
    feed = yahoo.news.fetch_finance_headlines_yahoo('AAPL')
    print(feed)
    assert isinstance(feed, list)

    [
        helpers.validate_schema(article, 'yahoo/yahoo_finance_headline.schema')
        for article in feed
    ]

def test_fetch_industry_headlines_happypath():
    """validate expected layout from yahoo raw feeds"""
    feed = yahoo.news.fetch_finance_headlines_yahoo(
        'AAPL',
        uri=yahoo.news.INDUSTRY_NEWS_URL
    )
    print(feed[0])
    print(feed[0].keys())
    assert isinstance(feed, list)

    [
        helpers.validate_schema(article, 'yahoo/yahoo_industry_headline.schema')
        for article in feed
    ]
