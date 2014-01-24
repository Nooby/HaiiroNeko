from rq import Connection, Queue
from redis import Redis

redis_conn = Redis()

BTC = Queue('btc', connection=redis_conn)
DATA = Queue('data', connection=redis_conn)

