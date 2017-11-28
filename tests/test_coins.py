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

class TestGetQuoteCC:
    """validate get_quote_cc behavior"""
    coin_list = ['BTC', 'ETH', 'DOGE']

    def test_get_quote_cc_happypath(self):
        """validate expected behavior"""
        data = coins.get_quote_cc(self.coin_list)
        print(data.columns.values)
        expected_columns = [
            'CHANGE24HOUR', 'CHANGEPCT24HOUR', 'FLAGS', 'FROMSYMBOL', 'HIGH24HOUR',
            'LASTMARKET', 'LASTTRADEID', 'LASTUPDATE', 'LASTVOLUME', 'LASTVOLUMETO',
            'LOW24HOUR', 'MARKET', 'MKTCAP', 'OPEN24HOUR', 'PRICE', 'SUPPLY', 'TICKER',
            'TOSYMBOL', 'TYPE', 'VOLUME24HOUR', 'VOLUME24HOURTO', 'Algorithm', 'CoinName',
            'FullName', 'FullyPremined', 'Id', 'ImageUrl', 'Name', 'PreMinedValue',
            'ProofType', 'SortOrder', 'TotalCoinSupply', 'TotalCoinsFreeFloat', 'Url', 'Sponsored',
            'HIGHDAY', 'TOTALVOLUME24H', 'VOLUMEDAYTO', 'Symbol', 'OPENDAY', 'TOTALVOLUME24HTO',
            'VOLUMEDAY', 'CHANGEDAY', 'CHANGEPCTDAY', 'LOWDAY'
        ]
        unique_values, unique_expected = helpers.find_uniques(
            list(data.columns.values),
            expected_columns
        )

        assert unique_expected == []

        if unique_values:
            pytest.xfail('Unexpected values from get_quote_cc(): {}'.format(unique_values))

class TestSupportedSymbolInfo:
    """validate supported_symbol_info() behavior"""
    def test_supported_commodities(self):
        """validate commoddity list"""
        commodity_list = coins.supported_symbol_info('commodity')

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
        currency_list = coins.supported_symbol_info('currency')

        assert isinstance(currency_list, list)

        expected_currencies = ['BTC', 'USD', 'ETH']
        assert currency_list == expected_currencies

    def test_supported_symbols(self):
        """validate symbols list"""
        symbols_list = coins.supported_symbol_info('symbol')

        assert isinstance(symbols_list, list)

        #TODO: validate values?

    def test_supported_symbol_info_switching(self):
        """make sure source-switching works"""
        symbols_list = coins.supported_symbol_info(
            'CoinName',
            coins.Sources.cc
        )
        assert isinstance(symbols_list, list)

        assert 'Bitcoin' in symbols_list
        #assert 'Ethereum ' in symbols_list

    def test_supported_symbol_info_strswitch(self):
        """check source-switching with str"""
        symbols_list = coins.supported_symbol_info(
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
        symbol = coins.get_symbol_hitbtc(self.good_commodity, self.good_currency)

        assert isinstance(symbol, str)
        assert symbol == self.good_symbol

    def test_get_symbol_bad_symbol(self):
        """validate exception case when bad symbol inputs requested"""
        with pytest.raises(exceptions.SymbolNotSupported):
            bad_symbol = coins.get_symbol_hitbtc('BUTTS', self.good_currency)

        with pytest.raises(exceptions.SymbolNotSupported):
            bad_symbol = coins.get_symbol_hitbtc(self.good_commodity, 'BUTTS')

class TestGetOHLCCC:
    """validate behavior for get_ohlc_cc()"""
    coin = 'BTC'
    limit = 60
    max_limit = 2001
    expected_headers = [
        'high', 'open', 'time', 'volumefrom', 'low', 'close', 'volumeto', 'datetime'
    ]

    def test_get_ohlc_cc_happypath(self):
        """validate expected default behavor for endpoint"""
        data = coins.get_ohlc_cc(
            self.coin,
            self.limit
        )

        assert isinstance(data, pandas.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(data.columns.values),
            self.expected_headers
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from get_ohlc_cc(): {}'.format(unique_values)
            )

    def test_get_ohlc_cc_maxrange(self):
        """make sure expected failure for too much data requested"""
        requested_limit = self.max_limit + 10
        data = coins.get_ohlc_cc(
            self.coin,
            requested_limit
        )
        if data.shape[0] > self.max_limit:
            pytest.xfail('Max limit unexpected.  Expected={} Requested={} Returned={}'.format(
                self.max_limit, requested_limit, data.shape[0]
            ))

    def test_get_ohlc_cc_hours(self):
        """request hours data"""
        data = coins.get_ohlc_cc(
            self.coin,
            self.limit,
            frequency='hour'
        )

        assert isinstance(data, pandas.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(data.columns.values),
            self.expected_headers
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from get_ohlc_cc(frequency=hour): {}'.format(unique_values)
            )

    def test_get_ohlc_cc_seconds(self):
        """request minute data"""
        data = coins.get_ohlc_cc(
            self.coin,
            self.limit,
            frequency='minute'
        )

        assert isinstance(data, pandas.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(data.columns.values),
            self.expected_headers
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from get_ohlc_cc(frequency=minute): {}'.format(unique_values)
            )

    def test_get_ohlc_cc_badfreq(self):
        """ask for bad frequency"""
        with pytest.raises(ValueError):
            data = coins.get_ohlc_cc(
                self.coin,
                self.limit,
                frequency='eons'
            )


class TestGetQuoteHitBTC:
    """validate get_quote_hitbtc() behavior"""
    coin_list = ['BTC', 'ETH']
    bad_list = ['BUTTS']
    expected_headers = [
        'ask', 'bid', 'high', 'last', 'low', 'open', 'symbol',
        'timestamp', 'volume', 'volume_quote', 'change_pct'
    ]

    def test_get_quote_hitbtc_happypath(self):
        """validate expected normal behavior"""
        quote = coins.get_quote_hitbtc(self.coin_list)

        assert isinstance(quote, pandas.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(quote.columns.values),
            self.expected_headers
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from get_quote_hitbtc(): {}'.format(unique_values)
            )

        assert len(quote) == len(self.coin_list)

    def test_get_quote_hitbtc_error(self):
        """validate system throws as expected"""
        with pytest.raises(KeyError):
            bad_quote = coins.get_quote_hitbtc(self.bad_list)

    def test_get_quote_hitbtc_singleton(self):
        """validate quote special case for 1 value"""
        quote = coins.get_quote_hitbtc([self.coin_list[0]])

        assert isinstance(quote, pandas.DataFrame)

        unique_values, unique_expected = helpers.find_uniques(
            list(quote.columns.values),
            self.expected_headers
        )
        assert unique_expected == []
        if unique_values:
            pytest.xfail(
                'Unexpected values from get_quote_hitbtc(): {}'.format(unique_values)
            )

        assert len(quote) == 1

class TestGetOrderbookHitBTC:
    """validate get_orderbook_hitbtc() behavior"""
    coin = 'BTC'
    expected_headers = ['price', 'ammount', 'symbol', 'coin', 'orderbook']

    def test_get_orderbook_hitbtc_happypath_asks(self):
        """validate expected normal behavior"""
        asks_orderbook = coins.get_orderbook_hitbtc(
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
        bids_orderbook = coins.get_orderbook_hitbtc(
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
            bad_book = coins.get_orderbook_hitbtc(
                self.coin,
                'butts'
            )

    def test_get_orderbook_hitbtc_bad_coin(self):
        """validate expected error for asking for bad enum"""
        with pytest.raises(KeyError):
            bad_book = coins.get_orderbook_hitbtc(
                'BUTTS',
                'asks'
            )
