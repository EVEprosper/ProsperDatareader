"""test_cryptopanic.py: validate behavior for datareader.cryptopanic"""
from os import path

import pytest
import helpers

import prosper.datareader.exceptions as exceptions
import prosper.datareader.cryptopanic as cryptopanic

class TestFetchPosts:
    coin_ticker = 'BTC'
    multi_ticker = 'BTC,ETH'

    def test_fetch_posts_happypath(self):
        """validate expected behavior for cryptopanic.posts.fetch_posts()"""
        articles = cryptopanic.posts.fetch_posts(
            auth_token=helpers.CONFIG.get('CRYPTOPANIC', 'auth_token'),
            ticker=self.coin_ticker
        )

        helpers.validate_schema(articles, 'coins/cryptopanic_posts.schema')
