"""test prosper.datareader.news top-level functions"""
from os import path

import pytest
import helpers
import pandas as pd

import prosper.datareader.news as news
import prosper.datareader.exceptions as exceptions

CAN_DIRECT_AUTH = all([
    helpers.CONFIG.get('INTRINIO', 'username'),
    helpers.CONFIG.get('INTRINIO', 'password')
])
CAN_PUBLIC_KEY = bool(helpers.CONFIG.get('INTRINIO', 'public_key'))


class TestCompanyNewsRobinhood:
    """valdiate stocks.company_news_rh"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')
    expected_news_cols = [
        'api_source', 'author', 'instrument', 'num_clicks', 'preview_image_url',
        'published_at', 'relay_url', 'source', 'summary', 'title', 'updated_at',
        'url', 'uuid', 'preview_image_width', 'preview_image_height'
    ]

    def test_company_news_rh_happypath(self):
        """make sure production endpoint works as expected"""
        all_news_df = news.company_news_rh(self.good_ticker)

        assert isinstance(all_news_df, pd.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(all_news_df.columns.values),
            self.expected_news_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from company_news_rh(): {}'.format(unique_values)
            )

    @pytest.mark.long
    def test_vader_application(self):
        """make sure use-case for news + vader works"""
        import prosper.datareader.utils as utils
        all_news_df = news.company_news_rh(self.good_ticker)

        graded_news = utils.vader_sentiment(all_news_df, 'title')

        expected_cols = self.expected_news_cols
        expected_cols.extend(['neu', 'pos', 'compound', 'neg'])

        unique_values, unique_expected = helpers.find_uniques(
            list(graded_news.columns.values),
            expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from vader_sentiment(): {}'.format(unique_values)
            )

class TestCompanyNewsIntrinino:
    """validate news.company_news_intrinino"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    expected_cols = [
        'ticker', 'figi_ticker', 'figi', 'title', 'publication_date', 'summary', 'url',
    ]
    def test_company_news_intrinino_happypath_direct(self):
        """make sure production endpoint works as expected -- direct auth"""
        if not CAN_DIRECT_AUTH:
            pytest.xfail('Lacking creds for Intrinino -- direct auth')

        all_news_df = news.company_news_intrinio(
            self.good_ticker,
            username=helpers.CONFIG.get('INTRINIO', 'username'),
            password=helpers.CONFIG.get('INTRINIO', 'password')
        )

        assert isinstance(all_news_df, pd.DataFrame)
        unique_values, unique_expected = helpers.find_uniques(
            list(all_news_df.columns.values),
            self.expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from company_news_intrinino(): {}'.format(unique_values)
            )

    def test_company_news_intrinino_happypath_pubkey(self):
        """make sure production endpoint work as expected -- pubkey auth"""
        if not CAN_PUBLIC_KEY:
            pytest.xfail('Lacking creds for Intrinino -- pubkey auth')

        all_news_df = news.company_news_intrinio(
            self.good_ticker,
            public_key=helpers.CONFIG.get('INTRINIO', 'public_key')
        )

        assert isinstance(all_news_df, pd.DataFrame)
        unique_values, unique_expected = helpers.find_uniques(
            list(all_news_df.columns.values),
            self.expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from company_news_intrinino(): {}'.format(unique_values)
            )

    def test_company_news_intrinino_badauth(self):
        """make sure exceptions raise for bad auth patterns"""
        with pytest.raises(exceptions.InvalidAuth):
            bad_news_df = news.company_news_intrinio(
                self.good_ticker
            )

        with pytest.raises(exceptions.InvalidAuth):
            bad_news_df = news.company_news_intrinio(
                self.good_ticker,
                username='fake',
                password='fake',
                public_key='fake'
            )

    @pytest.mark.long
    def test_vader_application(self):
        """make sure Intrinino plays nice with vader"""
        import prosper.datareader.utils as utils
        if not CAN_DIRECT_AUTH:
            pytest.xfail('Lacking creds for Intrinino -- direct auth')

        all_news_df = news.company_news_intrinio(
            self.good_ticker,
            username=helpers.CONFIG.get('INTRINIO', 'username'),
            password=helpers.CONFIG.get('INTRINIO', 'password')
        )
        graded_news = utils.vader_sentiment(all_news_df, 'summary')

        expected_cols = self.expected_cols
        expected_cols.extend(['neu', 'pos', 'compound', 'neg'])

        unique_values, unique_expected = helpers.find_uniques(
            list(graded_news.columns.values),
            expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from vader_sentiment(): {}'.format(unique_values)
            )

class TestCompanyHeadlinesYahoo:
    """validate news.company_headlines_yahoo()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    expected_cols = [
        'id', 'link', 'published', 'summary', 'title'
    ]
    company_cols = [
        'id', 'link', 'published', 'summary', 'title', 'credit'
    ]
    def test_company_headlines_yahoo_happypath(self):
        """make sure production endpoint works as expected -- COMPANY"""
        all_news_df = news.company_headlines_yahoo(self.good_ticker)

        assert isinstance(all_news_df, pd.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(all_news_df.columns.values),
            self.expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from company_headlines_yahoo(): {}'.format(unique_values)
            )

    def test_industry_headlines_yahoo_happypath(self):
        """make sure production endpoint works as expected -- INDUSTRY"""
        all_news_df = news.industry_headlines_yahoo(self.good_ticker)

        assert isinstance(all_news_df, pd.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(all_news_df.columns.values),
            self.company_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from company_headlines_yahoo(): {}'.format(unique_values)
            )

    @pytest.mark.long
    def test_vader_application_company(self):
        """make sure use-case for news + vader works"""
        import prosper.datareader.utils as utils
        all_news_df = news.company_headlines_yahoo(self.good_ticker)

        graded_news = utils.vader_sentiment(all_news_df, 'title')

        expected_cols = self.expected_cols
        expected_cols.extend(['neu', 'pos', 'compound', 'neg'])

        unique_values, unique_expected = helpers.find_uniques(
            list(graded_news.columns.values),
            expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from vader_sentiment(): {}'.format(unique_values)
            )

    @pytest.mark.long
    def test_vader_application_industry(self):
        """make sure use-case for news + vader works"""
        import prosper.datareader.utils as utils
        all_news_df = news.industry_headlines_yahoo(self.good_ticker)

        graded_news = utils.vader_sentiment(all_news_df, 'title')

        expected_cols = self.company_cols
        expected_cols.extend(['neu', 'pos', 'compound', 'neg'])

        unique_values, unique_expected = helpers.find_uniques(
            list(graded_news.columns.values),
            expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from vader_sentiment(): {}'.format(unique_values)
            )
