import sys
sys.path.append('../../')

from common.wrappers import ReadInfo, LogEntry

def from_json_to_read_info(data):
    '''Returns a ReadInfo object from a json and an appId'''
    return ReadInfo(data.get('appId'), data.get('from'), data.get('to'), data.get('tags'), data.get('pattern'))

def from_json_to_log(data):
    '''Creates a LogEntry object from a json and an appId'''
    return LogEntry(data.get('appId'), data.get('msg'), data.get('tags'), data.get('timestamp'))

def from_log_to_json(log):
    '''Creates a json with the information of a LogEntry object'''
    return {"appId" : log.get_appId(), "msg" : log.get_msg(), "tags" : log.get_tags(), "timestamp" : log.get_timestamp()}
