"""datareader.coins.prices.py: tools for fetching cryptocoin price data"""
from datetime import datetime
from os import path
from enum import Enum

import requests
import pandas as pd

import prosper.datareader.config as config
import prosper.datareader.exceptions as exceptions
import prosper.datareader.coins.info as info

LOGGER = config.LOGGER
HERE = path.abspath(path.dirname(__file__))

class OrderBook(Enum):
    """enumerator for handling order book info"""
    asks = 'asks'
    bids = 'bids'

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

def coin_list_to_ticker_list(
        coin_list,
        currency='USD',
        strict=False
):
    """convert list of crypto currencies to HitBTC tickers

    Args:
        coin_list (str or :obj:`list`): list of coins to convert
        currency (str, optional): currency to FOREX against
        strict (bool, optional): throw if unsupported ticker is requested

    Returns:
        (:obj:`list`): list of valid coins and tickers

    """
    valid_ticker_list = info.supported_symbol_info('symbol')

    ticker_list = []
    invalid_tickers = []
    for coin in coin_list:
        ticker = str(coin) + currency
        if ticker not in valid_ticker_list:
            invalid_tickers.append(ticker)

        ticker_list.append(ticker)

    if invalid_tickers and strict:
        raise KeyError('Unsupported ticker requested: {}'.format(invalid_tickers))

    return ticker_list

COIN_TICKER_URI = 'http://api.hitbtc.com/api/1/public/{symbol}/ticker'
def get_ticker_hitbtc(
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
        (:obj:`dict`) or (:obj:`list`): ticker data for desired coin

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

COIN_ORDER_BOOK_URI = 'http://api.hitbtc.com/api/1/public/{symbol}/orderbook'
def get_order_book_hitbtc(
        symbol,
        format_price='number',
        format_amount='number',
        uri=COIN_ORDER_BOOK_URI
):
    """fetch orderbook data

    Notes:
        incurs a .format(ticker=symbol) call, be careful with overriding uri

    Args:
        symbol (str): name of coin-ticker to pull
        format_price (str, optional): optional format helper
        format_amount (str, optional): optional format helper
        uri (str, optional): resource link

    Returns:
        (:obj:`dict`): order book for coin-ticker

    """
    params = {}
    #TODO: this sucks
    if format_price:
        params['format_price'] = format_price
    if format_amount:
        params['format_amount'] = format_amount

    full_uri = uri.format(symbol=symbol)
    req = requests.get(full_uri, params=params)
    req.raise_for_status()

    data = req.json()

    return data #return both bids/asks for other steps to clean up later

def get_quote_hitbtc(
        coin_list,
        currency='USD',
        logger=LOGGER
):
    """fetch common summary data for crypto-coins

    Args:
        coin_list (:obj:`list`): list of tickers to look up
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): coin info for the day, JSONable

    """
    logger.info('Generating quote for %s -- HitBTC', config._list_to_str(coin_list))
    #singleton = False
    #if isinstance(coin_list, str):
    #    singleton = True
    #    logger.info('--singleton mode')

    logger.info('--fetching ticker data')
    raw_quote = get_ticker_hitbtc('')

    quote_df = df.DataFrame(raw_quote)

    logger.info('--filtering ticker data')





