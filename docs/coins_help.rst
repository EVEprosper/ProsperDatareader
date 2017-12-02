========================
prosper.datareader.coins
========================

Meant as an extension of `pandas-datareader`_, ``prosper.datareader.coins`` provides the ability to fetch and parse data pertaining to crypto currencies.

``prosper.datareader.coins`` relies on services from `hitBTC`_ and `CryptoCompare`_

to_yahoo()
----------

Do you love how `pandas-datareader`_ displays data and want cryptocoin data in a similar shape?  Most fetchers include a ``to_yahoo`` bool value to convert results to a friendlier format. Not all keys are guaranteed to be returned and is offered only as a "nice to have".

Also, since Yahoo and Google have deprecated their financial APIs, do not expect continued coverage.

get_symbol()
------------

    ``symbol_name = coins.get_symbol('COIN_TIKER', 'CONVERT_TICKER')``

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
- ``BTC``

get_ticker_info()
-----------------

    ``ticker_info = coins.get_ticker_info('TICKER')``

If working backwards from a ticker, this function returns the original `hitBTC symbols`_ data.  

get_quote_hitbtc()
------------------

    ``quote_df = coins.get_quote_hitbtc(['BTC', 'ETH'])``

Get a peek at the current price and trend of your favorite crypto currency.  This feed helps get OHLC data as well as mimic `pandas-datareader`_ quote behavior with keys like ``pct_change``.

get_orderbook_hitbtc()
----------------------

    ``orderbook = coins.get_orderbook_hitbtc('BTC', 'asks')``

When you absolutely, positively, need all the data... go to the orderbook.  This supports ``asks`` and ``bids`` for lookup.

## TODO: add ``both`` behavior

get_quote_cc()
--------------

    ``quote = coins.get_quote_cc(['BTC', 'ETH'])``

Gets general metadata about requested coins from `CryptoCompare`_.  Supports ``USD`` and ``EUR`` as currency values.  Also returns current prices for desired coins.

get_ohlc_cc()
-------------

    ``history = coins.get_ohlc_cc('BTC', 30)``

Provides up to 2000 "units" of data for a given ``frequency`` (default=day).

frequency:

- ``'day'``
- ``'hour'``
- ``'minute'``


.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _CryptoCompare: https://www.cryptocompare.com/api/#introduction
.. _hitBTC: https://hitbtc.com/
.. _hitBTC symbols: https://hitbtc.com/api#symbols