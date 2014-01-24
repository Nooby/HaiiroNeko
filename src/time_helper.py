from datetime import datetime

def start_minute(dt):
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0, 0, dt.tzinfo)

def start_hour(dt):
    return datetime(dt.year, dt.month, dt.day, dt.hour, 0, 0, 0, dt.tzinfo)

