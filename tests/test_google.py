"""validate prosper.datareader.google tools"""
from os import path

import pytest
import helpers
import requests

import prosper.datareader.google as google
import prosper.datareader.exceptions as exceptions

class TestValidateGoogleResponse:
    """validate behavior for news.validate_google_response()"""
    def test_validate_google_response_happypath(self):
        """expected default behavior"""
        article_list = google.news.validate_google_response(
            helpers.get_sample_json('google_news_sample.json'))

        expected_primary = article_list[0]
        expected_non_primary = article_list[1]

        assert expected_primary['primary']
        assert not expected_non_primary['primary']

        helpers.validate_schema(
            expected_primary,
            path.join('stocks', 'google_company_news.schema')
        )

        helpers.validate_schema(
            expected_non_primary,
            path.join('stocks', 'google_company_news.schema')
        )

    def test_validate_google_repsonse_no_primary(self):
        """"epected results without tag_primary"""
        no_primary_article_list = google.news.validate_google_response(
            helpers.get_sample_json('google_news_sample.json'),
            tag_primary=False
        )
        test_article = no_primary_article_list[0]

        assert 'primary' not in test_article

        helpers.validate_schema(
            test_article,
            path.join('stocks', 'google_company_news.schema')
        )

def test_fetch_market_news_raw():
    """validate data coming in matches expected shape"""
    news_list = google.news.fetch_company_news_google(
        '',
        uri=google.news.GOOGLE_MARKET_NEWS
    )

    assert isinstance(news_list, list)

    sample_article = news_list[0]
    assert isinstance(sample_article, dict)
    assert 'primary' in sample_article
    assert 'usg' in sample_article
    assert 'sru' in sample_article

    for article in news_list:
        assert isinstance(article, dict)
        helpers.validate_schema(
            article,
            path.join('stocks', 'google_company_news.schema')
        )


class TestCompanyNewsGoogleRaw:
    """validate behavior for news.fetch_company_news_google()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')

    @pytest.mark.long
    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = google.news.fetch_company_news_google(self.good_ticker)

        assert isinstance(news_list, list)

        sample_article = news_list[0]
        assert isinstance(sample_article, dict)
        assert 'primary' in sample_article
        assert 'usg' in sample_article
        assert 'sru' in sample_article

        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news.schema')
            )

    def test_default_bad_ticker(self):
        """validate behavior -- incorrect ticker"""
        with pytest.raises(requests.exceptions.HTTPError):
            news_list = google.news.fetch_company_news_google(self.bad_ticker)
