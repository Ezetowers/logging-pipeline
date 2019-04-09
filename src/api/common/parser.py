import sys
sys.path.append('../../')

import json

from common.wrappers import ReadInfo, LogEntry

def from_json_to_read_info(json, appId):
    return ReadInfo(appId, json.get('from'), json.get('to'), json.get('tags'), json.get('pattern'))

def from_json_to_log(appId, json):
    return LogEntry(appId, json.get('msg'), json.get('tags'), json.get('timestamp'))

def from_log_to_json(log):
    return json.dumps({"appId" : log.get_appId(), "msg" : log.get_msg(), "tags" : log.get_tags(), "timestamp" : log.get_timestamp()})
