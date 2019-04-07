import sys
sys.path.append('../../')

import json

from common.wrappers import ReadInfo, LogRow

def from_json_to_read_info(json):
    return ReadInfo(json.get('appId'), json.get('from_time'), json.get('to_time'), json.get('tags'))

def from_json_to_log(json):
    return LogRow(json.get('appId'), json.get('msg'), json.get('tags'), json.get('timestamp'))

def from_log_to_json(log):
    return json.dumps({"appId" : log.get_appId(), "msg" : log.get_msg(), "tags" : log.get_tags(), "timestamp" : log.get_timestamp()})
