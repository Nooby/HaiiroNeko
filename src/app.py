from web import app
from rq_helper.schedule import schedule_ticker_querys
from btc.api_clients import get_bitstamp, get_bitfinex, get_coinbase, get_kraken, get_mtgox

schedule_ticker_querys((get_bitstamp, get_bitfinex, get_coinbase, get_kraken, get_mtgox))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
