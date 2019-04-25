#Entry point for the database server of the logging pipeline
import os
import signal
from multiprocessing.managers import SyncManager

from log_file_manager import LogFileManager
from db_handlers import ReaderDbHandler, WriterDbHandler

HOST = '0.0.0.0'
WRITER_PORT = 6061
READER_PORT = 6071

class DbServer(object):
    def __init__(self, number_of_workers, number_of_queued_connections):
        SyncManager.register('LogFileManager', LogFileManager)
        manager = SyncManager()
        manager.start()
        logs = manager.LogFileManager()

        self.writer = WriterDbHandler(logs, number_of_workers, number_of_queued_connections, HOST, WRITER_PORT)
        self.reader = ReaderDbHandler(logs, number_of_workers, number_of_queued_connections, HOST, READER_PORT)

    def quit(self, sig_num, frame):
        pid_reader = self.reader.pid
        pid_writer = self.writer.pid
        os.kill(pid_reader, signal.SIGTERM)
        os.kill(pid_writer, signal.SIGTERM)
        self.reader.join()
        self.writer.join()

    def run(self):
        self.reader.start()
        self.writer.start()

        signal.signal(signal.SIGTERM, self.quit)
        signal.signal(signal.SIGINT, self.quit)

        signal.pause()

if __name__ == '__main__':
    number_of_workers = 4 #int(os.environ['NUMBER_OF_THREADS'])
    number_of_queued_connections = 10 #int(os.environ['MAX_QUEUED_CONNECTIONS'])

    server = DbServer(number_of_workers, number_of_queued_connections)
    server.run()
