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

def fetch_stock_summary_rh(
        ticker_list,
        logger=LOGGER
):
    """fetch common summary data for stock reporting

    Args:
        ticker_list (:obj:`list`): list of tickers to look up
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`dict`): stock info for the day, JSONable
        {'ticker', 'company_name', 'price', 'percent_change', 'PE', 'short_ratio', 'quote_datetime'}
    """
    pass
