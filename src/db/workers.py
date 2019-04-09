class WriterWorker(object):
    def __init__(self, logs, queue):
        '''logs is a dictionario of Log objects and skt a socket'''
        self.logs = logs
        self.queue = queue

    def run(self):
        while True:
            skt = self.queue.get(True)
            write_info = skt.receive_write_info()
            self.logs.get_log(write_info.get_appId()).write_log(write_info.get_timestamp(), write_info.get_tags(), write_info.get_msg())
            skt.send_write_confirmation()
            skt.close()

class ReaderWorker(object):
    def __init__(self, logs, queue):
        '''logs is a dictionario of Log objects and skt a socket'''
        self.logs = logs
        self.queue = queue

    def run(self):
        while True:
            skt = self.queue.get(True)
            read_info = skt.receive_read_info()

            if (not self.logs.has_log(read_info.get_appId()))
                skt.send_logs([])
                continue

            logs_readed = self.logs.get_log(read_info.get_appId()).read_log(read_info.get_appId())
            skt.send_logs(logs_readed)
            skt.close()
