from os import path

import pytest
import helpers
import pandas as pd

import prosper.datareader.stocks as stocks

class TestGetQuoteRH:
    """validate behavior for prices.get_quote_rh()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    ticker_list = helpers.CONFIG.get('STOCKS', 'ticker_list').split(',')

    def test_get_quote_rh_default(self):
        """validate expected default behavior for get_quote_rh()"""
        single_quote = stocks.get_quote_rh(self.good_ticker)

        assert isinstance(single_quote, pd.DataFrame)
        assert len(single_quote) == 1

        assert set(list(single_quote.columns.values)) == set(stocks.SUMMARY_KEYS)

    def test_get_quote_rh_multi(self):
        """validate expected behavior with list of stocks"""
        multi_quote = stocks.get_quote_rh(self.ticker_list)

        assert isinstance(multi_quote, pd.DataFrame)
        assert len(multi_quote) == len(self.ticker_list)

        assert set(list(multi_quote.columns.values)) == set(stocks.SUMMARY_KEYS)

    def test_get_quote_rh_no_filter(self):
        """look at all possible summary keys"""
        no_filter = stocks.get_quote_rh(self.good_ticker, keys=None)

        assert isinstance(no_filter, pd.DataFrame)
        assert len(no_filter) == 1

        all_keys = [
            'adjusted_previous_close', 'ask_price', 'ask_size', 'average_volume',
            'bid_price', 'bid_size', 'bloomberg_unique', 'ceo', 'country',
            'current_price', 'day_trade_ratio', 'description', 'dividend_yield',
            'fundamentals', 'has_traded', 'headquarters_city', 'headquarters_state',
            'high', 'high_52_weeks', 'id', 'instrument', 'is_open',
            'last_extended_hours_trade_price', 'last_trade_price',
            'last_trade_price_source', 'list_date', 'low', 'low_52_weeks',
            'maintenance_ratio', 'margin_initial_ratio', 'market', 'market_cap',
            'min_tick_size', 'name', 'num_employees', 'open', 'pe_ratio',
            'previous_close', 'previous_close_date', 'quote', 'simple_name',
            'splits', 'state', 'symbol', 'tradeable', 'tradability', 'trading_halted', 'type',
            'updated_at', 'url', 'volume', 'year_founded', 'change_pct'
        ]
        assert set(list(no_filter.columns.values)) == set(all_keys)

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
        all_news_df = stocks.company_news_rh(self.good_ticker)

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
        all_news_df = stocks.company_news_rh(self.good_ticker)

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

class TestMarketNewsGoogle:
    """valdiate behavior on stocks.market_news_google()"""
    @pytest.mark.long
    def test_market_news_google_happypath(self):
        """validate default behavior"""
        all_news_df = stocks.market_news_google()

        assert isinstance(all_news_df, pd.DataFrame)

        expected_cols = [
            'age', 'primary', 'source', 'blurb',
            'sru', 'title', 'datetime', 'url', 'usg'
        ]

        assert list(all_news_df.columns.values) == expected_cols

    def test_market_news_google_no_pretty(self):
        """validate not-pretty return works as expected"""
        all_news_df = stocks.market_news_google(pretty=False)

        assert isinstance(all_news_df, pd.DataFrame)

        expected_cols = [
            'd', 'primary', 's', 'sp', 'sru', 't', 'tt', 'u', 'usg'
        ]

        assert list(all_news_df.columns.values) == expected_cols


class TestCompanyNewsGoogle:
    """validate behavior for stocks.company_news_google()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')

    def test_company_news_happypath(self):
        """make sure pandas wrapper works as expected"""
        all_news_df = stocks.company_news_google(self.good_ticker)

        assert isinstance(all_news_df, pd.DataFrame)

        expected_cols = [
            'age', 'primary', 'source', 'blurb',
            'sru', 'title', 'datetime', 'url', 'usg'
        ]

        unique_values, unique_expected = helpers.find_uniques(
            list(all_news_df.columns.values),
            expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail('Unexpected values from company_news_google(): {}'.format(unique_values))

    def test_company_news_no_pretty(self):
        """validate not-pretty return works as expected"""
        all_news_df = stocks.company_news_google(
            self.good_ticker,
            pretty=False
        )

        assert isinstance(all_news_df, pd.DataFrame)

        expected_cols = [
            'd', 'primary', 's', 'sp', 'sru', 't', 'tt', 'u', 'usg'
        ]
        unique_values, unique_expected = helpers.find_uniques(
            list(all_news_df.columns.values),
            expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail('Unexpected values from company_news_google(): {}'.format(unique_values))

    @pytest.mark.long
    def test_vader_application(self):
        """make sure use-case for news + vader works"""
        import prosper.datareader.utils as utils
        all_news_df = stocks.company_news_google(self.good_ticker)

        graded_news = utils.vader_sentiment(all_news_df, 'title')

        expected_cols = [
            'age', 'primary', 'source', 'blurb',
            'sru', 'title', 'datetime', 'url', 'usg',
            'neu', 'pos', 'compound', 'neg'
        ]

        unique_values, unique_expected = helpers.find_uniques(
            list(graded_news.columns.values),
            expected_cols
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail('Unexpected values from company_news_google(): {}'.format(unique_values))
