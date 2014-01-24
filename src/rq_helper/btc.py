from rq_helper import DATA

def enqueue_write(*args, **kwargs):
    DATA.enqueue('database.Ticks.write', args=args, kwargs=kwargs)

