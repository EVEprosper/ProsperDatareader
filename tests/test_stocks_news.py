"""test_stocks_news.py: validate behavior for datareader.stocks.news"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers

import prosper.datareader.stocks.news as news
import prosper.datareader.exceptions as exceptions

class TestValidateGoogleResponse:
    """validate behavior for news.validate_google_response()"""
    def test_validate_google_response_happypath(self):
        """expected default behavior"""
        article_list = news.validate_google_response(
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
        no_primary_article_list = news.validate_google_response(
            helpers.get_sample_json('google_news_sample.json'),
            tag_primary=False
        )
        test_article = no_primary_article_list[0]

        assert 'primary' not in test_article

        helpers.validate_schema(
            test_article,
            path.join('stocks', 'google_company_news.schema')
        )

class TestPrettyGoogleNews:
    """validate behavior for news.pretty_return_google_news"""
    def test_pretty_google_news(self):
        """make sure expected transformation happens from news.pretty_return_google_news()"""
        article_list = news.validate_google_response(
            helpers.get_sample_json('google_news_sample.json'))
        pretty_list = news.pretty_return_google_news([article_list[0]])

        pretty_entry = pretty_list[0]
        helpers.validate_schema(
            pretty_entry,
            path.join('stocks', 'google_company_news_pretty.schema')
        )

        assert 'usg' not in pretty_entry
        assert 'sru' not in pretty_entry
        assert 'primary' in pretty_entry

    def test_pretty_google_news_keep_links(self):
        """test expected result for keep_google_links"""
        article_list = news.validate_google_response(
            helpers.get_sample_json('google_news_sample.json'))
        pretty_list = news.pretty_return_google_news([article_list[0]], keep_google_links=True)

        pretty_entry = pretty_list[0]
        helpers.validate_schema(
            pretty_entry,
            path.join('stocks', 'google_company_news_pretty.schema')
        )

        assert 'usg' in pretty_entry
        assert 'sru' in pretty_entry
        assert 'primary' in pretty_entry

    def test_pretty_google_news_no_primary(self):
        """test expected pretty result without tag_primary data"""
        no_primary_list = news.validate_google_response(
            helpers.get_sample_json('google_news_sample.json'),
            tag_primary=False
        )
        pretty_no_primary = news.pretty_return_google_news([no_primary_list[0]])

        no_primary_entry = pretty_no_primary[0] #I love this anime
        helpers.validate_schema(
            no_primary_entry,
            path.join('stocks', 'google_company_news_pretty.schema')
        )

        assert 'primary' not in no_primary_entry
        assert 'usg' not in no_primary_entry
        assert 'sru' not in no_primary_entry

class TestMarketNewsGoogle:
    config = helpers.CONFIG

    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = news.fetch_market_news_google()

        assert isinstance(news_list, list)

        sample_article = news_list[0]
        assert isinstance(sample_article, dict)
        assert 'primary' in sample_article
        assert 'usg' in sample_article
        assert 'sru' in sample_article

        ## NOTE: slow ##
        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news.schema')
            )

    def test_pretty_news(self):
        """validate behavior -- pretty results"""
        news_list = news.fetch_market_news_google(pretty=True)

        assert isinstance(news_list, list)

        sample_article = news_list[0]
        assert isinstance(sample_article, dict)
        assert 'primary' in sample_article
        assert 'usg' not in sample_article
        assert 'sru' not in sample_article

        ## NOTE: slow ##
        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news_pretty.schema')
            )

    def test_pretty_keep_links(self):
        """validate behavior -- pretty + keep_google_links"""
        news_list = news.fetch_market_news_google(pretty=True, keep_google_links=True)

        assert isinstance(news_list, list)

        sample_article = news_list[0]
        assert isinstance(sample_article, dict)
        assert 'primary' in sample_article
        assert 'usg' in sample_article
        assert 'sru' in sample_article

class TestCompanyNewsGoogle:
    """validate behavior for news.fetch_company_news_google()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')

    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = news.fetch_company_news_google(self.good_ticker)

        assert isinstance(news_list, list)

        sample_article = news_list[0]
        assert isinstance(sample_article, dict)
        assert 'primary' in sample_article
        assert 'usg' in sample_article
        assert 'sru' in sample_article

        ## NOTE: slow ##
        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news.schema')
            )

    def test_default_bad_ticker(self):
        """validate behavior -- incorrect ticker"""
        with pytest.raises(requests.exceptions.HTTPError):
            news_list = news.fetch_company_news_google(self.bad_ticker)

    def test_pretty_news(self):
        """validate behavior -- pretty print"""
        news_list = news.fetch_company_news_google(
            self.good_ticker,
            pretty=True
        )

        assert isinstance(news_list, list)

        sample_article = news_list[0]
        assert isinstance(sample_article, dict)
        assert 'primary' in sample_article
        assert 'usg' not in sample_article
        assert 'sru' not in sample_article

        ## NOTE: slow ##
        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'google_company_news_pretty.schema')
            )

    def test_pretty_keep_links(self):
        """validate behavior -- pretty + keep_google_links"""
        news_list = news.fetch_company_news_google(
            self.good_ticker,
            pretty=True,
            keep_google_links=True
        )

        assert isinstance(news_list, list)

        sample_article = news_list[0]
        assert isinstance(sample_article, dict)
        assert 'primary' in sample_article
        assert 'usg' in sample_article
        assert 'sru' in sample_article

class TestCompanyNewsRobinhood:
    """validate behavior for news.fetch_company_news_rh()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')

    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = news.fetch_company_news_rh(self.good_ticker)

        assert isinstance(news_list, list)

        ## NOTE: slow ##
        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'rh_news.schema')
            )

    def test_default_bad_ticker(self):
        """validate behavior -- incorrect ticker"""
        #with pytest.raises(requests.exceptions.HTTPError):
        news_list = news.fetch_company_news_rh(self.bad_ticker)

    def test_page_stop(self):
        """make sure page limit works"""
        long_news_list = news.fetch_company_news_rh(self.good_ticker)

        short_news_list = news.fetch_company_news_rh(
            self.good_ticker,
            page_limit=2
        )

        assert len(long_news_list) > len(short_news_list)

    def test_hard_page_stop(self):
        """make sure anti-recursion stop works as intended"""
        default_page_hardbreak = news.PAGE_HARDBREAK
        news.PAGE_HARDBREAK = 2

        with pytest.warns(exceptions.PaginationWarning):
            news_list = news.fetch_company_news_rh(self.good_ticker)

        news.PAGE_HARDBREAK = default_page_hardbreak
