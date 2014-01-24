from datetime import datetime, timedelta

from rq_helper import redis_conn
from time_helper import start_minute
from rq_scheduler import Scheduler

btc_scheduler = Scheduler('btc', connection=redis_conn)

def schedule_ticker_querys(funcs):
    jobs = btc_scheduler.get_jobs()
    if len(jobs) >= len(funcs): # TODO: Test if these are the right jobs.
        return

    for f in funcs:
        btc_scheduler.schedule(
                scheduled_time=start_minute(datetime.now()) + timedelta(minutes=1), # Start at the beginning of next minute
                func=f,
                interval=60)

