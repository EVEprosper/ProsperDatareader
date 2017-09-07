"""test_stocks_news.py: validate behavior for datareader.stocks.news"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

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

class TestMarketNewsGoogle:
    """valdiate behavior on market_news_google()"""
    @pytest.mark.long
    def test_fetch_market_news_raw(self):
        """validate data coming in matches expected shape"""
        news_list = news.fetch_company_news_google(
            '',
            uri=news.GOOGLE_MARKET_NEWS
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

    def test_market_news_google_happypath(self):
        """validate default behavior"""
        all_news_df = news.market_news_google()

        assert isinstance(all_news_df, pandas.DataFrame)

        expected_cols = [
            'age', 'primary', 'source', 'blurb',
            'sru', 'title', 'datetime', 'url', 'usg'
        ]

        assert list(all_news_df.columns.values) == expected_cols

    def test_market_news_google_no_pretty(self):
        """validate not-pretty return works as expected"""
        all_news_df = news.market_news_google(pretty=False)

        assert isinstance(all_news_df, pandas.DataFrame)

        expected_cols = [
            'd', 'primary', 's', 'sp', 'sru', 't', 'tt', 'u', 'usg'
        ]

        assert list(all_news_df.columns.values) == expected_cols

class TestCompanyNewsGoogle:
    """validate behavior for news.fetch_company_news_google()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')

    @pytest.mark.long
    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = news.fetch_company_news_google(self.good_ticker)

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
            news_list = news.fetch_company_news_google(self.bad_ticker)

    def test_company_news_happypath(self):
        """make sure pandas wrapper works as expected"""
        all_news_df = news.company_news_google(self.good_ticker)

        assert isinstance(all_news_df, pandas.DataFrame)

        expected_cols = [
            'age', 'primary', 'source', 'blurb',
            'sru', 'title', 'datetime', 'url', 'usg'
        ]

        assert list(all_news_df.columns.values) == expected_cols


    def test_company_news_no_pretty(self):
        """validate not-pretty return works as expected"""
        all_news_df = news.company_news_google(
            self.good_ticker,
            pretty=False
        )

        assert isinstance(all_news_df, pandas.DataFrame)

        expected_cols = [
            'd', 'primary', 's', 'sp', 'sru', 't', 'tt', 'u', 'usg'
        ]

        assert list(all_news_df.columns.values) == expected_cols

    @pytest.mark.long
    def test_vader_application(self):
        """make sure use-case for news + vader works"""
        import prosper.datareader.utils as utils
        all_news_df = news.company_news_google(self.good_ticker)

        graded_news = utils.vader_sentiment(all_news_df, 'title')

        expected_cols = [
            'age', 'primary', 'source', 'blurb',
            'sru', 'title', 'datetime', 'url', 'usg',
            'neu', 'pos', 'compound', 'neg'
        ]

        assert list(graded_news.columns.values) == expected_cols

class TestCompanyNewsRobinhood:
    """validate behavior for news.fetch_company_news_rh()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')
    expected_news_cols = [
        'api_source', 'author', 'instrument', 'num_clicks', 'preview_image_url',
        'published_at', 'relay_url', 'source', 'summary', 'title', 'updated_at',
        'url', 'uuid'
    ]

    @pytest.mark.long
    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = news.fetch_company_news_rh(self.good_ticker)

        assert isinstance(news_list, list)

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


    def test_company_news_rh_happypath(self):
        """make sure production endpoint works as expected"""
        all_news_df = news.company_news_rh(self.good_ticker)

        assert isinstance(all_news_df, pandas.DataFrame)

        assert list(all_news_df.columns.values) == self.expected_news_cols

    @pytest.mark.long
    def test_vader_application(self):
        """make sure use-case for news + vader works"""
        import prosper.datareader.utils as utils
        all_news_df = news.company_news_rh(self.good_ticker)

        graded_news = utils.vader_sentiment(all_news_df, 'title')

        expected_cols = self.expected_news_cols
        expected_cols.extend(['neu', 'pos', 'compound', 'neg'])

        print(list(graded_news.columns.values))
        assert list(graded_news.columns.values) == expected_cols
