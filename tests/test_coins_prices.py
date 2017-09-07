"""test_coins_prices.py: validate behavior for datareader.coins.prices"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

import prosper.datareader.coins.prices as prices
import prosper.datareader.exceptions as exceptions

def test_listify():
    """validate expected behavior for _listify()"""
    demo_data = {
        'key1': {
            'val1': 1,
            'val2': 2
        },
        'key2': {
            'val1': 10,
            'val2': 20
        }
    }
    fixed_data = prices._listify(demo_data, 'key')
    assert isinstance(fixed_data, list)
    expected_keys = ['val1', 'val2', 'key']
    expected_keys.sort()
    for row in fixed_data:
        keys = list(row.keys())
        keys.sort()
        assert keys == expected_keys

def test_get_ticker_single():
    """validate get_ticker_hitbtc() returns valid schema"""
    data = prices.get_ticker_hitbtc('BTCUSD')

    assert isinstance(data, dict)
    helpers.validate_schema(
        data,
        path.join('coins', 'hitbtc_ticker.schema')
    )

    with pytest.raises(requests.exceptions.HTTPError):
        bad_data = prices.get_ticker_hitbtc('BUTTS')

def test_get_ticker_all():
    """validate get_ticker() behavior with blank args"""
    data = prices.get_ticker_hitbtc('')

    assert isinstance(data, list)
    helpers.validate_schema(
        data[0],
        path.join('coins', 'hitbtc_ticker.schema')
    )
    assert len(data) >= 190 * 0.9 #expect ~same data or more

def test_get_orderbook():
    """validate get_order_book_hitbtc() returns valid schema"""
    data = prices.get_order_book_hitbtc('BTCUSD')

    assert isinstance(data, dict)
    assert isinstance(data['asks'], list)
    assert isinstance(data['bids'], list)

def test_coin_list_to_ticker_list():
    """validate coin_list_to_ticker_list() works as expected"""
    test_coin_list = ['BTC', 'ETH']

    ticker_list = prices.coin_list_to_ticker_list(test_coin_list)

    expected_tickers = ['BTCUSD', 'ETHUSD']
    assert isinstance(ticker_list, list)
    assert ticker_list == expected_tickers

    with pytest.raises(KeyError):
        bad_ticker = prices.coin_list_to_ticker_list(['BUTTS'], strict=True)

class TestGetQuoteHitBTC:
    """validate get_quote_hitbtc() behavior"""
    coin_list = ['BTC', 'ETH']
    bad_list = ['BUTTS']
    expected_headers = [
        'ask', 'bid', 'high', 'last', 'low', 'open', 'symbol',
        'timestamp', 'volume', 'volume_quote'
    ]

    def test_get_quote_hitbtc_happypath(self):
        """validate expected normal behavior"""
        quote = prices.get_quote_hitbtc(self.coin_list)

        assert isinstance(quote, pandas.DataFrame)

        print(list(quote.columns.values))
        assert list(quote.columns.values) == self.expected_headers
        assert len(quote) == len(self.coin_list)

    def test_get_quote_hitbtc_error(self):
        """validate system throws as expected"""
        with pytest.raises(KeyError):
            bad_quote = prices.get_quote_hitbtc(self.bad_list)

    def test_get_quote_hitbtc_singleton(self):
        """validate quote special case for 1 value"""
        quote = prices.get_quote_hitbtc([self.coin_list[0]])

        assert isinstance(quote, pandas.DataFrame)

        print(list(quote.columns.values))
        assert list(quote.columns.values) == self.expected_headers
        assert len(quote) == 1
