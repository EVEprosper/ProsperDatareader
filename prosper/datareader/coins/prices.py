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

COIN_TICKER_URI = 'http://api.hitbtc.com/api/1/public/{ticker}/ticker'
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
    req = requests.get(uri.format(ticker=symbol))
    req.raise_for_status()
    return req.json()
