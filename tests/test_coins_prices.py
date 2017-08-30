"""test_coins_prices.py: validate behavior for datareader.coins.prices"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

import prosper.datareader.coins.prices as prices
import prosper.datareader.exceptions as exceptions

def test_get_ticker():
    """validate get_ticker() returns valid schema"""
    data = prices.get_ticker('BTCUSD')

    helpers.validate_schema(
        data,
        path.join('coins', 'hitbtc_ticker.schema')
    )

    with pytest.raises(requests.exceptions.HTTPError):
        bad_data = prices.get_ticker('BUTTS')
