import multiprocessing
import csv
import sys

sys.path.append('../')
from common.wrappers import LogRow

class Log(object):
    def __init__(self, log_file_name):
        self.lock = multiprocessing.Lock()
        self.log_file_name = log_file_name

    def write_log(self, timestamp, tags, msj):
        self.lock.acquire()
        try:
            with open(self.log_file_name, mode='a') as log_file:
                log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                if (not log_file.tell()):
                    log_writer.writerow(["timestamp", "tags", "msj"])

                log_writer.writerow([timestamp, tags, msj])
        finally:
            self.lock.release()

    def read_log(self, appId):
        self.lock.acquire()
        try:
            logs = []
            with open(self.log_file_name, mode='r') as log_file:
                log_reader = csv.DictReader(log_file)
                for row in log_reader:
                    log = LogRow(appId, row["msj"], row["tags"], row["timestamp"])
                    logs.append(log)
                return logs
        finally:
            self.lock.release()
