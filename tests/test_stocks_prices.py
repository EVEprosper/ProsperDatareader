"""test_stocks_news.py: validate behavior for datareader.stocks.prices"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers

import prosper.datareader.stocks.prices as prices
import prosper.datareader.exceptions as exceptions

class TestExpectedSchemas:
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    markets_url = helpers.CONFIG.get('STOCKS', 'markets_url')
    ticker_list = helpers.CONFIG.get('STOCKS', 'ticker_list').split(',')
    instruments_url = helpers.CONFIG.get('STOCKS', 'instruments_url')
    instruments_ticker = helpers.CONFIG.get('STOCKS', 'instruments_ticker')
    today = datetime.utcnow().strftime('%Y-%m-%d')

    def test_validate_quotes_endpoint(self):
        """make sure /quotes endpoint works as expected"""
        for ticker in self.ticker_list:
            quote = prices.fetch_price_quotes_rh(ticker)

            helpers.validate_schema(quote, 'stocks/rh_quotes.schema')

    def test_validate_fundamentals_endpoint(self):
        """make sure /fundamentals endpoint works as expected"""
        for ticker in self.ticker_list:
            fundamental = prices.fetch_fundamentals_rh(ticker)

            helpers.validate_schema(fundamental, 'stocks/rh_fundamentals.schema')

    def test_validate_instruments_rh(self):
        """make sure /instruments endpoint works as expected"""
        instrument = prices.fetch_instruments_rh(self.instruments_url)

        helpers.validate_schema(instrument, 'stocks/rh_instruments.schema')

        assert instrument['symbol'] == self.instruments_ticker

    def test_validate_market_info(self):
        """make sure /markets endpoint works as expected"""
        market_req = requests.get(self.markets_url)
        market_req.raise_for_status()

        market = market_req.json()

        helpers.validate_schema(market, 'stocks/rh_markets.schema')

    def test_validate_market_hours(self):
        """make sure /markets/hours works as expected"""
        url = '{markets_url}hours/{today}'.format(
            markets_url=self.markets_url,
            today=self.today)

        hours_req = requests.get(url)
        hours_req.raise_for_status()

        hours = hours_req.json()

        helpers.validate_schema(hours, 'stocks/rh_markets_hours.schema')
