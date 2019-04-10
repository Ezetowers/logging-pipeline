import threading
import csv
import sys

import parser

sys.path.append('../')
from common.wrappers import LogEntry

TIMESTAMP_COL = "timestamp"
TAGS_COL = "field"
MSJ_COL = "msj"
EMPTY_TIMESTAMP = "                          "
EMPTY_TAGS = " "

class LogFile(object):
    def __init__(self, log_file_name):
        self.lock = threading.Lock()
        self.log_file_name = log_file_name

    def write_log(self, timestamp, tags, msj):
        self.lock.acquire()
        try:
            with open(self.log_file_name, mode='a') as log_file:
                log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                if (not log_file.tell()):
                    log_writer.writerow([TIMESTAMP_COL, TAGS_COL, MSJ_COL])

                log_writer.writerow([timestamp, tags, msj])
        finally:
            self.lock.release()

    def read_log(self, appId, from_timestamp, to_timestamp, tag):
        self.lock.acquire()
        try:
            logs = []
            with open(self.log_file_name, mode='r') as log_file:
                log_reader = csv.DictReader(log_file)
                for row in log_reader:
                    log = LogEntry(appId, row[MSJ_COL], row[TAGS_COL], row[TIMESTAMP_COL])
                    log_timestamp = parser.get_datetime_from_timestamp(log.get_timestamp())
                    log_tags = log.get_tags().split(" ")

                    if (from_timestamp != EMPTY_TIMESTAMP and log_timestamp < parser.get_datetime_from_timestamp(from_timestamp)):
                        continue

                    if (to_timestamp != EMPTY_TIMESTAMP and log_timestamp > parser.get_datetime_from_timestamp(to_timestamp)):
                        continue

                    if (tag != EMPTY_TAGS and tag not in log_tags):
                        continue

                    logs.append(log)

                return logs
        finally:
            self.lock.release()
