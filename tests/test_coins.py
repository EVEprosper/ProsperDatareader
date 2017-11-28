"""test_coins_info.py: validate behavior for datareader.coins.info"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

import prosper.datareader.coins as coins
import prosper.datareader.exceptions as exceptions

class TestColumnsToYahoo:
    """validate expected return for columns_to_yahoo"""
    coin_list = ['BTC', 'ETH', 'LTC']
    def test_columns_to_yahoo_hitbtc(self):
        """validate columns_to_yahoo() works for hitbtc data"""
        data = coins.get_quote_hitbtc(self.coin_list, to_yahoo=False)

        updated = coins.columns_to_yahoo(data, coins.Sources.hitbtc)
        print(updated)
        expected_headers = [
            'ask', 'bid', 'high', 'last', 'low', 'open', 'symbol', 'timestamp',
            'volume', 'volume_quote', 'change_pct', 'datetime'
        ]
        unique_values, unique_expected = helpers.find_uniques(
            list(updated.columns.values),
            expected_headers
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from columns_to_yahoo(): {}'.format(unique_values)
            )

        ## assert %change done correctly
        ## assert cols not_na

    def test_columns_to_yahoo_cc(self):
        """validate column_to_yahoo() works for cryptocompare"""
        data = coins.get_quote_cc(self.coin_list, to_yahoo=False)
        updated = coins.columns_to_yahoo(data, coins.Sources.cc)
        print(updated)
        expected_headers = [
            'change_pct', 'high', 'volume', 'low', 'stock_exchange',
            'market_capitalization', 'open', 'last', 'name', 'more_info', 'symbol',
            'shares_outstanding', 'float_shares', 'datetime', 'timestamp'
        ]
        unique_values, unique_expected = helpers.find_uniques(
            list(updated.columns.values),
            expected_headers
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from columns_to_yahoo(): {}'.format(unique_values)
            )

        ## assert %change done correctly
        ## assert cols not_na
