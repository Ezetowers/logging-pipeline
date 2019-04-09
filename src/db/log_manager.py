import threading

from log import Log

class LogManager(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.logs = {}

    def has_log(self, appId):
        return (appId in self.logs)

    def _add_log(self, appId):
        self.logs[appId] = Log("{}_log.csv".format(appId))

    def get_log(self, appId):
        self.lock.acquire()
        try:
            if not self.has_log(appId):
                self._add_log(appId)
            return self.logs.get(appId)
        finally:
            self.lock.release()
