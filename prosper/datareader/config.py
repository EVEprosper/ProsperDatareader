import pandas as pd

import prosper.common.prosper_logging as p_logging

LOGGER = p_logging.DEFAULT_LOGGER

def _list_to_str(ticker_list):
    """parses/joins ticker list

    Args:
        ticker_list (:obj:`list` or str): ticker(s) to parse

    Returns:
        (str): list of tickers

    """
    if isinstance(ticker_list, str):
        return ticker_list.upper()
    elif isinstance(ticker_list, list):
        return ','.join(ticker_list).upper()
    else:
        raise TypeError

def _cast_str_to_int(dataframe):
    """tries to apply to_numeric to each str column

    Args:
        dataframe (:obj:`pandas.DataFrame`): dataframe to adjust

    Returns:
        (:obj:`pandas.DataFrame`)

    """
    columns = list(dataframe.columns.values)
    for col in columns:
        try:
            dataframe[col] = pd.to_numeric(dataframe[col])
        except Exception:
            pass

    return dataframe
