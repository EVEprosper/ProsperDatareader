"""test_yahoo: exercise prosper.datareader.yahoo functions"""
import pytest
import helpers

import prosper.datareader.yahoo as yahoo
import prosper.datareader.exceptions as exceptions

def test_fetch_finance_headlines_happypath():
    """validate expected layout from yahoo raw feeds"""
    feed = yahoo.news.fetch_finance_headlines_yahoo('AAPL')
    assert isinstance(feed, list)

    [
        helpers.validate_schema(article, 'yahoo/yahoo_finance_headline.schema')
        for article in feed
    ]
