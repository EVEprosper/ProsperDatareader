"""test_cryptopanic.py: validate behavior for datareader.cryptopanic"""
from os import path
import time

import pytest
import helpers

import prosper.datareader.exceptions as exceptions
import prosper.datareader.cryptopanic as cryptopanic

CRYPTOPANIC_AUTH = helpers.CONFIG.get_option('CRYPTOPANIC', 'auth_token')
class TestFetchPosts:
    coin_ticker = 'BTC'
    multi_ticker = 'BTC,ETH'

    def test_fetch_posts_happypath(self):
        """validate expected behavior for cryptopanic.posts.fetch_posts()"""
        if not CRYPTOPANIC_AUTH:
            pytest.xfail('Lacking `auth_token` for cryptopanic')

        time.sleep(0.5)  # cryptopanic API is heavily rate-limited
        articles = cryptopanic.posts.fetch_posts(
            auth_token=CRYPTOPANIC_AUTH,
            ticker=self.coin_ticker
        )

        helpers.validate_schema(articles, 'coins/cryptopanic_posts.schema')

    def test_fetch_posts_complex(self):
        """hit all the things"""
        if not CRYPTOPANIC_AUTH:
            pytest.xfail('Lacking `auth_token` for cryptopanic')

        time.sleep(0.5)  # cryptopanic API is heavily rate-limited
        articles = cryptopanic.posts.fetch_posts(
            auth_token=CRYPTOPANIC_AUTH,
            ticker=self.multi_ticker,
            filters='hot',
            public=False,
            following=True
        )

    def test_fetch_posts_bad_filter(self):
        """validate error case for bad filter"""
        if not CRYPTOPANIC_AUTH:
            pytest.xfail('Lacking `auth_token` for cryptopanic')

        time.sleep(0.5)  # cryptopanic API is heavily rate-limited
        with pytest.raises(AssertionError):
            articles = cryptopanic.posts.fetch_posts(
                auth_token=CRYPTOPANIC_AUTH,
                ticker=self.coin_ticker,
                filters='butts'
            )

    def test_fetch_posts_pagelimit(self):
        """validate pagination limit"""
        if not CRYPTOPANIC_AUTH:
            pytest.xfail('Lacking `auth_token` for cryptopanic')

        time.sleep(0.5)  # cryptopanic API is heavily rate-limited
        with pytest.warns(exceptions.PaginationWarning):
            articles = cryptopanic.posts.fetch_posts(
                auth_token=CRYPTOPANIC_AUTH,
                ticker=self.coin_ticker,
                article_limit=50
            )
