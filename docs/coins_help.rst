========================
prosper.datareader.coins
========================

Meant as an extension of `pandas-datareader`_, ``prosper.datareader.coins`` provides the ability to fetch and parse data pertaining to crypto currencies.

``prosper.datareader.coins`` relies on services from `hitBTC`_.

Info
====

General metadata and feed testing tools.

**NOTE**: will implement caching layer for info, since this data should only refresh daily

get_symbol()
------------

    ``symbol_name = coins.info.get_symbol('COIN_TIKER', 'CONVERT_TICKER')``

Price of a crypto currency is measured in relation to other currencies a la FOREX.  `hitBTC`_ requires a smash-cut version of coin + currency.

Examples:

+------+----------+--------+
| Coin | Currency | Ticker |
+======+==========+========+
| BTC  | USD      | BTCUSD |
+------+----------+--------+
| ETH  | EUR      | ETHEUR |
+------+----------+--------+
| ETH  | BTC      | ETHBTC |
+------+----------+--------+

Expected supported currencies:

- ``USD``
- ``EUR``
- ``ETH``
- ``BTC``

For more info, try ``info.supported_currencies()`` for a current list

get_ticker_info()
-----------------

    ``ticker_info = coins.info.get_ticker_info('TICKER')``

If working backwards from a ticker, this function returns the original `hitBTC symbols`_ data.  

Prices
======

get_quote_hitbtc()
------------------

    ``quote_df = coins.prices.get_quote_hitbtc(['BTC', 'ETH'])``

Get a peek at the current price and trend of your favorite crypto currency.  This feed helps get OHLC data as well as mimic `pandas-datareader`_ quote behavior with keys like ``pct_change``.

get_orderbook_hitbtc()
----------------------

    ``orderbook = coins.prices.get_orderbook_hitbtc('BTC', 'asks')``

When you absolutely, positively, need all the data... go to the orderbook.  This supports ``asks`` and ``bids`` for lookup.

## TODO: add ``both`` behavior

.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _hitBTC: https://hitbtc.com/
.. _hitBTC symbols: https://hitbtc.com/api#symbols