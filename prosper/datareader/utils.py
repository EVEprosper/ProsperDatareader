"""datareader.utils.py: tools for fetching stock news"""
from os import path
import warnings

from nltk import download
import nltk.sentiment as sentiment

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
