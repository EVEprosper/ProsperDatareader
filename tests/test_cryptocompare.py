"""test_cryptocompare.py: validate behavior for datareader.cryptocompare"""
from datetime import datetime
from os import path

import pytest
import helpers

import prosper.datareader.exceptions as exceptions
import prosper.datareader.cryptocompare as cryptocompare

def test_get_supported_symbols_cc():
    """validate get_supported_symbols_cc() return valid schema"""
    data = cryptocompare.quotes.get_supported_symbols_cc()

    for symbol in data:
        helpers.validate_schema(
            symbol,
            path.join('coins', 'cryptocompare_coinlist.schema')
        )
class TestGetTickerCC:
    """validate get_ticker_cc() behavior"""
    coin_list = ['BTC', 'ETH', 'LTC']
    market = 'Coinbase'

    def test_get_ticker_cc_happypath(self):
        """validate expected behavior"""
        data = cryptocompare.quotes.get_ticker_cc(self.coin_list)
        assert isinstance(data, list)
        for row in data:
            helpers.validate_schema(
                row,
                path.join('coins', 'cryptocompare_pricemultifull.schema')
            )

    def test_get_ticker_cc_strs(self):
        """make sure endpoint works with str data"""
        data = cryptocompare.quotes.get_ticker_cc(self.coin_list[0])
        assert len(data) == 1
        assert data[0]['FROMSYMBOL'] == self.coin_list[0]

        data = cryptocompare.quotes.get_ticker_cc(','.join(self.coin_list))
        assert len(data) == len(self.coin_list)

    def test_get_ticker_cc_marketlist(self):
        """make sure we can switch market"""
        data = cryptocompare.quotes.get_ticker_cc(
            self.coin_list, market_list=[self.market]
        )

        print(data)
        for row in data:
            assert row['MARKET'] == self.market

    def test_get_ticker_cc_bad_coin(self):
        """validate exception throw for bad coins"""
        data = cryptocompare.quotes.get_ticker_cc('DOGE')  # works as expected
        with pytest.raises(exceptions.SymbolNotSupported):
            data = cryptocompare.quotes.get_ticker_cc('DOGE', market_list=['Coinbase'])

    def test_get_ticker_cc_bad_key(self):
        """validate exception throw for bad price key"""
        with pytest.raises(KeyError):
            data = cryptocompare.quotes.get_ticker_cc(self.coin_list, price_key='BUTTS')


class TestGetHistoDayCC:
    """validate behavior for get_histo_day_cc"""
    coin = 'BTC'
    limit = 60

    def test_get_histo_day_cc_happypath(self):
        """validate expected default behavior for endpoint"""
        data = cryptocompare.quotes.get_histo_day_cc(
            self.coin,
            self.limit
        )

        for row in data:
            helpers.validate_schema(
                row,
                path.join('coins', 'cryptocompare_histo_day.schema')
            )

    def test_get_histo_day_cc_aggregate(self):
        """validate `aggregate` path"""

        data = cryptocompare.quotes.get_histo_day_cc(
            self.coin,
            self.limit,
            aggregate=3
        )
        ## TODO VALIDATE ##

    def test_get_histo_day_cc_badcoin(self):
        """validate expected error for bad coin id"""
        with pytest.raises(exceptions.SymbolNotSupported):
            bad_data = cryptocompare.quotes.get_histo_day_cc(
                'BUTTS',
                self.limit
            )
