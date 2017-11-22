"""prosper.datareader.hitbtc.quotes: utilities for fetching price/info -- HITBTC"""

import requests

from .. import config
from .. import exceptions
from ..coins import supported_symbol_info

SYMBOLS_URI_HITBTC = 'http://api.hitbtc.com/api/1/public/symbols'
def get_supported_symbols_hitbtc(
        uri=SYMBOLS_URI_HITBTC,
        data_key='symbols'
):
    """fetch supported symbols from API -- hitBTC

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

def coin_list_to_symbol_list(
        coin_list,
        currency='USD',
        strict=False
):
    """convert list of crypto currencies to HitBTC symbols

    Args:
        coin_list (str or :obj:`list`): list of coins to convert
        currency (str, optional): currency to FOREX against
        strict (bool, optional): throw if unsupported ticker is requested

    Returns:
        (:obj:`list`): list of valid coins and tickers

    """
    valid_symbol_list = supported_symbol_info('symbol')

    symbols_list = []
    invalid_symbols = []
    for coin in coin_list:
        ticker = str(coin).upper() + currency
        if ticker not in valid_symbol_list:
            invalid_symbols.append(ticker)

        symbols_list.append(ticker)

    if invalid_symbols and strict:
        raise KeyError('Unsupported ticker requested: {}'.format(invalid_symbols))

    return symbols_list

COIN_TICKER_URI_HITBTC = 'http://api.hitbtc.com/api/1/public/{symbol}/ticker'
def get_ticker_hitbtc(
        symbol,
        uri=COIN_TICKER_URI_HITBTC
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
        ## fetching entire ticker list ##
        full_uri = uri.replace(r'{symbol}/', '')
    else:
        full_uri = uri.format(symbol=symbol)

    req = requests.get(full_uri)
    req.raise_for_status()
    data = req.json()

    if not symbol:
        ## fetching entire ticker list ##
        data = config._listify(data, 'symbol')

    return data
