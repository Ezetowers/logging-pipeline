from db_handler import DbHandler
from workers import ReaderWorker

class ReaderDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, reading_requests):
        worker = ReaderWorker(self.logs, reading_requests)
        worker.run()
