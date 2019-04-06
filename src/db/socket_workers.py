STATIC_FIELD_SIZE = 3
TIMESTAMP_FIELD_SIZE = 5

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

class SocketWorkers(object):
    def __init__(self, skt):
        self.skt = skt

    def receive_write_info(self):
        appId = self._receive(STATIC_FIELD_SIZE)
        timestamp = self._receive(TIMESTAMP_FIELD_SIZE)
        msg = self._receive_with_size()
        tags = self._receive_with_size()

        return LogRow(appId, msg, tags, timestamp)

    def receive_read_info(self):
        appId = self._receive(STATIC_FIELD_SIZE)
        from_time = self._receive(TIMESTAMP_FIELD_SIZE)
        to_time = self._receive(TIMESTAMP_FIELD_SIZE)
        tags = self._receive_with_size()

        return ReadInfo(appId, from_time, to_time, tags)

    def send_write_confirmation(self):
        self.sendall("ok".encode())

    def send_read_info(self, logs):
        for log in logs:
            self.skt.sendall(log.get_appId().encode())
            self.skt.sendall(log.get_timestamp().encode())
            self._send_with_size(log.get_msg())
            self._send_with_size(log.get_tags())

    def _send_with_size(self, msg):
        self.skt.sendall(str(len(msg)).zfill(3).encode())
        self.skt.sendall(msg.encode())

    def _receive(self, msg_len):
        msg = ""
        while len(msg) < msg_len:
            chunk = self.skt.recv(msg_len-len(msg))
            if not chunk:
                raise RuntimeError('Lal')
            msg = msg + chunk.decode('UTF-8', 'ignore')
        return msg

    def _receive_with_size(self):
        field_size = self._receive(STATIC_FIELD_SIZE)
        return self._receive(int(field_size))
