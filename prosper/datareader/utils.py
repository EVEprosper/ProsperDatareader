"""datareader.utils.py: tools for fetching stock news"""
from os import path
import warnings

NLTK_IMPORT = True
try:
    from nltk import download
    import nltk.sentiment as sentiment
except ImportError:
    NLTK_IMPORT = False
import pandas as pd

from prosper.datareader.config import LOGGER as G_LOGGER
import prosper.datareader.exceptions as exceptions

_TESTMODE = False
INSTALLED_PACKAGES = []
def _validate_install(
        package_name,
        logger=G_LOGGER
):
    """make sure required NLTK lexicon is available

    Note:
        Skips NLTK GUI downloader.  Please see RHEL for full lexicon list

    Args:
        package_name (str): name of package on nltk.download()
        logger (:obj:`logging.logger`, optional): logging handle

    Raises:
        (:obj:`exceptions.UtilsNLTKDownloadFailed`)

    """
    if not NLTK_IMPORT:
        raise ImportError('Please use `prosperdatareader[nltk]` import')

    if package_name in INSTALLED_PACKAGES:
        if _TESTMODE:
            warnings.warn(
                'Package already installed',
                exceptions.DatareaderWarning
            )
        logger.info('Package already installed: %s', package_name)
        return

    logger.info('Installing package: %s', package_name)
    install_status = download(package_name)

    if not install_status:
        raise exceptions.UtilsNLTKDownloadFailed(
            'Unable to install: {}'.format(package_name))

    INSTALLED_PACKAGES.append(package_name)

def _get_analyzer():
    """fetch analyzer for grading strings

    Returns:
        (:obj:`nltk.sentiment.vader.SentimentIntensityAnalyzer`)

    """
    if 'vader_lexicon' not in INSTALLED_PACKAGES:
        _validate_install('vader_lexicon')

    return sentiment.vader.SentimentIntensityAnalyzer()

COLUMN_NAMES = ['neu', 'pos', 'compound', 'neg']
def map_vader_sentiment(
        string_series,
        column_names=COLUMN_NAMES
):
    """apply vader sentiment to an entire column and update the original source

    Note:
        relies on `pandas.series.map()` functionality

    Args:
        string_series (:obj:`pandas.Series`): column to grade strings from
        column_names (:obj:`list`, optional): column names for vader results
            ['neu', 'pos', 'compound', 'neg']
    Returns:
        (:obj:`pandas.DataFrame`) updated series + vader-sentiments

    """
    analyzer = _get_analyzer()
    def map_func(grade_str):
        """actual map function that does the heavy lifting

        Args:
            grade_str (str): string to be scored

        Returns:
            (:obj:`list`): original str + polarity scores ('neu', 'pos', 'compound', 'neg')

        """
        row = []
        row.append(grade_str)
        grades = analyzer.polarity_scores(grade_str)
        row.extend([
            grades['neu'],
            grades['pos'],
            grades['compound'],
            grades['neg']
        ])
        return row

    source_col = string_series.name
    columns = [source_col]
    columns.extend(column_names)

    new_df = pd.DataFrame(
        list(map(map_func, string_series)),
        columns=columns
    )

    return new_df
