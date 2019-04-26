import sys
sys.path.append('../')

import errno
import multiprocessing

from workers import WriterWorker, ReaderWorker
from common.worker_socket import WorkerSocket
from common.connection_handler import ConnectionHandler

'''A DbHandler that spawns WriterWorker threads'''
class WriterDbHandler(ConnectionHandler):
    def __init__(self, logs, number_of_workers, number_of_queued_connections, host, port):
        super().__init__(number_of_workers, number_of_queued_connections, host, port)
        self.logs = logs

    def _spawn_worker(self, writing_requests, finished_requests):
        return WriterWorker(self.logs, writing_requests, finished_requests)

'''A DbHandler that spawns ReaderWorker threads'''
class ReaderDbHandler(ConnectionHandler):
    def __init__(self, logs, number_of_workers, number_of_queued_connections, host, port):
        super().__init__(number_of_workers, number_of_queued_connections, host, port)
        self.logs = logs

    def _spawn_worker(self, reading_requests, finished_requests):
        return ReaderWorker(self.logs, reading_requests, finished_requests)
