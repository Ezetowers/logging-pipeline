from .string_socket import StringSocket
from .wrappers import LogEntry, ReadInfo

import sys

STATIC_FIELD_SIZE = 3
TIMESTAMP_FIELD_SIZE = 26 #YYYY-MM-DD HH:MM:SS.SSSSSS
LOGS_NUMBER_FIELD_SIZE = 5
WRITE_STATUS_FIELD_SIZE = 2

'''A worker socket aware of the difficult lifes of the employees,
it is just a StringSocket with enhanced options'''
class WorkerSocket(StringSocket):
    def __init__(self, skt=None):
        '''Initializer for the WorkerSocket, if no socket is given,
        a new one of type TCP is created'''
        super().__init__(skt)

    def accept(self):
        '''Accepts a new connection, a new WorkerSocket and
        the connected address is returned'''
        new_skt, addr = self.skt.accept()
        return WorkerSocket(new_skt), addr

    def receive_write_info(self):
        '''Receives write information and returns a LogEntry object'''
        appId = super().receiveall(STATIC_FIELD_SIZE)
        timestamp = super().receiveall(TIMESTAMP_FIELD_SIZE)
        msg = super().receive_with_size(STATIC_FIELD_SIZE)
        tags = super().receive_with_size(STATIC_FIELD_SIZE)

        return LogEntry(appId, msg, tags, timestamp)

    def receive_read_info(self):
        '''Receives read information and returns a ReadInfo object'''
        appId = super().receiveall(STATIC_FIELD_SIZE)
        from_time = super().receiveall(TIMESTAMP_FIELD_SIZE)
        to_time = super().receiveall(TIMESTAMP_FIELD_SIZE)
        tags = super().receive_with_size(STATIC_FIELD_SIZE)
        pattern = super().receive_with_size(STATIC_FIELD_SIZE)

        return ReadInfo(appId, from_time, to_time, tags, pattern)

    def send_read_info(self, read_info):
        '''Sends all the information of a ReadInfo object'''
        super().sendall(read_info.get_appId())
        super().sendall(read_info.get_from())
        super().sendall(read_info.get_to())
        super().send_with_size(read_info.get_tags())
        super().send_with_size(read_info.get_pattern())

    def send_write_confirmation(self):
        '''Send a message to confirm a successful write'''
        super().sendall("ok")

    def send_log(self, log):
        '''Sends all the information of a LogEntry object'''
        super().sendall(log.get_appId())
        super().sendall(log.get_timestamp())
        super().send_with_size(log.get_msg())
        super().send_with_size(log.get_tags())

    def send_logs(self, logs):
        '''Sends all the information of a list LogEntry objects'''
        super().sendall(str(len(logs)).zfill(LOGS_NUMBER_FIELD_SIZE))
        for log in logs:
            self.send_log(log)

    def receive_logs(self):
        '''Receives a size and then a collection of size size of
        LogEntry objects'''
        logs = []

        size = int(super().receiveall(LOGS_NUMBER_FIELD_SIZE))
        for x in range(size):
            appId = super().receiveall(STATIC_FIELD_SIZE)
            timestamp = super().receiveall(TIMESTAMP_FIELD_SIZE)
            msg = super().receive_with_size(STATIC_FIELD_SIZE)
            tags = super().receive_with_size(STATIC_FIELD_SIZE)

            logs.append(LogEntry(appId, msg, tags, timestamp))

        return logs

    def receive_write_status(self):
        '''Receives a write confirmation'''
        return super().receiveall(WRITE_STATUS_FIELD_SIZE)
