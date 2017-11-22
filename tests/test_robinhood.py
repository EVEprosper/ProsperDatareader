"""validate prosper.datareader.robinhood utilities"""
from datetime import datetime
from os import path

import pytest
from flaky import flaky
import requests
import helpers

import prosper.datareader.robinhood as robinhood
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
            quote = robinhood.quotes.fetch_price_quotes_rh(ticker)

            helpers.validate_schema(quote, 'stocks/rh_quotes.schema')

    def test_validate_fundamentals_endpoint(self):
        """make sure /fundamentals endpoint works as expected"""
        for ticker in self.ticker_list:
            fundamental = robinhood.quotes.fetch_fundamentals_rh(ticker)

            helpers.validate_schema(fundamental, 'stocks/rh_fundamentals.schema')

    def test_validate_instruments_rh(self):
        """make sure /instruments endpoint works as expected"""
        instrument = robinhood.quotes.fetch_instruments_rh(self.instruments_url)

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

class TestFetchCompanyNewsRobinhood:
    """validate behavior for news.fetch_company_news_rh()"""
    good_ticker = helpers.CONFIG.get('STOCKS', 'good_ticker')
    bad_ticker = helpers.CONFIG.get('STOCKS', 'bad_ticker')
    expected_news_cols = [
        'api_source', 'author', 'instrument', 'num_clicks', 'preview_image_url',
        'published_at', 'relay_url', 'source', 'summary', 'title', 'updated_at',
        'url', 'uuid', 'preview_image_width', 'preview_image_height'
    ]

    @pytest.mark.long
    def test_default_happypath(self):
        """validate default behavior -- minimum args"""
        news_list = robinhood.news.fetch_company_news_rh(self.good_ticker)

        assert isinstance(news_list, list)

        for article in news_list:
            assert isinstance(article, dict)
            helpers.validate_schema(
                article,
                path.join('stocks', 'rh_news.schema')
            )

    def test_default_bad_ticker(self):
        """validate behavior -- incorrect ticker"""
        #with pytest.raises(requests.exceptions.HTTPError):
        news_list = robinhood.news.fetch_company_news_rh(self.bad_ticker)

    def test_page_stop(self):
        """make sure page limit works"""
        long_news_list = robinhood.news.fetch_company_news_rh(self.good_ticker)

        short_news_list = robinhood.news.fetch_company_news_rh(
            self.good_ticker,
            page_limit=2
        )

        assert len(long_news_list) > len(short_news_list)

    def test_hard_page_stop(self):
        """make sure anti-recursion stop works as intended"""
        default_page_hardbreak = robinhood.news.PAGE_HARDBREAK
        robinhood.news.PAGE_HARDBREAK = 2

        with pytest.warns(exceptions.PaginationWarning):
            news_list = robinhood.news.fetch_company_news_rh(self.good_ticker)

        robinhood.news.PAGE_HARDBREAK = default_page_hardbreak
