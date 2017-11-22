"""prosper.datareader.google.news: news utilities using google APIs"""
from datetime import datetime

import demjson
import requests
from six.moves.html_parser import HTMLParser

from .. import config
from .. import exceptions

def validate_google_response(response, tag_primary=True):
    """crunches down google response for return

    Args:
        response (:obj:`dict`): data from google response
        tag_primary (bool, optional): certain articles exist at front of lists, mark them

    Returns:
        (:obj:`list`): list of parsed news articles

    """
    article_list = []
    for block in response['clusters']:
        if int(block['id']) == -1:
            continue # final entry is weird

        for index, story in enumerate(block['a']):
            ## Tag primary sources ##
            if index == 0 and tag_primary:
                story['primary'] = True
            elif tag_primary:
                story['primary'] = False

            ## Clean up HTML ##
            story['t'] = HTMLParser().unescape(story['t'])
            story['sp'] = HTMLParser().unescape(story['sp'])

            ## ISO datetime ##
            story['tt'] = datetime.fromtimestamp(int(story['tt'])).isoformat()

            article_list.append(story)

    return article_list

GOOGLE_MARKET_NEWS = 'https://www.google.com/finance/market_news'
GOOGLE_COMPANY_NEWS = 'https://www.google.com/finance/company_news'
def fetch_company_news_google(
        ticker,
        uri=GOOGLE_COMPANY_NEWS,
        logger=config.LOGGER
):
    """fetch news for one company ticker

    Args:
        ticker (str): ticker for company
        uri (str, optional): endpoint URI for `company_news`
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`list`): processed news results, JSONable

    """
    logger.info('fetching company_news for %s', ticker)

    params = {
        'q': ticker,
        'output': 'json'
    }
    logger.debug(uri)
    req = requests.get(uri, params=params)
    req.raise_for_status()

    articles_list = []
    try:
        raw_articles = demjson.decode(req.text)
    except Exception as err: #pragma: no cover
        #No coverage: blank news has no single ticker
        logger.debug(req.text)
        if str(err) == 'Can not decode value starting with character \'<\'': #pragma: no cover
            #demjson does not raise unique exceptions :<
            logger.warning('empty news endpoint for %s @ %s', ticker, uri)
            return articles_list
        else:
            logger.error('Unable to parse news items for %s @ %s', ticker, uri, exc_info=True)
            raise err

    logger.info('parsing news object for %s', ticker)
    articles_list = validate_google_response(raw_articles)

    return articles_list
