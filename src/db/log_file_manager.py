import threading

from log_file import LogFile
import parser

EMPTY_TIMESTAMP = "                          "

class LogFileManager(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.log_files = {}

    def has_log_file(self, appId, timestamp):
        day = parser.get_day_from_timestamp(timestamp)
        return (appId in self.log_files) and (day in self.log_files[appId])

    def _add_log_file(self, appId, timestamp):
        day = parser.get_day_from_timestamp(timestamp)
        if (not appId in self.log_files):
            self.log_files[appId] = {}
        self.log_files[appId][day] = LogFile("{}_{}_log.csv".format(appId, day))

    def _get_log_file(self, appId, timestamp):
        return self.log_files.get(appId).get(parser.get_day_from_timestamp(timestamp))

    def get_or_create_log_file(self, appId, timestamp):
        self.lock.acquire()
        try:
            if not self.has_log_file(appId, timestamp):
                self._add_log_file(appId, timestamp)
            return self._get_log_file(appId, timestamp)
        finally:
            self.lock.release()

    def get_log_files_between_range(self, appId, from_timestamp, to_timestamp):
        self.lock.acquire()
        try:
            logs = []
            days = parser.get_all_days_from_range(from_timestamp, to_timestamp)

            for day in days:
                if self.has_log(appId, day):
                    logs.append(self._get_log(appId, day))

            return days
        finally:
            self.lock.release()

    def get_log_files_from_timestamp(self, appId, from_timestamp):
        self.lock.acquire()
        try:
            logs_from_timestamp = []
            logs = self.log_files.get(appId, {})

            print(self.log_files)
            print(self.log_files.get(appId, {}))

            for timestamp in logs:
                if timestamp >= parser.get_day_from_timestamp(from_timestamp):
                    logs_from_timestamp.append(logs[timestamp])

            return logs_from_timestamp
        finally:
            self.lock.release()

    def get_log_files_to_timestamp(self, appId, to_timestamp):
        self.lock.acquire()
        try:
            logs_to_timestamp = []
            logs = self.log_files.get(appId, {})

            for timestamp in logs:
                if timestamp <= parser.get_day_from_timestamp(to_timestamp):
                    logs_to_timestamp.append(logs[timestamp])

            return logs_to_timestamp
        finally:
            self.lock.release()

    def _get_all_log_files(self, appId):
        self.lock.acquire()
        try:
            return self.log_files.get(appId, {}).values()
        finally:
            self.lock.release()

    def get_log_files(self, appId, from_timestamp, to_timestamp):
        print("Mis timestamps son: {} y {}".format(from_timestamp, to_timestamp))
        if (from_timestamp == EMPTY_TIMESTAMP and to_timestamp == EMPTY_TIMESTAMP):
            print("---------------------------Devuelvo todos los logs----------------------------------")
            return self._get_all_log_files(appId)

        if (from_timestamp == EMPTY_TIMESTAMP):
            print("---------------------------Devuelvo los logs hasta el timestamp----------------------------------")
            return self.get_log_files_to_timestamp(appId, to_timestamp)

        if (to_timestamp == EMPTY_TIMESTAMP):
            print("---------------------------Devuelvo los logs hasta el timestamp----------------------------------")
            return self.get_log_files_from_timestamp(appId, from_timestamp)

        print("---------------------------Devuelvo los logs en el rango----------------------------------")
        return self.get_log_files_between_range(appId, from_timestamp, to_timestamp)
