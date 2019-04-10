import threading

from log_file import LogFile
import parser

EMPTY_TIMESTAMP = "                          "
EMPTY_TAGS = " "

'''A manager for a collection of LogFile objects'''
class LogFileManager(object):
    def __init__(self):
        '''Initializer for a LogFileManager'''
        self.lock = threading.Lock()
        self.log_files = {}

    def has_log_file_for_timestamp(self, appId, timestamp):
        '''Returns true if the LogFileManager has a LogFile for the given
        timestamp and appId'''
        day = parser.get_day_from_timestamp(timestamp)
        return (appId in self.log_files) and (day in self.log_files[appId]["days"])

    def has_log_file_for_tag(self, appId, tag):
        '''Returns true if the LogFileManager has a LogFile for the given
        tag and appId'''
        return (appId in self.log_files) and (tag in self.log_files[appId]["tags"])

    def get_or_create_log_file_for_timestamp(self, appId, timestamp):
        '''Gets the LogFile for a given timestamp and appId, if there is no one,
        one is created and then returned'''
        self.lock.acquire()
        try:
            if not self.has_log_file_for_timestamp(appId, timestamp):
                self._add_log_file_for_timestamp(appId, timestamp)
            return self._get_log_file_for_timestamp(appId, timestamp)
        finally:
            self.lock.release()

    def _add_log_file_for_timestamp(self, appId, timestamp):
        day = parser.get_day_from_timestamp(timestamp)
        if (not appId in self.log_files):
            self.log_files[appId] = {"tags" : {}, "days" : {}}
        self.log_files[appId]["days"][day] = LogFile("{}_{}_log.csv".format(appId, day))

    def _get_log_file_for_timestamp(self, appId, timestamp):
        return self.log_files.get(appId).get("days").get(parser.get_day_from_timestamp(timestamp))

    def get_or_create_log_file_for_tags(self, appId, tags):
        '''Gets the LogFiles for a given set of tags and appId, if there is no
        one for at least one of them, they are created and then returned'''
        self.lock.acquire()
        try:
            log_files = []
            for tag in tags.split(" "):
                if not self.has_log_file_for_tag(appId, tag):
                    self._add_log_file_for_tag(appId, tag)
                log_files.append(self._get_log_file_for_tag(appId, tag))
            return log_files
        finally:
            self.lock.release()

    def _add_log_file_for_tag(self, appId, tag):
        if (not appId in self.log_files):
            self.log_files[appId] = {"tags" : {}, "days" : []}
        self.log_files[appId]["tags"][tag] = LogFile("{}_{}_log.csv".format(appId, tag))

    def _get_log_file_for_tag(self, appId, tag):
        return self.log_files.get(appId).get("tags").get(tag)

    def get_log_files(self, appId, from_timestamp, to_timestamp, tag):
        '''Gets all the LogFiles for a given appId, a set of tags and between
        a range of timestamps'''
        if (from_timestamp == EMPTY_TIMESTAMP and to_timestamp == EMPTY_TIMESTAMP):
            if (tag != EMPTY_TAGS):
                return self._get_log_files_for_tag(appId, tag)
            return self._get_all_log_files(appId)

        if (from_timestamp == EMPTY_TIMESTAMP):
            return self._get_log_files_to_timestamp(appId, to_timestamp)

        if (to_timestamp == EMPTY_TIMESTAMP):
            return self._get_log_files_from_timestamp(appId, from_timestamp)

        return self._get_log_files_between_range(appId, from_timestamp, to_timestamp)

    def _get_log_files_for_tag(self, appId, tag):
        self.lock.acquire()
        try:
            if (self.has_log_file_for_tag(appId, tag)):
                return [self.log_files.get(appId).get("tags").get(tag)]
            return []
        finally:
            self.lock.release()

    def _get_all_log_files(self, appId):
        self.lock.acquire()
        try:
            return self.log_files.get(appId, {}).get("days", {}).values()
        finally:
            self.lock.release()

    def _get_log_files_to_timestamp(self, appId, to_timestamp):
        self.lock.acquire()
        try:
            logs_to_timestamp = []
            to_timestamp = parser.get_day_from_timestamp(to_timestamp)
            logs = self.log_files.get(appId, {}).get("days", {})

            for timestamp in logs:
                if timestamp <= to_timestamp:
                    logs_to_timestamp.append(logs[timestamp])

            return logs_to_timestamp
        finally:
            self.lock.release()

    def _get_log_files_from_timestamp(self, appId, from_timestamp):
        self.lock.acquire()
        try:
            logs_from_timestamp = []
            from_timestamp = parser.get_day_from_timestamp(from_timestamp)
            logs = self.log_files.get(appId, {}).get("days", {})

            for timestamp in logs:
                if timestamp >= from_timestamp:
                    logs_from_timestamp.append(logs[timestamp])

            return logs_from_timestamp
        finally:
            self.lock.release()

    def _get_log_files_between_range(self, appId, from_timestamp, to_timestamp):
        self.lock.acquire()
        try:
            logs_from_timestamp = []
            from_timestamp = parser.get_day_from_timestamp(from_timestamp)
            to_timestamp = parser.get_day_from_timestamp(to_timestamp)
            logs = self.log_files.get(appId, {}).get("days", {})

            for timestamp in logs:
                if timestamp >= from_timestamp and timestamp <= to_timestamp:
                    logs_from_timestamp.append(logs[timestamp])

            return logs_from_timestamp
        finally:
            self.lock.release()
