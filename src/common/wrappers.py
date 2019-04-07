class LogRow(object):
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

class ReadInfo(object):
    def __init__(self, appId, from_time, to_time, tags):
        self.appId = appId
        self.from_time = from_time
        self.to_time = to_time
        self.tags = tags

    def get_tags(self):
        return self.tags

    def get_appId(self):
        return self.appId

    def get_to(self):
        return self.to_time

    def get_from(self):
        return self.from_time
