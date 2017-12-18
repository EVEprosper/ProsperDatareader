"""test_coins_info.py: validate behavior for datareader.coins.info"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

import prosper.datareader.coins.info as info
import prosper.datareader.exceptions as exceptions

def test_get_supported_symbols_hitbtc():
    """validate get_supported_symbols_hitbtc() returns valid schema"""
    data = info.get_supported_symbols_hitbtc()

    for symbol in data:
        helpers.validate_schema(
            symbol,
            path.join('coins', 'hitbtc_symbols.schema')
        )
def test_get_supported_symbols_cc():
    """validate get_supported_symbols_cc() return valid schema"""
    data = info.get_supported_symbols_cc()

    for symbol in data:
        helpers.validate_schema(
            symbol,
            path.join('coins', 'cryptocompare_coinlist.schema')
        )

class TestSupportedSymbolInfo:
    """validate supported_symbol_info() behavior"""
    def test_supported_commodities(self):
        """validate commoddity list"""
        commodity_list = info.supported_symbol_info('commodity')

        assert isinstance(commodity_list, list)

        expected_commodities = [
            'BCN', 'BTC', 'DASH', 'DOGE', 'DSH', 'EMC', 'ETH', 'FCN', 'LSK', 'LTC',
        ]
        unique_values, unique_expected = helpers.find_uniques(
            commodity_list,
            expected_commodities
        )

        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from supported_symbol_info(): {}'.format(unique_values))

    def test_supported_currencies(self):
        """validate currency list"""
        currency_list = info.supported_symbol_info('currency')

        assert isinstance(currency_list, list)

        expected_currencies = ['BTC', 'USD', 'ETH']
        assert currency_list == expected_currencies

    def test_supported_symbols(self):
        """validate symbols list"""
        symbols_list = info.supported_symbol_info('symbol')

        assert isinstance(symbols_list, list)

        #TODO: validate values?

    def test_supported_symbol_info_switching(self):
        """make sure source-switching works"""
        symbols_list = info.supported_symbol_info(
            'CoinName',
            info.Sources.cc
        )
        assert isinstance(symbols_list, list)

        assert 'Bitcoin' in symbols_list
        #assert 'Ethereum ' in symbols_list

    def test_supported_symbol_info_strswitch(self):
        """check source-switching with str"""
        symbols_list = info.supported_symbol_info(
            'CoinName',
            'cryptocompare'
        )

        assert isinstance(symbols_list, list)


class TestGetSymbolHitBTC:
    """tests for info.get_symbol()"""
    good_commodity = 'BTC'
    good_currency = 'USD'
    good_symbol = 'BTCUSD'

    def test_get_symbol_happypath(self):
        """validate expected behavior for get_symbol()"""
        symbol = info.get_symbol_hitbtc(self.good_commodity, self.good_currency)

        assert isinstance(symbol, str)
        assert symbol == self.good_symbol

    def test_get_symbol_bad_symbol(self):
        """validate exception case when bad symbol inputs requested"""
        with pytest.raises(exceptions.SymbolNotSupported):
            bad_symbol = info.get_symbol_hitbtc('BUTTS', self.good_currency)

        with pytest.raises(exceptions.SymbolNotSupported):
            bad_symbol = info.get_symbol_hitbtc(self.good_commodity, 'BUTTS')

class TestGetTickerInfo:
    """tests info.get_ticker_info()"""
    good_symbol = 'BTCUSD'

    def test_get_ticker_info_happypath_nocache(self):
        """validate expected behavior for get_ticker_info()"""
        symbol_info = info.get_ticker_info(self.good_symbol)
        assert symbol_info['symbol'] == self.good_symbol
        assert symbol_info['currency'] == 'USD'

    def test_get_ticker_info_bad_symbol(self):
        """validate exception case when bad symbol inputs requested"""
        with pytest.raises(exceptions.TickerNotFound):
            bad_symbol = info.get_ticker_info('BUTTS')
