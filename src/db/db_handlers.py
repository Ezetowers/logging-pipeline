import sys
sys.path.append('../')

import errno
import multiprocessing

from workers import WriterWorker, ReaderWorker
from common.worker_socket import WorkerSocket

'''A base database handler that receives incomming connections and spawns
threads for processing them'''
class DbHandler(multiprocessing.Process):
    def __init__(self, logs, number_of_workers, number_of_queued_connections, host, port):
        '''Initializer for the DbHandler object, it takes a LogFileManager,
        the number of workers that it has, the number of maximum queued
        connections, a host and a port to listen to'''
        multiprocessing.Process.__init__(self)

        self.logs = logs
        self.host = host
        self.port = port
        self.skt = WorkerSocket()
        self.keep_running = True
        self.number_of_workers = number_of_workers
        self.number_of_queued_connections = number_of_queued_connections

    def _spawn_worker(self, reading_requests):
        '''Returns a thread to use everytime a connections is accepted'''
        raise NotImplementedError("Abstract method!")

    def run(self):
        '''Run function, it accepts connections and spawns threads with
        that new connections'''
        requests = multiprocessing.Queue()

        self.skt.bind(self.host, self.port)
        self.skt.listen(self.number_of_queued_connections)

        workers = []

        for i in range(self.number_of_workers):
            worker = self._spawn_worker(requests)
            #worker.daemon = True
            worker.start()
            workers.append(worker)

        while self.keep_running:
            try:
                request_skt, addr = self.skt.accept()
                requests.put(request_skt)
            except IOError as serr:
                if serr.errno != errno.EINVAL:
                    raise serr

        while not requests.empty():
            requests.get().close()

        for worker in workers:
            requests.put(None)

        for worker in workers:
            worker.join()

    def stop(self):
        '''Tells the DbHandler to stop its execution'''
        self.keep_running = False
        self.skt.close()

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
