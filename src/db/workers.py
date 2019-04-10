import threading

'''A thread that gets connected sockets from a queue and writes to a log
regarding the information received'''
class WriterWorker(threading.Thread):
    def __init__(self, logs, queue):
        '''Initializer for the WriterWorker, it receives a LogFileManager
        and a blocking Queue'''
        threading.Thread.__init__(self)
        self.logs = logs
        self.queue = queue
        self.keep_running = True

    def run(self):
        '''Run function, it gets connected sockets from its queue and then
        writes the requested information'''
        while self.keep_running:
            skt = self.queue.get(True)
            write_info = skt.receive_write_info()
            self.logs.get_or_create_log_file_for_timestamp(write_info.get_appId(), write_info.get_timestamp()).write_log(write_info.get_timestamp(), write_info.get_tags(), write_info.get_msg())

            logs_for_tags = self.logs.get_or_create_log_file_for_tags(write_info.get_appId(), write_info.get_tags())
            for log in logs_for_tags:
                log.write_log(write_info.get_timestamp(), write_info.get_tags(), write_info.get_msg())

            skt.send_write_confirmation()
            skt.close()

    def stop(self):
        '''Tells the worker to stop its execution'''
        self.keep_running = False

'''A thread that gets connected sockets from a queue and reads from a log
regarding the information received'''
class ReaderWorker(threading.Thread):
    def __init__(self, logs, queue):
        '''Initializer for the ReaderWorker, it receives a LogFileManager
        and a blocking Queue'''
        threading.Thread.__init__(self)
        self.logs = logs
        self.queue = queue
        self.keep_running = True

    def run(self):
        '''Run function, it gets connected sockets from its queue and then
        sends the readed requested information'''
        while self.keep_running:
            skt = self.queue.get(True)
            read_info = skt.receive_read_info()

            logs_to_read = self.logs.get_log_files(read_info.get_appId(), read_info.get_from(), read_info.get_to(), read_info.get_tags())

            logs_readed = []
            for log_to_read in logs_to_read:
                logs_readed += log_to_read.read_log(read_info.get_appId(), read_info.get_from(), read_info.get_to(), read_info.get_tags())

            skt.send_logs(logs_readed)
            skt.close()

    def stop(self):
        '''Tells the worker to stop its execution'''
        self.keep_running = False
