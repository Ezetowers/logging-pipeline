EMPTY_TIMESTAMP = "                          "
EMPTY_TAGS = " "
EMPTY_PATTERN = " "

'''A wrapper for a log entry, just with getters'''
class LogEntry(object):
    def __init__(self, appId, msg, tags, timestamp):
        self.appId = appId
        self.msg = msg
        self.tags = tags
        self.timestamp = timestamp

    def get_tags(self):
        return self.tags

    def get_appId(self):
        return self.appId

    def get_timestamp(self):
        return self.timestamp

    def get_msg(self):
        return self.msg

'''A wrapper for the information needed to read a log, just with getters'''
class ReadInfo(object):
    def __init__(self, appId, from_time, to_time, tags, pattern):
        self.appId = appId
        self.from_time = from_time if from_time else EMPTY_TIMESTAMP
        self.to_time = to_time if to_time else EMPTY_TIMESTAMP
        self.tags = tags if tags else EMPTY_TAGS
        self.pattern = pattern if pattern else EMPTY_PATTERN

    def get_tags(self):
        return self.tags

    def get_appId(self):
        return self.appId

    def get_to(self):
        return self.to_time

    def get_from(self):
        return self.from_time

    def get_pattern(self):
        return self.pattern
