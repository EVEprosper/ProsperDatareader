"""test_stocks_news.py: validate behavior for datareader.stocks.news"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

import prosper.datareader.coins.info as info
import prosper.datareader.exceptions as exceptions

def test_get_supported_symbols():
    """validate get_supported_symbols() returns valid schema"""
    data = info.get_supported_symbols()

    for symbol in data:
        helpers.validate_schema(
            symbol,
            path.join('coins', 'hitbtc_symbols.schema')
        )

class TestSupportedCommodity:
    """tests for info.supported_commodity()"""
    def test_supported_commodities_nocache(self):
        """validate supported_commodity() happypath"""
        commodity_list = info.supported_commodities(force_refresh=True)

        assert isinstance(commodity_list, list)

        expected_commodities = [
            'BCN', 'BTC', 'DASH', 'DOGE', 'DSH', 'EMC', 'ETH', 'FCN', 'LSK', 'LTC',
            'NXT', 'QCN', 'SBD', 'SC', 'STEEM', 'XDN', 'XEM', 'XMR', 'ARDR', 'ZEC',
            'WAVES', 'MAID', 'AMP', 'BUS', 'DGD', 'ICN', 'SNGLS', '1ST', 'XLC', 'TRST',
            'TIME', 'GNO', 'REP', 'ZRC', 'BOS', 'DCT', 'AEON', 'GUP', 'PLU', 'LUN',
            'TAAS', 'NXC', 'EDG', 'RLC', 'SWT', 'TKN', 'WINGS', 'XAUR', 'AE', 'PTOY',
            'WTT', 'ETC', 'CFI', 'PLBT', 'BNT', 'XDNCO', 'FYN', 'SNM', 'SNT', 'CVC',
            'PAY', 'OAX', 'OMG', 'BQX', 'XTZ', 'CRS', 'DICE', 'XRP', 'MPK', 'NET',
            'STRAT', 'SNC', 'ADX', 'BET', 'EOS', 'DENT', 'SAN', 'MNE', 'MRV', 'MSP',
            'DDF', 'UET', 'MYB', 'SUR', 'IXT', 'HRB', 'PLR', 'TIX', 'NDC', 'PRO',
            'AVT', 'TFL', 'COSS', 'PBKX', 'PQT', '8BT', 'EVX', 'IML', 'ROOTS', 'DELTA',
            'QAU', 'MANA', 'DNT', 'FYP', 'OPT', 'GRPH', 'TNT', 'STX', 'CAT', 'BCC',
            'ECAT', 'BAS', 'ZRX', 'RVT', 'ICOS', 'PPC', 'VERI', 'IGNIS', 'QTUM',
            'PRG', 'BMC', 'CND', 'ANT', 'EMGO', 'SKIN'
        ]
        assert commodity_list == expected_commodities

    #TODO: CACHE TESTS

class TestSupportedCurrencies:
    """tests for info.supported_currencies()"""
    def test_supported_currencies_nocache(self):
        """validate supported_currencies() happypath"""
        currency_list = info.supported_currencies(force_refresh=True)

        assert isinstance(currency_list, list)

        expected_currencies = ['BTC', 'EUR', 'USD', 'ETH']
        assert currency_list == expected_currencies

class TestGetSymbol:
    """tests for info.get_symbol()"""
    good_commodity = 'BTC'
    good_currency = 'USD'
    good_symbol = 'BTCUSD'

    def test_get_symbol_happypath_nocache(self):
        """validate expected behavior for get_symbol()"""
        symbol = info.get_symbol(
            self.good_commodity,
            self.good_currency,
            force_refresh=True
        )

        assert isinstance(symbol, str)
        assert symbol == self.good_symbol

    def test_get_symbol_bad_symbol(self):
        """validate exception case when bad symbol inputs requested"""
        with pytest.raises(exceptions.SymbolNotSupported):
            bad_symbol = info.get_symbol(
                'BUTTS',
                self.good_currency,
                force_refresh=True #TODO: remove
            )

        with pytest.raises(exceptions.SymbolNotSupported):
            bad_symbol = info.get_symbol(
                self.good_commodity,
                'BUTTS',
                force_refresh=True #TODO: remove
            )
