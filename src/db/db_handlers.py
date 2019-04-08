import sys
sys.path.append('../')

import multiprocessing

from workers import WriterWorker, ReaderWorker
from common.worker_socket import WorkerSocket

class DbHandler(object):
    def __init__(self, logs, host, port):
        self.logs = logs
        self.host = host
        self.port = port

    def _spawn_worker(self, reading_requests):
        raise NotImplementedError("abstract method!")

    def run(self):
        reading_requests = multiprocessing.Queue()

        skt = WorkerSocket()
        skt.bind(self.host, self.port)
        skt.listen()

        readers_pool = multiprocessing.Pool(2, self._spawn_worker, (reading_requests,))

        while True:
            reader_skt, addr = skt.accept()
            print("------------------------Acepte a un gil----------------------------------")
            reading_requests.put(reader_skt)

class WriterDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, reading_requests):
        worker = WriterWorker(self.logs, reading_requests)
        worker.run()

class ReaderDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, reading_requests):
        worker = ReaderWorker(self.logs, reading_requests)
        worker.run()
