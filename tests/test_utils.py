"""test_utils.py: validate behavior for datareader.utils"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas as pd

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

def test_map_vader_sentiment():
    """validate map_vader_sentiment() behavior"""
    demo_data = [
        {'text': 'I like hotdogs'},
        {'text': 'Sandwiches are bad'},
        {'text': 'Libraries have books'}
    ]

    demo_df = pd.DataFrame(demo_data)
    graded_df = utils.map_vader_sentiment(demo_df['text'])

    assert graded_df['compound'].loc[0] > 0
    assert graded_df['compound'].loc[1] < 0
    assert graded_df['compound'].loc[2] == 0
