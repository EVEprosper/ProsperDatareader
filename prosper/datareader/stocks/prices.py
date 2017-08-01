"""datareader.news.py: tools for fetching stock news"""
from os import path

import requests
import pandas as pd

from prosper.datareader.config import LOGGER as G_LOGGER

LOGGER = G_LOGGER
HERE = path.abspath(path.dirname(__file__))

RH_PRICE_QUOTES = 'https://api.robinhood.com/quotes'
def fetch_price_quotes_rh(
        ticker_list,
        uri=RH_PRICE_QUOTES,
        logger=LOGGER
):
    """fetch quote data from Robinhood

    Notes:
        Currently requires no Auth

    Args:
        ticker_list (:obj:`list` or str): list of tickers to fetch
        uri (str, optional): endpoint URI for `quotes`
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`list`): results from endpoint, JSONable

    """
    pass

RH_FUNDAMENTALS = 'https://api.robinhood.com/fundamentals/'
def fetch_fundamentals_rh(
        ticker,
        uri=RH_FUNDAMENTALS,
        logger=LOGGER
):
    """fetch fundamental data from Robinhood

    Notes:
        Currently requires no Auth

    Args:
        ticker (str): ticker for company
        uri (str, optional): endpoint URI for `fundamentals`
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`dict`): company fundamental data, JSONable

    """
    pass

RH_INSTRUMENTS = 'https://api.robinhood.com/instruments'
def fetch_instruments_rh(
        company_uid,
        uri=RH_INSTRUMENTS,
        logger=LOGGER
):
    """fetch instrument data for stock

    Notes:
        Currently requires no Auth
        company_uid needs to come from another request

    Args:
        company_uid (str): uid for company
        uri (str, optional): endpoint URI for `instruments`
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`dict`): trading data for company, JSONable

    """
    pass

SUMMARY_KEYS = ['symbol', 'simple_name', 'PE', 'change_pct', 'last', 'short_ratio', 'time']
def stock_summary_rh(
        ticker_list,
        keys=SUMMARY_KEYS,
        logger=LOGGER
):
    """fetch common summary data for stock reporting

    Args:
        ticker_list (:obj:`list`): list of tickers to look up
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): stock info for the day, JSONable
        {'ticker', 'company_name', 'price', 'percent_change', 'PE', 'short_ratio', 'quote_datetime'}
    """
    summary_raw_data = []

    ## Gather Required Data ##
    quotes = fetch_price_quotes_rh(ticker_list, logger=logger)
    for quote in quotes:
        fundamentals = fetch_fundamentals_rh(quote['symbol'], logger=logger)
        instruments = fetch_instruments_rh(quote['instrument'], logger=logger)

        stock_info = {**quote, **fundamentals, **instruments}

        summary_raw_data.append(stock_info)


    summary_df = pd.DataFrame(summary_raw_data)

    #TODO: calc pct_change

    return summary_df[keys]
