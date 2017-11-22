"""prosper.datareader.stocks: utilities for looking at stock market data"""

import pandas as pd

import prosper.datareader.robinhood as robinhood  # TODO: simplify import
import prosper.datareader.google as google
import prosper.datareader.config as config  # TODO: simplify import

SUMMARY_KEYS = [
    'symbol', 'name', 'pe_ratio', 'change_pct', 'current_price', 'updated_at'
]
def get_quote_rh(
        ticker_list,
        keys=SUMMARY_KEYS,
        logger=config.LOGGER
):
    """fetch common summary data for stock reporting

    Args:
        ticker_list (:obj:`list`): list of tickers to look up
        keys (:obj:`list`, optional): which keys to present in summary
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): stock info for the day, JSONable
        {'ticker', 'company_name', 'price', 'percent_change', 'PE', 'short_ratio', 'quote_datetime'}

    """
    logger.info('Generating quote for %s -- Robinhood', config._list_to_str(ticker_list))

    ## Gather Required Data ##
    summary_raw_data = []
    quotes = robinhood.quotes.fetch_price_quotes_rh(ticker_list, logger=logger)
    for quote in quotes['results']:
        fundamentals = robinhood.quotes.fetch_fundamentals_rh(quote['symbol'], logger=logger)
        instruments = robinhood.quotes.fetch_instruments_rh(quote['instrument'], logger=logger)

        stock_info = {**quote, **fundamentals, **instruments}   #join all data together
        stock_info['is_open'] = robinhood.quotes.market_is_open(instruments['market'])

        if stock_info['is_open']:   #pragma: no cover
            stock_info['current_price'] = stock_info['last_trade_price']
        else:
            stock_info['current_price'] = stock_info['last_extended_hours_trade_price']

        summary_raw_data.append(stock_info)

    summary_df = pd.DataFrame(summary_raw_data)
    summary_df = config._cast_str_to_int(summary_df)

    summary_df['change_pct'] = (summary_df['current_price'] - summary_df['previous_close']) / summary_df['previous_close']

    summary_df['change_pct'] = list(map(
        '{:+.2%}'.format,
        summary_df['change_pct']
    ))
    if keys:
        return summary_df[keys]
    else:
        return summary_df

def company_news_rh(
        ticker,
        page_limit=robinhood.news.PAGE_HARDBREAK,
        logger=config.LOGGER
):
    """get news items from Robinhood for a given company

    Args:
        ticker (str): stock ticker for desired company
        page_limit (int, optional): how many pages to allow in call
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): tabularized data for news

    """
    logger.info('Fetching company raw data feed for `%s` -- ROBINHOOD', ticker)
    raw_news_data = robinhood.news.fetch_company_news_rh(
        ticker.upper(),
        page_limit=page_limit,
        logger=logger
    )

    logger.info('--Pushing data into Pandas')
    news_df = pd.DataFrame(raw_news_data)
    news_df['published_at'] = pd.to_datetime(news_df['published_at'])

    logger.debug(news_df)
    return news_df

def company_news_google(
        ticker,
        pretty=True,
        _source_override=google.news.GOOGLE_COMPANY_NEWS,
        logger=config.LOGGER
):
    """get news items from Google for a given company

    Args:
        ticker (str): ticker to look up
        pretty (bool, optional): human-readable column names
        keep_google_links (bool, optional): include google metadata links
        _source_override (str, optional): source URI; used to switch feeds
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): tabularized data for news

    """
    logger.info('Fetching company raw data feed for `%s` -- GOOGLE', ticker)
    raw_news_data = google.news.fetch_company_news_google(
        ticker,
        uri=_source_override,
        logger=logger
    )

    logger.info('--Pushing data into Pandas')
    news_df = pd.DataFrame(raw_news_data)
    news_df['tt'] = pd.to_datetime(news_df['tt'])

    if pretty:
        logger.info('--Prettifying data')
        col_map = {
            's': 'source',
            'u': 'url',
            't': 'title',
            'sp': 'blurb',
            'tt': 'datetime',
            'd': 'age'
        }
        news_df = news_df.rename(columns=col_map)

    logger.debug(news_df)
    return news_df


def market_news_google(
        pretty=True,
        _source_override=google.news.GOOGLE_MARKET_NEWS,
        logger=config.LOGGER
):
    """Get all of today's general finance news from Google

    Args:
        pretty (bool, optional): human-readable column names
        _source_override (str, optional): source URI; used to switch feeds
        logger (:obj:`logging.logger`, optional): logging handle

    Returns:
        (:obj:`pandas.DataFrame`): tabularized data for news

    """
    logger.info('Fetching general finance news -- GOOGLE')
    news_df = company_news_google(
        '',
        pretty=pretty,
        _source_override=_source_override,
        logger=logger
    )
    logger.debug(news_df)
    return news_df
