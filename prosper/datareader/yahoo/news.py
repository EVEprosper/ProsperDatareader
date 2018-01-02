"""prosper.datareader.yahoo.news: parse news feeds from yahoo"""
from six.moves.html_parser import HTMLParser
import requests
import feedparser
import pandas as pd

DROP_COLUMNS = [
    'guidislink', 'links', 'summary_detail', 'title_detail', 'published_parsed'
]
FINANCE_NEWS_URL = 'http://finance.yahoo.com/rss/headline'
def fetch_finance_headlines_yahoo(
        ticker,
        drop_columns=DROP_COLUMNS,
        uri=FINANCE_NEWS_URL,
):
    """fetch & parse RSS feed from yahoo

    Args:
        ticker (str): company ticker to fetch
        drop_columns (:obj:`list`): list of columns not to report
        uri (str): headline endpoint

    Returns:
        dict: parsed RSS->JSON

    Raises:
        requests.exceptions: connection/HTTP errors

    """
    req = requests.get(
        url=uri,
        params={'s':ticker}
    )
    req.raise_for_status()

    feed_df = pd.DataFrame(feedparser.parse(req.text)['entries'])\
        .drop(drop_columns, axis=1, errors='ignore')

    # TODO: parse/encode utf-8

    return feed_df.to_dict(orient='records')
