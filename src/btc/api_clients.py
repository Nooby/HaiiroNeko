import requests

from datetime import datetime

from rq_helper.btc import enqueue_write

def get_bitstamp():
    r = requests.get('https://www.bitstamp.net/api/ticker/')
    data = r.json()
    return enqueue_write('Bitstamp', data['last'], data['ask'], data['bid'], datetime.utcnow())

def get_coinbase():
    r = requests.get('https://coinbase.com/api/v1/prices/spot_rate')
    data = r.json()
    spot = data['amount']

    r = requests.get('https://coinbase.com/api/v1/prices/buy')
    data = r.json()
    ask = data['total']['amount']

    r = requests.get('https://coinbase.com/api/v1/prices/sell')
    data = r.json()
    bid = data['total']['amount']

    return enqueue_write('Coinbase', spot, ask, bid, datetime.utcnow())

def get_kraken():
    r = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
    data = r.json()
    trade_pair_data = data['result']['XXBTZUSD']
    spot = trade_pair_data['c'][0]
    ask = trade_pair_data['a'][0]
    bid = trade_pair_data['b'][0]
    return enqueue_write('Kraken', spot, ask, bid, datetime.utcnow())

def get_bitfinex():
    r = requests.get('https://api.bitfinex.com/v1/ticker/btcusd', verify=False)
    data = r.json()
    return enqueue_write('bitfinex', data['last_price'], data['ask'], data['bid'], datetime.utcnow())

def get_mtgox():
    r = requests.get('http://data.mtgox.com/api/2/BTCUSD/money/ticker_fast')
    data = r.json()['data']
    spot = data['last']['value']
    ask = data['buy']['value']
    bid = data['sell']['value']
    return enqueue_write('MtGox', spot, ask, bid, datetime.utcnow())



