import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f' #YYYY-MM-DD HH:MM:SS.SSSSSS

def get_datetime_from_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)

def get_day_from_timestamp(timestamp):
    return get_datetime_from_timestamp(timestamp).date()
