"""test_cryptopanic.py: validate behavior for datareader.cryptopanic"""
from os import path

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
        articles = cryptopanic.posts.fetch_posts(
            auth_token=CRYPTOPANIC_AUTH,
            ticker=self.coin_ticker
        )

        helpers.validate_schema(articles, 'coins/cryptopanic_posts.schema')
