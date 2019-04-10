def is_log_valid(log):
    '''Returns if a LogEntry object is valid, that is to say,
    that all its attributes are different that None'''
    return not((not log.get_appId()) or (not log.get_msg()) or (not log.get_tags()) or (not log.get_timestamp()))
