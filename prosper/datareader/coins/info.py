"""datareader.coins.info.py: tools for fetching stock news"""
from datetime import datetime
import itertools
from os import path
import warnings

import requests
import pandas as pd

from prosper.datareader.config import LOGGER as G_LOGGER
import prosper.datareader.exceptions as exceptions

LOGGER = G_LOGGER
HERE = path.abspath(path.dirname(__file__))

SYMBOLS_URI = 'http://api.hitbtc.com/api/1/public/symbols'
def get_supported_symbols(
        uri=SYMBOLS_URI,
        data_key='symbols'
):
    """fetch supported symbols from API

    Note:
        Supported by hitbtc
        https://hitbtc.com/api#symbols

    Args:
        uri (str, optional): address for API
        data_key (str, optional): data key name in JSON data

    Returns:
        (:obj:`list`): list of supported feeds

    """
    req = requests.get(uri)
    req.raise_for_status()
    data = req.json()

    return data[data_key]


def supported_commodities(
        force_refresh=False,
        logger=LOGGER
):
    """list supported symbols

    Args:
        force_refresh (bool, optional): ignore local cache and fetch directly from API
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`list`): list of supported crypto coins

    """

    #TODO: check cache
    if force_refresh:
        logger.info('--Fetching symbol list from API')
        symbols_df = pd.DataFrame(get_supported_symbols())


    commodities = list(symbols_df['commodity'].unique())

    #TODO: save cache

    return commodities

def supported_currencies(
        force_refresh=False,
        logger=LOGGER
):
    """list supported currency conversions

    Args:
        force_refresh (bool, optional): ignore local cache and fetch directly from API
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`list`): list of supported currency conversions

    """
    #TODO: check cache
    if force_refresh:
        logger.info('--Fetching symbol list from API')
        symbols_df = pd.DataFrame(get_supported_symbols())


    currencies = list(symbols_df['currency'].unique())

    #TODO: save cache

    return currencies

def get_symbol(
        commodity_ticker,
        currency_ticker,
        force_refresh=False,
        logger=LOGGER
):
    """get valid ticker to look up

    Args:
        commodity_ticker (str): short-name for crypto coin
        currency_ticker (str): short-name for currency
        force_refresh (bool, optional): ignore local cacne and fetch directly from API
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (str): valid ticker for HITBTC

    """
    #TODO: check cache
    if force_refresh:
        logger.info('--Fetching symbol list from API')
        symbols_df = pd.DataFrame(get_supported_symbols())

    symbol = symbols_df.query(
        'commodity==\'{commodity}\' & currency==\'{currency}\''.format(
            commodity=commodity_ticker.upper(),
            currency=currency_ticker.upper()
        ))

    if symbol.empty:
        raise exceptions.SymbolNotSupported()

    #TODO: update cache

    return symbol['symbol'].iloc[0]

def get_ticker_info(
        ticker,
        force_refresh=False,
        logger=LOGGER
):
    """reverse lookup, get more info about a requested ticker

    Args:
        ticker (str): info ticker for coin (ex: BTCUSD)
        force_refresh (bool, optional): ignore local cacne and fetch directly from API
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`dict`): hitBTC info about requested ticker

    """
    #TODO: check cache
    if force_refresh:
        logger.info('--Fetching symbol list from API')
        data = get_supported_symbols()

    ## Skip pandas, vanilla list search ok here
    for ticker_info in data:
        if ticker_info['symbol'] == ticker.upper():
            return ticker_info

    #TODO: update cache
    raise exceptions.TickerNotFound()
