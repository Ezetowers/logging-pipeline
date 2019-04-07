import sys
sys.path.append('../')

from common.string_socket import StringSocket
from wrappers import LogRow, ReadInfo

STATIC_FIELD_SIZE = 3
TIMESTAMP_FIELD_SIZE = 5

'''A worker socket aware of the difficult lifes of the employees'''
class WorkerSocket(StringSocket):
    def __init__(self, skt=None):
        super().__init__(skt)

    def accept(self):
        new_skt, addr = self.skt.accept()
        return WorkerSocket(new_skt), addr

    def receive_write_info(self):
        appId = super().receiveall(STATIC_FIELD_SIZE)
        timestamp = super().receiveall(TIMESTAMP_FIELD_SIZE)
        msg = super().receive_with_size(STATIC_FIELD_SIZE)
        tags = super().receive_with_size(STATIC_FIELD_SIZE)

        return LogRow(appId, msg, tags, timestamp)

    def receive_read_info(self):
        appId = super().receiveall(STATIC_FIELD_SIZE)
        from_time = super().receiveall(TIMESTAMP_FIELD_SIZE)
        to_time = super().receiveall(TIMESTAMP_FIELD_SIZE)
        tags = super().receive_with_size(STATIC_FIELD_SIZE)

        return ReadInfo(appId, from_time, to_time, tags)

    def send_write_confirmation(self):
        super().sendall("ok")

    def send_read_info(self, logs):
        super().sendall(str(len(logs)).zfill(5))
        for log in logs:
            super().sendall(log.get_appId())
            super().sendall(log.get_timestamp())
            super().send_with_size(log.get_msg())
            super().send_with_size(log.get_tags())
