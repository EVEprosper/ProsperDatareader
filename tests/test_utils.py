"""test_utils.py: validate behavior for datareader.utils"""
from datetime import datetime
from os import path

import pytest
import requests
import helpers
import pandas as pd
import nltk

import prosper.datareader.utils as utils
import prosper.datareader.exceptions as exceptions

DEMO_DATA = [
    {'text': 'I like hotdogs', 'etc': 4},
    {'text': 'Sandwiches are bad', 'etc': 5},
    {'text': 'Libraries have books', 'etc': 6}
]

def test_prep():
    """prep environemnt into known starting state"""
    utils.INSTALLED_PACKAGES = []

class TestNLTKInstall:
    """validate NLTK install checker works as expected"""
    fake_lexicon = 'fake_lexicon_name'
    real_lexicon = 'vader_lexicon'

    def test_bad_install(self):
        """validate behavior for failed lexicon install"""
        utils.INSTALLED_PACKAGES = []
        with pytest.raises(exceptions.UtilsNLTKDownloadFailed):
            utils._validate_install(self.fake_lexicon)

        assert self.fake_lexicon not in utils.INSTALLED_PACKAGES

    def test_no_install(self):
        """make sure raises without .[nltk]"""
        utils.NLTK_IMPORT = False
        with pytest.raises(ImportError):
            utils._validate_install(self.real_lexicon)

        utils.NLTK_IMPORT = True

    def test_validate_install_happypath(self):
        """valdiate expected behavior for lexicon instal"""
        utils._validate_install(self.real_lexicon)

        assert self.real_lexicon in utils.INSTALLED_PACKAGES

    def test_validate_already_installed(self):
        """validate expected skip if already installed"""
        utils._TESTMODE = True
        utils._validate_install(self.real_lexicon)  #Make sure pre installed
        with pytest.warns(exceptions.DatareaderWarning):
            utils._validate_install(self.real_lexicon)

        #return to normal mode
        utils._TESTMODE = False

def test_get_analyzer():
    """validate _get_analyzer() behavior"""
    analyzer = utils._get_analyzer()
    assert isinstance(analyzer, nltk.sentiment.vader.SentimentIntensityAnalyzer)

def test_get_analyzer_no_lexicon():
    """validate ability to setup vader_lexicon if virgin"""
    utils._TESTMODE = True
    utils.INSTALLED_PACKAGES = []

    with pytest.warns(exceptions.DatareaderWarning):
        analyzer = utils._get_analyzer()

    assert 'vader_lexicon' in utils.INSTALLED_PACKAGES

    utils._TESTMODE = False

def test_map_vader_sentiment():
    """validate map_vader_sentiment() behavior"""
    demo_df = pd.DataFrame(DEMO_DATA)
    graded_df = utils.map_vader_sentiment(demo_df['text'])

    assert graded_df['compound'].loc[0] > 0
    assert graded_df['compound'].loc[1] < 0
    assert graded_df['compound'].loc[2] == 0

    custom_columns = ['ennie', 'mennie', 'minie', 'moe']
    custom_df = utils.map_vader_sentiment(
        demo_df['text'],
        column_names=custom_columns
    )
    my_cols = list(custom_df.columns.values)
    assert list(set(custom_columns) - set(my_cols)) == []

    with pytest.raises(exceptions.VaderClassificationException):
        bad_df = utils.map_vader_sentiment(
            demo_df['text'],
            column_names=['not', 'enough', 'keys']
        )

def test_prod_vader_sentiment():
    """validate vader_sentiment()"""
    demo_df = pd.DataFrame(DEMO_DATA)

    vader_df = utils.vader_sentiment(demo_df, 'text')

    expected_columns = ['etc', 'text']
    expected_columns.extend(utils.COLUMN_NAMES)

    assert expected_columns == list(vader_df.columns.values)

    assert vader_df['compound'].loc[0] > 0
    assert vader_df['compound'].loc[1] < 0
    assert vader_df['compound'].loc[2] == 0
