"""test_stocks_news.py: validate behavior for datareader.stocks.news"""
from os import path

import pytest
import helpers

import prosper.datareader.stocks.news as news


def test_validate_google_response():
    """make sure expected transformation happens from news.validate_google_response()"""
    dummy_data = helpers.get_sample_json('google_news_sample.json')

    article_list = news.validate_google_response(dummy_data)

    helpers.dump_debug(article_list)

    assert False

class TestMarketNewsGoogle:
    config = helpers.CONFIG

    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = news.fetch_market_news_google()

        assert isinstance(news_list, list)

        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news.schema')
            )

    def test_pretty_news(self):
        news_list = news.fetch_market_news_google(pretty=True)

        assert isinstance(news_list, list)

        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news_pretty.schema')
            )
