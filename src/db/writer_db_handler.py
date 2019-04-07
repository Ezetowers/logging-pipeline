from db_handler import DbHandler
from workers import WriterWorker

class WriterDbHandler(DbHandler):
    def __init__(self, logs, host, port):
        super().__init__(logs, host, port)

    def _spawn_worker(self, reading_requests):
        worker = WriterWorker(self.logs, reading_requests)
        worker.run()
