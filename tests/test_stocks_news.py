"""test_stocks_news.py: validate behavior for datareader.stocks.news"""
from os import path

import pytest
import helpers

import prosper.datareader.stocks.news as news

class TestMarketNewsGoogle:
    config = helpers.CONFIG

    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = news.fetch_market_news_google(self.config.get('STOCKS', 'good_ticker'))

        assert isinstance(news_list, list)

        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news.schema')
            )
