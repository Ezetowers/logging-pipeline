import sys
sys.path.append('../')

import threading
import queue

NUM_THREADS = 2

from workers import WriterWorker, ReaderWorker
from common.worker_socket import WorkerSocket

class DbHandler(object):
    def __init__(self, logs, host, port):
        self.logs = logs
        self.host = host
        self.port = port

    def _spawn_worker(self, reading_requests):
        raise NotImplementedError("Abstract method!")

    def run(self):
        requests = queue.Queue()

        skt = WorkerSocket()
        skt.bind(self.host, self.port)
        skt.listen()

        for i in range(NUM_THREADS):
            worker = threading.Thread(target=self._spawn_worker, args=(requests,))
            worker.setDaemon(True)
            worker.start()

        while True:
            print("---------------------------Acepto una conexion----------------------------------")
            request_skt, addr = skt.accept()
            requests.put(request_skt)

class WriterDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, writing_requests):
        worker = WriterWorker(self.logs, writing_requests)
        worker.run()

class ReaderDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, reading_requests):
        worker = ReaderWorker(self.logs, reading_requests)
        worker.run()
