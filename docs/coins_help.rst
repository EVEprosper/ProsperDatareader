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

.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _hitBTC: https://hitbtc.com/
.. _hitBTC symbols: https://hitbtc.com/api#symbols