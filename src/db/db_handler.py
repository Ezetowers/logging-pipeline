import multiprocessing

from worker_socket import WorkerSocket

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
            reading_requests.put(reader_skt)
