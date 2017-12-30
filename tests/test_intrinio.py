"""test_intrinio: validate intrinio connections and helpers"""

import pytest
import helpers

import prosper.datareader.intrinio.auth as auth

class TestAuth:
    """validate that authentication works"""
    route = 'access'

    def test_direct_auth_happypath(self):
        """validate direct_auth scheme"""
        pass
