"""test_coins_prices.py: validate behavior for datareader.coins.prices"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

import prosper.datareader.coins.prices as prices
import prosper.datareader.coins.info as info
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


class TestGetTickerCC:
    """validate get_ticker_cc() behavior"""
    coin_list = ['BTC', 'ETH', 'DOGE']
    def test_get_ticker_cc_happypath(self):
        """validate expected behavior"""
        data = prices.get_ticker_cc(self.coin_list)
        print(data)
        assert isinstance(data, list)
        for row in data:
            helpers.validate_schema(
                row,
                path.join('coins', 'cryptocompare_pricemultifull.schema')
            )

class TestGetQuoteCC:
    """validate get_quote_cc behavior"""
    coin_list = ['BTC', 'ETH', 'DOGE']
    def test_get_quote_cc_happypath(self):
        """validate expected behavior"""
        data = prices.get_quote_cc(self.coin_list)
        print(data)
        assert False

class TestColumnsToYahoo:
    """validate expected return for columns_to_yahoo"""
    def test_columns_to_yahoo_hitbtc(self):
        """validate columns_to_yahoo() works for hitbtc data"""
        data = pandas.DataFrame(info.get_supported_symbols_hitbtc())
        print(data)
        updated = prices.columns_to_yahoo(data, info.Sources.hitbtc)
        assert False

    def test_columns_to_yahoo_cc(self):
        """validate column_to_yahoo() works for cryptocompare"""
        data = pandas.DataFrame(info.get_supported_symbols_cc())
        print(data)
        updated = prices.columns_to_yahoo(data, info.Sources.cc)
        assert False

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

def test_coin_list_to_symbol_list():
    """validate coin_list_to_symbol_list() works as expected"""
    test_coin_list = ['BTC', 'ETH']

    ticker_list = prices.coin_list_to_symbol_list(test_coin_list, currency='USD')

    expected_tickers = ['BTCUSD', 'ETHUSD']
    assert isinstance(ticker_list, list)
    assert ticker_list == expected_tickers

    with pytest.raises(KeyError):
        bad_ticker = prices.coin_list_to_symbol_list(['BUTTS'], strict=True)

class TestGetQuoteHitBTC:
    """validate get_quote_hitbtc() behavior"""
    coin_list = ['BTC', 'ETH']
    bad_list = ['BUTTS']
    expected_headers = [
        'ask', 'bid', 'high', 'last', 'low', 'open', 'symbol',
        'timestamp', 'volume', 'volume_quote', 'pct_change'
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

class TestGetOrderbookHitBTC:
    """validate get_orderbook_hitbtc() behavior"""
    coin = 'BTC'
    expected_headers = ['price', 'ammount', 'symbol', 'coin', 'orderbook']

    def test_get_orderbook_hitbtc_happypath_asks(self):
        """validate expected normal behavior"""
        asks_orderbook = prices.get_orderbook_hitbtc(
            self.coin,
            'asks',
            currency='USD'
        )

        assert isinstance(asks_orderbook, pandas.DataFrame)
        print(list(asks_orderbook.columns.values))
        assert list(asks_orderbook.columns.values) == self.expected_headers

        orderbook = asks_orderbook['orderbook'].unique()
        assert len(orderbook) == 1
        assert orderbook[0] == 'asks'

        coin = asks_orderbook['coin'].unique()
        assert len(coin) == 1
        assert coin[0] == self.coin

        symbol = asks_orderbook['symbol'].unique()
        assert len(symbol) == 1
        assert symbol[0] == self.coin + 'USD'

    def test_get_orderbook_hitbtc_happypath_bids(self):
        """validate expected normal behavior"""
        bids_orderbook = prices.get_orderbook_hitbtc(
            self.coin,
            'bids',
            currency='USD'
        )

        assert isinstance(bids_orderbook, pandas.DataFrame)
        print(list(bids_orderbook.columns.values))
        assert list(bids_orderbook.columns.values) == self.expected_headers

        orderbook = bids_orderbook['orderbook'].unique()
        assert len(orderbook) == 1
        assert orderbook[0] == 'bids'

        coin = bids_orderbook['coin'].unique()
        assert len(coin) == 1
        assert coin[0] == self.coin

        symbol = bids_orderbook['symbol'].unique()
        assert len(symbol) == 1
        assert symbol[0] == self.coin + 'USD'

    def test_get_orderbook_hitbtc_bad_book(self):
        """validate expected error for asking for bad enum"""
        with pytest.raises(ValueError):
            bad_book = prices.get_orderbook_hitbtc(
                self.coin,
                'butts'
            )

    def test_get_orderbook_hitbtc_bad_coin(self):
        """validate expected error for asking for bad enum"""
        with pytest.raises(KeyError):
            bad_book = prices.get_orderbook_hitbtc(
                'BUTTS',
                'asks'
            )
