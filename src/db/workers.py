class WriterWorker(object):
    def __init__(self, logs, skt):
        '''logs is a dictionario of Log objects and skt a socket'''
        self.logs = logs
        self.skt = skt

    def run():
        while True:
            write_info = self.skt.receive_write_info()
            logs[write_info.get_appId()].write_log(write_info.get_timestamp(), write_info.get_tags(), write_info.get_msg())
            self.skt.send_write_confirmation()

class ReaderWorker(object):
    def __init__(self, logs, skt):
        '''logs is a dictionario of Log objects and skt a socket'''
        self.logs = logs
        self.skt = skt

    def run():
        while True:
            read_info = self.skt.receive_read_info()
            logs_readed = logs[read_info.get_appId()].read_log(read_info.get_appId())
            self.skt.send_read_info(logs_readed)
