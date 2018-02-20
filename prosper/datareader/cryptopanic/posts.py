"""prosper.datareader.cryptopanic.posts: utilities for fetching cryptocoin news"""
import warnings

import requests

from .. import exceptions

CRYPTOPANIC_FILTERS = (
    'trending', 'hot', 'bullish', 'bearish', 'important', 'saved', 'lol',
)

ROOT_API = 'https://cryptopanic.com/api/'
def fetch_posts(
        auth_token,
        ticker='',
        filters='',
        public=True,
        following=False,
        article_limit=10000,
        _route='posts/'
):
    """fetch posts from cryptopanic

    Notes:
        Paginated

    Args:
        auth_token (str): authentication token for cryptopanic
        ticker (str): short name of coin
        filters (str): cryptopanic filter
        public (bool): public/private filter
        article_limit (int): pagination limit
        _route (str): endpoint route

    Returns:
        list: list of articles for a given query

    Raises:
        requests.exceptions: connection or HTTP error

    """
    params = {'auth_token': auth_token}
    if ticker:
        params['currencies'] = ticker
    if filters:
        assert filters in CRYPTOPANIC_FILTERS
        params['filter'] = filters.lower()
    if public:
        params['public'] = True
    if not public and following:
        params['following'] = True

    articles = []
    article_count = 0
    url = ROOT_API + _route
    while True:
        req = requests.get(
            url=url,
            params=params,
        )
        req.raise_for_status()
        page = req.json()

        articles.extend(page['results'])
        article_count += len(page['results'])

        url = page['next']

        if article_count >= article_limit:
            warnings.warn(
                'article limit {} reached'.format(article_limit),
                exceptions.PaginationWarning
            )
        if not url or article_count >= article_limit:
            break

    return articles
