"""datareader.coins.prices.py: tools for fetching cryptocoin price data"""
from datetime import datetime
import itertools
from os import path

import requests
import pandas as pd

from prosper.datareader.config import LOGGER as G_LOGGER
import prosper.datareader.exceptions as exceptions

LOGGER = G_LOGGER
HERE = path.abspath(path.dirname(__file__))

def _listify(
        data,
        key_name
):
    """recast data from dict to list, compress keys into sub-dict

    Args:
        data (:obj:`dict`): data to transform (dict(dict))
        key_name (str): name to recast key to

    Returns:
        (:obj:`list`): fixed data

    """
    listified_data = []
    for key, value in data.items():
        row = dict(value)
        row[key_name] = key
        listified_data.append(row)

    return listified_data

COIN_TICKER_URI = 'http://api.hitbtc.com/api/1/public/{symbol}/ticker'
def get_ticker(
        symbol,
        uri=COIN_TICKER_URI
):
    """fetch quote for coin

    Notes:
        incurs a .format(ticker=symbol) call, be careful with overriding uri

    Args:
        symbol (str): name of coin-ticker to pull
        uri (str, optional): resource link

    Returns:
        (:obj:`dict`): ticker data for desired coin

    """
    full_uri = ''
    if not symbol:
        full_uri = uri.replace(r'{symbol}/', '')
    else:
        full_uri = uri.format(symbol=symbol)

    req = requests.get(full_uri)
    req.raise_for_status()

    data = req.json()
    if not symbol:
        data = _listify(data, 'symbol')

    return data
