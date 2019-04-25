import sys
sys.path.append('../')

import errno
import multiprocessing

from workers import WriterWorker, ReaderWorker
from common.worker_socket import WorkerSocket
from common.connection_handler import ConnectionHandler

'''A base database handler that receives incomming connections and spawns
threads for processing them'''
class DbHandler(ConnectionHandler):
    def __init__(self, logs, number_of_workers, number_of_queued_connections, host, port):
        '''Initializer for the DbHandler object, it takes a LogFileManager,
        the number of workers that it has, the number of maximum queued
        connections, a host and a port to listen to'''
        super().__init__(number_of_workers, number_of_queued_connections, host, port)
        self.logs = logs

'''A DbHandler that spawns WriterWorker threads'''
class WriterDbHandler(DbHandler):
    def __init__(self, logs, number_of_workers, number_of_queued_connections, host, port):
        super().__init__(logs, number_of_workers, number_of_queued_connections, host, port)

    def _spawn_worker(self, writing_requests):
        return WriterWorker(self.logs, writing_requests)

'''A DbHandler that spawns ReaderWorker threads'''
class ReaderDbHandler(DbHandler):
    def __init__(self, logs, number_of_workers, number_of_queued_connections, host, port):
        super().__init__(logs, number_of_workers, number_of_queued_connections, host, port)

    def _spawn_worker(self, reading_requests):
        return ReaderWorker(self.logs, reading_requests)
