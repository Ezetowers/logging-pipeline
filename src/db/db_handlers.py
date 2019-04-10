import sys
sys.path.append('../')

import threading
import queue

NUM_THREADS = 2

from workers import WriterWorker, ReaderWorker
from common.worker_socket import WorkerSocket

class DbHandler(threading.Thread):
    def __init__(self, logs, host, port):
        threading.Thread.__init__(self)
        self.logs = logs
        self.host = host
        self.port = port
        self.skt = WorkerSocket()
        self.keep_running = True

    def _spawn_worker(self, reading_requests):
        raise NotImplementedError("Abstract method!")

    def run(self):
        requests = queue.Queue()

        self.skt.bind(self.host, self.port)
        self.skt.listen()

        workers = []

        for i in range(NUM_THREADS):
            worker = self._spawn_worker(requests)
            worker.setDaemon(True)
            worker.start()
            workers.append(worker)

        while self.keep_running:
            print("Estoy por aceptar")
            request_skt, addr = self.skt.accept()
            print("Ya acepte")
            requests.put(request_skt)

        print("salgo del loop")

        while not requests.empty():
            requests.get().close()

        for worker in workers:
            worker.stop()
        for worker in workers:
            worker.join()

        print("termine")

    def stop(self):
        print("Estoy en el stop de los handlers")
        self.keep_running = False
        self.skt.settimeout(0.1)
        self.skt.close()
        print(self.keep_running)

class WriterDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, writing_requests):
        return WriterWorker(self.logs, writing_requests)

class ReaderDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, reading_requests):
        return ReaderWorker(self.logs, reading_requests)
