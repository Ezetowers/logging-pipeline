import threading

from log import Log
import parser

EMPTY_TIMESTAMP = "                          "

class LogManager(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.logs = {}

    def has_log(self, appId, timestamp):
        day = parser.get_day_from_timestamp(timestamp)
        return (appId in self.logs) and (day in self.logs[appId])

    def _add_log(self, appId, timestamp):
        day = parser.get_day_from_timestamp(timestamp)
        if (not appId in self.logs):
            self.logs[appId] = {}
        self.logs[appId][day] = Log("{}_{}_log.csv".format(appId, day))

    def _get_log(self, appId, timestamp):
        return self.logs.get(appId).get(parser.get_day_from_timestamp(timestamp))

    def get_or_create_log(self, appId, timestamp):
        self.lock.acquire()
        try:
            if not self.has_log(appId, timestamp):
                self._add_log(appId, timestamp)
            return self._get_log(appId, timestamp)
        finally:
            self.lock.release()

    def get_logs_between_range(self, appId, from_timestamp, to_timestamp):
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

    def get_logs_from_timestamp(self, appId, from_timestamp):
        self.lock.acquire()
        try:
            logs_from_timestamp = []
            logs = self.logs.get(appId, [])

            for timestamp, log in logs:
                if parser.get_day_from_timestamp(timestamp) >= parser.get_day_from_timestamp(from_timestamp):
                    logs_from_timestamp.append(log)

            return logs_from_timestamp
        finally:
            self.lock.release()

    def get_logs_to_timestamp(self, appId, to_timestamp):
        self.lock.acquire()
        try:
            logs_to_timestamp = []
            logs = self.logs.get(appId, [])

            for timestamp, log in logs:
                if parser.get_day_from_timestamp(timestamp) <= parser.get_day_from_timestamp(from_timestamp):
                    logs_from_timestamp.append(log)

            return logs_to_timestamp
        finally:
            self.lock.release()

    def _get_logs(self, appId):
        self.lock.acquire()
        try:
            return self.logs.get(appId, {}).values()
        finally:
            self.lock.release()

    def get_logs(self, appId, from_timestamp, to_timestamp):
        print("Mis timestamps son: {} y {}".format(from_timestamp, to_timestamp))
        if (from_timestamp == EMPTY_TIMESTAMP and to_timestamp == EMPTY_TIMESTAMP):
            print("---------------------------Devuelvo todos los logs----------------------------------")
            return self._get_logs(appId)

        if (from_timestamp == EMPTY_TIMESTAMP):
            print("---------------------------Devuelvo los logs hasta el timestamp----------------------------------")
            return self.get_logs_to_timestamp(appId, from_timestamp)

        if (to_timestamp == EMPTY_TIMESTAMP):
            print("---------------------------Devuelvo los logs hasta el timestamp----------------------------------")
            return self.get_logs_from_timestamp(appId, from_timestamp)

        print("---------------------------Devuelvo los logs en el rango----------------------------------")
        return self.get_logs_between_range(appId, from_timestamp, to_timestamp)
