"""test_intrinino: validate intrinino connections and helpers

NOTE: may be flaky with pytest-xdist due to order problems

"""

import pytest
import helpers

import prosper.datareader.intrinio.auth as auth
import prosper.datareader.exceptions as exceptions

CAN_DIRECT_AUTH = all([
    helpers.CONFIG.get_option('INTRINIO', 'username'),
    helpers.CONFIG.get_option('INTRINIO', 'password')
])
CAN_PUBLIC_KEY = bool(helpers.CONFIG.get_option('INTRINIO', 'public_key'))


def direct_connection(capsys):
    """generate a direct-auth connector"""
    with capsys.disabled():
        return auth.IntrinioHelper(
            username=helpers.CONFIG.get_option('INTRINIO', 'username'),
            password=helpers.CONFIG.get_option('INTRINIO', 'password')
        )

def pubkey_connection(capsys):
    """generate a pub-key connector"""
    with capsys.disabled():
        return auth.IntrinioHelper(
            public_key=helpers.CONFIG.get_option('INTRINIO', 'public_key')
        )

def test_bad_auth():
    """validate helper complains about not having valid auth setup"""
    with pytest.raises(exceptions.InvalidAuth):
        bad_auth = auth.IntrinioHelper()

    with pytest.raises(exceptions.InvalidAuth):
        too_much_auth = auth.IntrinioHelper(
            username='fake',
            password='fake',
            public_key='flake'
        )

def test_direct_auth_happypath(capsys):
    """validate direct_auth scheme"""
    if not CAN_DIRECT_AUTH:
        pytest.xfail('Missing `username`/`password` for intrinio')

    direct_auth = direct_connection(capsys)

    response = direct_auth.request('usage/access')
    helpers.validate_schema(response, 'intrinio/intrinio_access.schema')

@pytest.mark.xfail
def test_pubkey_auth_happypath(capsys):
    """validate direct_auth scheme"""
    if not CAN_PUBLIC_KEY:
        pytest.xfail('Missing `username`/`password` for intrinio')

    pub_auth = pubkey_connection(capsys)

    response = pub_auth.request('usage/access')
    helpers.validate_schema(response, 'intrinio/intrinio_access.schema')

def test_news_endpoint(capsys):
    """validate /news endpoint contents"""
    if not CAN_DIRECT_AUTH:
        pytest.xfail('Missing `username`/`password` for intrinio')

    response = direct_connection(capsys).request(
        'news',
        params={'ticker':'AAPL'}
    )

    [
        helpers.validate_schema(article, 'intrinio/intrinio_news.schema')
        for article in response['data']
    ]
