import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f' #YYYY-MM-DD HH:MM:SS.SSSSSS

def get_datetime_from_timestamp(timestamp):
    '''Given a datetime in string form, it return a datetime object'''
    return datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)

def get_day_from_timestamp(timestamp):
    '''Returns the date of a timestamp given in string format'''
    return get_datetime_from_timestamp(timestamp).date()
