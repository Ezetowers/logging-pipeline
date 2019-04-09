def is_log_valid(log):
    return not((not log.get_appId()) or (not log.get_msg()) or (not log.get_tags()) or (not log.get_timestamp())) 
