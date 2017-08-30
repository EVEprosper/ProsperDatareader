"""test_coins_prices.py: validate behavior for datareader.coins.prices"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas

import prosper.datareader.coins.prices as prices
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
    for row in fixed_data:
        assert list(row.keys()) == expected_keys

def test_get_ticker_single():
    """validate get_ticker() returns valid schema"""
    data = prices.get_ticker('BTCUSD')

    assert isinstance(data, dict)
    helpers.validate_schema(
        data,
        path.join('coins', 'hitbtc_ticker.schema')
    )

    with pytest.raises(requests.exceptions.HTTPError):
        bad_data = prices.get_ticker('BUTTS')

def test_get_ticker_all():
    """validate get_ticker() behavior with blank args"""
    data = prices.get_ticker('')

    assert isinstance(data, list)
    helpers.validate_schema(
        data[0],
        path.join('coins', 'hitbtc_ticker.schema')
    )
    assert len(data) >= 190 * 0.9 #expect ~same data or more
