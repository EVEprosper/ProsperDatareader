"""datareader.coins.prices.py: tools for fetching cryptocoin price data"""
from datetime import datetime
import itertools
from os import path

import requests
import pandas as pd

from prosper.datareader.config import LOGGER as G_LOGGER
import prosper.datareader.exceptions as exceptions

LOGGER = G_LOGGER
HERE = path.abspath(path.dirname(__file__))
