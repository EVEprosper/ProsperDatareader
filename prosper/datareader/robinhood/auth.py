"""Helper for logging in/out of Robinhood"""
import logging

import requests

RH_LOGIN = ''
RH_LOGOUT = ''
class RobinHoodAuth(object):
    """context manager for logging in and out of Robinhood

    Args:
        username (str): Robinhood username
        password (str): Robinhood password
        client_id (str): oAuth client header

    Note:
        Does not work with `mfa_code` or 2-FA accounts

    Returns:
        str: bearer token for authenticating requests

    Raises:
        requests.RequestException: connection or HTTP errors
        KeyError: expected json response missing required keys

    """
    def __init__(
            self,
            username,
            password,
            client_id='c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS'
    ):
        self._username = username
        self._password = password
        self.client_id = client_id

        self.bearer_token = ''
        self.refresh_token = ''

    def __enter__(self):
        """context manager for logging in.  Returns bearer_token for use elsewhere"""
        logging.debug('RobinHood LOGIN -- `%s` with `%s`', RH_LOGIN, self._username)
        req = requests.post(
            RH_LOGIN,
            data=dict(
                password=self._password,
                username=self._username,
                grant_type='password',
                client_id=self.client_id,
            )
        )
        req.raise_for_status()
        self.bearer_token = 'Bearer ' + req.json()['access_token']
        self.refresh_token = req.json()['refresh_token']
        logging.info('RobinHood LOGIN -- Success')
        return self.bearer_token

    def __exit__(self, *exc_info):
        logging.debug('RobinHood LOGOUT -- `%s` with `%s`', RH_LOGOUT, self._username)
        req = requests.post(
            RH_LOGOUT,
            data=dict(
                client_id=self.client_id,
                token=self.refresh_token,
            )
        )
        req.raise_for_status()
        self.bearer_token = ''
        self.refresh_token = ''
