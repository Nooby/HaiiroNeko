import pymongo

from database import db

ticks = db['ticks']
ticks.ensure_index('Time')
ticks.ensure_index('Exchange')

def write(exchange, spot, bid, ask, time):
    doc = {
        "Exchange": exchange,
        "Spot": spot,
        "Ask": ask,
        "Bid": bid,
        "Time": time }
    ticks.insert(doc, safe=True)

def count():
    return ticks.count()

def oldest():
    return ticks.find().sort([('Time', pymongo.ASCENDING)]).limit(1).next()

def newest():
    return ticks.find().sort([('Time', pymongo.DESCENDING)]).limit(1).next()

def get_exchange_names():
    return ticks.distinct('Exchange')

def get_spot(exchange, limit):
    cursor = ticks.find({'Exchange': exchange, 'Time': {'$gte': limit}})

    return list(cursor)


