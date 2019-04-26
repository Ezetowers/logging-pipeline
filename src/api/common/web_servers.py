import sys
sys.path.append('../../')

from common.connection_handler import ConnectionHandler
from .workers import GetWorker, PostWorker

'''A ConnectionHandler that spawns GetWorker processes'''
class GetServer(ConnectionHandler):
    def __init__(self, number_of_workers, number_of_queued_connections, host, port):
        super().__init__(number_of_workers, number_of_queued_connections, host, port)

    def _spawn_worker(self, get_requests, finished_requests):
        print("--------Spawn de un GET worker-----------")
        return GetWorker(get_requests, finished_requests)

'''A ConnectionHandler that spawns PostWorker processes'''
class PostServer(ConnectionHandler):
    def __init__(self, number_of_workers, number_of_queued_connections, host, port):
        super().__init__(number_of_workers, number_of_queued_connections, host, port)

    def _spawn_worker(self, post_requests, finished_requests):
        print("--------Spawn de un POST worker-----------")
        return PostWorker(post_requests, finished_requests)
