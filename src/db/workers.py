class WriterWorker(object):
    def __init__(self, logs, queue):
        '''logs is a dictionario of Log objects and skt a socket'''
        self.logs = logs
        self.queue = queue

    def run(self):
        while True:
            skt = self.queue.get(True)
            write_info = skt.receive_write_info()
            self.logs.get_or_create_log_file_for_timestamp(write_info.get_appId(), write_info.get_timestamp()).write_log(write_info.get_timestamp(), write_info.get_tags(), write_info.get_msg())

            logs_for_tags = self.logs.get_or_create_log_file_for_tags(write_info.get_appId(), write_info.get_tags())
            for log in logs_for_tags:
                log.write_log(write_info.get_timestamp(), write_info.get_tags(), write_info.get_msg())

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

            logs_to_read = self.logs.get_log_files(read_info.get_appId(), read_info.get_from(), read_info.get_to(), read_info.get_tags())

            logs_readed = []
            for log_to_read in logs_to_read:
                logs_readed += log_to_read.read_log(read_info.get_appId(), read_info.get_from(), read_info.get_to(), read_info.get_tags())

            skt.send_logs(logs_readed)
            skt.close()
