"""test_stocks_news.py: validate behavior for datareader.stocks.prices"""
from datetime import datetime
from os import path
import re

import pytest
from flaky import flaky
import requests
import helpers
import pandas as pd
import numpy

import prosper.datareader.stocks.prices as prices
import prosper.datareader.exceptions as exceptions
import prosper.datareader.config as config

class TestExpectedSchemas:
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    markets_url = helpers.CONFIG.get('STOCKS', 'markets_url')
    ticker_list = helpers.CONFIG.get('STOCKS', 'ticker_list').split(',')
    instruments_url = helpers.CONFIG.get('STOCKS', 'instruments_url')
    instruments_ticker = helpers.CONFIG.get('STOCKS', 'instruments_ticker')
    today = datetime.utcnow().strftime('%Y-%m-%d')

    @flaky
    def test_validate_quotes_endpoint(self):
        """make sure /quotes endpoint works as expected"""
        for ticker in self.ticker_list:
            quote = prices.fetch_price_quotes_rh(ticker)

            helpers.validate_schema(quote, 'stocks/rh_quotes.schema')

    @flaky
    def test_validate_fundamentals_endpoint(self):
        """make sure /fundamentals endpoint works as expected"""
        for ticker in self.ticker_list:
            fundamental = prices.fetch_fundamentals_rh(ticker)

            helpers.validate_schema(fundamental, 'stocks/rh_fundamentals.schema')

    @flaky
    def test_validate_instruments_rh(self):
        """make sure /instruments endpoint works as expected"""
        instrument = prices.fetch_instruments_rh(self.instruments_url)

        helpers.validate_schema(instrument, 'stocks/rh_instruments.schema')

        assert instrument['symbol'] == self.instruments_ticker

    @flaky
    def test_validate_market_info(self):
        """make sure /markets endpoint works as expected"""
        market_req = requests.get(self.markets_url)
        market_req.raise_for_status()

        market = market_req.json()

        helpers.validate_schema(market, 'stocks/rh_markets.schema')

    @flaky
    def test_validate_market_hours(self):
        """make sure /markets/hours works as expected"""
        url = '{markets_url}hours/{today}'.format(
            markets_url=self.markets_url,
            today=self.today)

        hours_req = requests.get(url)
        hours_req.raise_for_status()

        hours = hours_req.json()

        helpers.validate_schema(hours, 'stocks/rh_markets_hours.schema')

def test_ticker_list_to_str():
    """make sure ticker_list_to_str returns as expected"""
    no_caps_pattern = re.compile('[a-z]+')

    single_stock = config._list_to_str('MU')
    assert not no_caps_pattern.match(single_stock)
    assert single_stock == 'MU'

    lower_stock = config._list_to_str('mu')
    assert not no_caps_pattern.match(lower_stock)
    assert lower_stock == 'MU'

    multi_stock = config._list_to_str(['MU', 'INTC', 'BA'])
    assert not no_caps_pattern.match(multi_stock)
    assert multi_stock == 'MU,INTC,BA'

    lower_multi_stock = config._list_to_str(['MU', 'intc', 'BA'])
    assert not no_caps_pattern.match(lower_multi_stock)
    assert lower_multi_stock == 'MU,INTC,BA'

    with pytest.raises(TypeError):
        bad_stock = config._list_to_str({'butts':1})

def test_cast_str_to_int():
    """validate behavior for cast_str_to_int"""
    demo_json = [
        {
            "string_value": "butts",
            "int_value": "12",
            "float_value": "10.50"
        },
        {
            "string_value": "otherbutts",
            "int_value": "-99",
            "float_value": "-5.00"
        }
    ]

    demo_df = pd.DataFrame(demo_json)
    assert demo_df['string_value'].dtype == object
    assert demo_df['int_value'].dtype == object
    assert demo_df['float_value'].dtype == object

    with pytest.raises(TypeError):
        demo_df['diff'] = demo_df['int_value'] - demo_df['float_value']

    updated_df = prices.cast_str_to_int(demo_df)

    assert updated_df['string_value'].dtype == object
    assert updated_df['int_value'].dtype == numpy.int64
    assert updated_df['float_value'].dtype == numpy.float64

    updated_df['diff'] = updated_df['int_value'] - updated_df['float_value']
    assert updated_df['diff'].dtype == numpy.float64

class TestGetQuoteRH:
    """validate behavior for prices.get_quote_rh()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    ticker_list = helpers.CONFIG.get('STOCKS', 'ticker_list').split(',')

    @flaky
    def test_get_quote_rh_default(self):
        """validate expected default behavior for get_quote_rh()"""
        single_quote = prices.get_quote_rh(self.good_ticker)

        assert isinstance(single_quote, pd.DataFrame)
        assert len(single_quote) == 1

        assert set(list(single_quote.columns.values)) == set(prices.SUMMARY_KEYS)

    @flaky
    def test_get_quote_rh_multi(self):
        """validate expected behavior with list of stocks"""
        multi_quote = prices.get_quote_rh(self.ticker_list)

        assert isinstance(multi_quote, pd.DataFrame)
        assert len(multi_quote) == len(self.ticker_list)

        assert set(list(multi_quote.columns.values)) == set(prices.SUMMARY_KEYS)

    @flaky
    def test_get_quote_rh_no_filter(self):
        """look at all possible summary keys"""
        no_filter = prices.get_quote_rh(self.good_ticker, keys=None)

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
