"""datareader.news.py: tools for fetching stock news"""
from os import path

import requests
import demjson

from prosper.datareader.config import LOGGER as G_LOGGER

LOGGER = G_LOGGER
HERE = path.abspath(path.dirname(__file__))

GOOGLE_COMPANY_NEWS = 'https://www.google.com/finance/company_news'
def fetch_company_news_google(
        ticker,
        pretty=False,
        uri=GOOGLE_COMPANY_NEWS,
        logger=LOGGER
):
    """fetch news for one company ticker

    Args:
        ticker (str): ticker for company
        pretty (bool, optional): recast short->pretty keys
        uri (str, optional): endpoint URI for `company_news`
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`list`): processed news results, JSONable

    """
    pass

GOOGLE_MARKET_NEWS = 'https://www.google.com/finance/market_news'
def fetch_market_news_google(
        ticker,
        pretty=False,
        uri=GOOGLE_MARKET_NEWS,
        logger=LOGGER
):
    """fetch market news for indexes and google products

    Args:
        ticker (str): google-name for index or product (ex: INDEXNASDAQ)
        pretty (bool, optional): recast short->pretty keys
        uri (str, optional): endpoint URI for `market_news`
        logger (:obj:`logging.logger`, optional): logging handle
    Returns:
        (:obj:`list`): processed news results, JSONable

    """
    pass

def pretty_return_google_news(
        results,
        logger=LOGGER
):
    """recast keys shorthand->human in google result

    Args:
        results (:obj:`list`): google news results
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`list`): human-friendly results, JSONable

    """
    pass
