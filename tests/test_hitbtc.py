"""test_hitbtc.py: validate behavior for datareader.hitbtc"""
from datetime import datetime
from os import path

import pytest
import helpers
import requests

import prosper.datareader.exceptions as exceptions
import prosper.datareader.hitbtc as hitbtc

def test_get_supported_symbols_hitbtc():
    """validate get_supported_symbols_hitbtc() returns valid schema"""
    data = hitbtc.quotes.get_supported_symbols_hitbtc()

    for symbol in data:
        helpers.validate_schema(
            symbol,
            path.join('coins', 'hitbtc_symbols.schema')
        )


class TestGetTickerInfo:
    """tests info.get_ticker_info_hitbtc()"""
    good_symbol = 'BTCUSD'

    def test_get_ticker_info_happypath_nocache(self):
        """validate expected behavior for get_ticker_info_hitbtc()"""
        symbol_info = hitbtc.quotes.get_ticker_info_hitbtc(self.good_symbol)
        assert symbol_info['symbol'] == self.good_symbol
        assert symbol_info['currency'] == 'USD'

    def test_get_ticker_info_bad_symbol(self):
        """validate exception case when bad symbol inputs requested"""
        with pytest.raises(exceptions.TickerNotFound):
            bad_symbol = hitbtc.quotes.get_ticker_info_hitbtc('BUTTS')

def test_get_ticker_single():
    """validate get_ticker_hitbtc() returns valid schema"""
    data = hitbtc.quotes.get_ticker_hitbtc('BTCUSD')

    assert isinstance(data, dict)
    helpers.validate_schema(
        data,
        path.join('coins', 'hitbtc_ticker.schema')
    )

    with pytest.raises(requests.exceptions.HTTPError):
        bad_data = hitbtc.quotes.get_ticker_hitbtc('BUTTS')

def test_get_ticker_all():
    """validate get_ticker() behavior with blank args"""
    data = hitbtc.quotes.get_ticker_hitbtc('')

    assert isinstance(data, list)
    print(data[0])
    helpers.validate_schema(
        data[0],
        path.join('coins', 'hitbtc_ticker.schema')
    )
    assert len(data) >= 190 * 0.9 #expect ~same data or more

def test_coin_list_to_symbol_list():
    """validate coin_list_to_symbol_list() works as expected"""
    test_coin_list = ['BTC', 'ETH']

    ticker_list = hitbtc.quotes.coin_list_to_symbol_list(test_coin_list, currency='USD')

    expected_tickers = ['BTCUSD', 'ETHUSD']
    assert isinstance(ticker_list, list)
    assert ticker_list == expected_tickers

    with pytest.raises(KeyError):
        bad_ticker = hitbtc.quotes.coin_list_to_symbol_list(['BUTTS'], strict=True)

def test_get_orderbook():
    """validate get_order_book_hitbtc() returns valid schema"""
    data = hitbtc.quotes.get_order_book_hitbtc('BTCUSD')

    assert isinstance(data, dict)
    assert isinstance(data['asks'], list)
    assert isinstance(data['bids'], list)
