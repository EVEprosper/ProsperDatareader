"""test prosper.datareader.stocks top-level functions"""
from os import path

import pytest
import helpers
import pandas as pd
from flaky import flaky

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
            'updated_at', 'url', 'volume', 'year_founded', 'change_pct', 'shares_outstanding',
            'sector', 'average_volume_2_weeks', 'tradable_chain_id',
        ]
        assert set(list(no_filter.columns.values)) == set(all_keys)
