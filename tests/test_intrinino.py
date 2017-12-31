"""test_intrinino: validate intrinino connections and helpers

NOTE: may be flaky with pytest-xdist due to order problems

"""

import pytest
import helpers

import prosper.datareader.intrinino.auth as auth
import prosper.datareader.exceptions as exceptions

CAN_DIRECT_AUTH = all([
    helpers.CONFIG.get('INTRININO', 'username'),
    helpers.CONFIG.get('INTRININO', 'password')
])
CAN_PUBLIC_KEY = bool(helpers.CONFIG.get('INTRININO', 'public_key'))


def direct_connection(capsys):
    """generate a direct-auth connector"""
    with capsys.disabled():
        return auth.IntrininoHelper(
            username=helpers.CONFIG.get('INTRININO', 'username'),
            password=helpers.CONFIG.get('INTRININO', 'password')
        )

def pubkey_connection(capsys):
    """generate a pub-key connector"""
    with capsys.disabled():
        return auth.IntrininoHelper(
            public_key=helpers.CONFIG.get('INTRININO', 'public_key')
        )

def test_bad_auth():
    """validate helper complains about not having valid auth setup"""
    with pytest.raises(exceptions.InvalidAuth):
        bad_auth = auth.IntrininoHelper()

    with pytest.raises(exceptions.InvalidAuth):
        too_much_auth = auth.IntrininoHelper(
            username='fake',
            password='fake',
            public_key='flake'
        )

def test_direct_auth_happypath(capsys):
    """validate direct_auth scheme"""
    if not CAN_DIRECT_AUTH:
        pytest.xfail('Missing username/password')

    direct_auth = direct_connection(capsys)

    response = direct_auth.request('usage/access')
    helpers.validate_schema(response, 'intrinino/intrinino_access.schema')

@pytest.mark.xfail
def test_pubkey_auth_happypath(capsys):
    """validate direct_auth scheme"""
    if not CAN_PUBLIC_KEY:
        pytest.xfail('Missing username/password')

    pub_auth = pubkey_connection(capsys)

    response = pub_auth.request('usage/access')
    helpers.validate_schema(response, 'intrinino/intrinino_access.schema')

def test_news_endpoint(capsys):
    """validate /news endpoint contents"""
    if not CAN_DIRECT_AUTH:
        pytest.xfail('Missing username/password')

    response = direct_connection(capsys).request(
        'news',
        params={'ticker':'AAPL'}
    )

    [
        helpers.validate_schema(article, 'intrinino/intrinino_news.schema')
        for article in response['data']
    ]
