"""prosper.datareader.yahoo.news: parse news feeds from yahoo"""

import requests
import feedparser

FINANCE_NEWS_URL = 'http://finance.yahoo.com/rss/headline'
def fetch_finance_headlines_yahoo(
        ticker_list,
        uri=FINANCE_NEWS_URL
):
    """fetch & parse RSS feed from yahoo

    Args:
        ticker_list (str or list): list of tickers to fetch
        uri (str): headline endpoint

    Returns:
        dict: parsed RSS->JSON

    Raises:
        requests.exceptions: connection/HTTP errors

    """
    pass
