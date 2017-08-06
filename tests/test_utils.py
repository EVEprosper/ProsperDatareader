"""test_utils.py: validate behavior for datareader.utils"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers

import prosper.datareader.utils as utils
import prosper.datareader.exceptions as exceptions

class TestNLTKInstall:
    """validate NLTK install checker works as expected"""
    fake_lexicon = 'fake_lexicon_name'
    real_lexicon = 'vader_lexicon'
    def test_empty_install(self):
        """make sure virgin setup looks like expected (order checker)"""
        assert utils.INSTALLED_PACKAGES == []

    def test_bad_install(self):
        """validate behavior for failed lexicon install"""
        with pytest.raises(exceptions.UtilsNLTKDownloadFailed):
            utils._validate_install(self.fake_lexicon)

        assert self.fake_lexicon not in utils.INSTALLED_PACKAGES

    def test_validate_install_happypath(self):
        """valdiate expected behavior for lexicon instal"""
        utils._validate_install(self.real_lexicon)

        assert self.real_lexicon in utils.INSTALLED_PACKAGES

    def test_validate_already_installed(self):
        """validate expected skip if already installed"""
        utils._TESTMODE = True
        with pytest.warns(exceptions.DatareaderWarning):
            utils._validate_install(self.real_lexicon)

        #return to normal mode
        utils._TESTMODE = False
