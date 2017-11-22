"""prosper.datareader.coins: utilities for looking up info on cryptocoins"""
from enum import Enum

import pandas as pd

# TODO: Simplify import #
import prosper.datareader.config as config
import prosper.datareader.exceptions as exceptions
import prosper.datareader.cryptocompare as cryptocompare
import prosper.datareader.hitbtc as hitbtc

class Sources(Enum):
    hitbtc = 'hitbtc'
    cc = 'cryptocompare'

def columns_to_yahoo(
        quote_df,
        source
):
    """recast column names to yahoo equivalent

    Args:
        quote_df (:obj:`pandas.DataFrame`): dataframe to update
        source (:obj:`Enum`): source info

    Returns:
        (:obj:`pandas.DataFrame`): updated dataframe cols

    """
    if source == Sources.hitbtc:
        index_key = 'symbol'
        quote_df = quote_df.rename(index=quote_df[index_key])

    elif source == Sources.cc:
        ## Remap column names ##
        index_key = 'Name'
        column_map = {
            'CoinName': 'name',
            'FullName': 'more_info',
            'Name': 'symbol',
            'TotalCoinSupply': 'shares_outstanding',
            'TotalCoinsFreeFloat': 'float_shares',
            'LASTVOLUME': 'volume',
            'MKTCAP': 'market_capitalization',
            'CHANGEPCT24HOUR': 'change_pct',
            'MARKET': 'stock_exchange',
            'OPEN24HOUR': 'open',
            'HIGH24HOUR': 'high',
            'LOW24HOUR': 'low',
            'PRICE': 'last',
            'LASTUPDATE': 'timestamp'
        }

        ## Trim unused data ##
        keep_keys = list(column_map.keys())
        keep_keys.append(index_key)
        drop_keys = list(set(list(quote_df.columns.values)) - set(keep_keys))
        quote_df = quote_df.drop(drop_keys, 1)

        ## Apply remap ##
        quote_df = quote_df.rename(
            columns=column_map,
            index=quote_df[index_key])
        quote_df['change_pct'] = quote_df['change_pct'] / 100

    else:  # pragma: no cover
        raise exceptions.UnsupportedSource()

    ## reformat change_pct ##
    quote_df['change_pct'] = list(map(
        '{:+.2%}'.format,
        quote_df['change_pct']
    ))

    ## Timestamp to datetime ##
    quote_df['datetime'] = pd.to_datetime(
        pd.to_numeric(quote_df['timestamp']),
        infer_datetime_format=True,
        #format='%Y-%m-%dT%H:%M:%S',
        errors='coerce'
    )

    return quote_df

def supported_symbol_info(
        key_name,
        source=Sources.hitbtc
):
    """find unique values for key_name in symbol feed

    Args:
        key_name (str): name of key to search
        source (:obj:`Enum`): source name

    Returns:
        (:obj:`list`): list of unique values

    """
    if isinstance(source, str):
        source = Sources(source)

    if source == Sources.hitbtc:
        symbols_df = pd.DataFrame(hitbtc.quotes.get_supported_symbols_hitbtc())
    elif source == Sources.cc:
        symbols_df = pd.DataFrame(cryptocompare.quotes.get_supported_symbols_cc())
    else:  # pragma: no cover
        raise exceptions.UnsupportedSource()

    unique_list = list(symbols_df[key_name].unique())

    return unique_list

def get_symbol_hitbtc(
        commodity_ticker,
        currency_ticker,
        logger=config.LOGGER
):
    """get valid ticker to look up

    Args:
        commodity_ticker (str): short-name for crypto coin
        currency_ticker (str): short-name for currency
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (str): valid ticker for HITBTC

    """
    logger.info('--Fetching symbol list from API')
    symbols_df = pd.DataFrame(hitbtc.quotes.get_supported_symbols_hitbtc())

    symbol = symbols_df.query(
        'commodity==\'{commodity}\' & currency==\'{currency}\''.format(
            commodity=commodity_ticker.upper(),
            currency=currency_ticker.upper()
        ))

    if symbol.empty:
        raise exceptions.SymbolNotSupported()

    return symbol['symbol'].iloc[0]

def get_ticker_info_hitbtc(
        ticker,
        logger=config.LOGGER
):
    """reverse lookup, get more info about a requested ticker

    Args:
        ticker (str): info ticker for coin (ex: BTCUSD)
        force_refresh (bool, optional): ignore local cacne and fetch directly from API
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`dict`): hitBTC info about requested ticker

    """
    logger.info('--Fetching symbol list from API')
    data = hitbtc.quotes.get_supported_symbols_hitbtc()

    ## Skip pandas, vanilla list search ok here
    for ticker_info in data:
        if ticker_info['symbol'] == ticker.upper():
            return ticker_info

    raise exceptions.TickerNotFound()
