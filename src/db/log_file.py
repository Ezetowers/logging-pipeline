import fcntl
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

'''Class that implements safe writes and reads for a file'''
class LogFile(object):
    def __init__(self, log_file_name):
        '''Initializer for the LogFile, it takes a name for its file'''
        self.log_file_name = log_file_name

    def write_log(self, timestamp, tags, msj):
        '''Writes a log to its file'''
        with open(self.log_file_name, mode='a') as log_file:
            fcntl.flock(log_file, fcntl.LOCK_EX)

            log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if (not log_file.tell()):
                log_writer.writerow([TIMESTAMP_COL, TAGS_COL, MSJ_COL])

            log_writer.writerow([timestamp, tags, msj])

            fcntl.flock(log_file, fcntl.LOCK_UN)

    def read_log(self, appId, from_timestamp, to_timestamp, tag):
        '''Returns the all the LogEntry objects of id appId, that are between
        from_timestamp date to to_timestamp date and have the given tag'''
        with open(self.log_file_name, mode='r+') as log_file:
            logs = []
            fcntl.flock(log_file, fcntl.LOCK_SH)

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

            fcntl.flock(log_file, fcntl.LOCK_UN)
            return logs
