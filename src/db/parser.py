import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f' #YYYY-MM-DD HH:MM:SS.SSSSSS

def get_date_from_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)

def get_day_from_timestamp(timestamp):
    return get_date_from_timestamp(timestamp).date()

def get_all_days_from_range(from_timestamp, to_timestamp):
    days = []
    from_timestamp = get_date_from_timestamp(from_timestamp)
    to_timestamp = get_date_from_timestamp(to_timestamp)
    delta = from_timestamp - to_timestamp
    for i in range(delta.days + 1):
        days.append(from_timestamp + datetime.delta(i))
    return days
