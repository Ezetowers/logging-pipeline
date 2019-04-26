import os
import signal
import sys
sys.path.append('../')

from common.web_servers import PostServer

HOST = '0.0.0.0'
PORT = 6060

if __name__ == '__main__':
    number_of_workers = int(os.environ['NUMBER_OF_WORKERS_POST'])
    number_of_queued_connections = int(os.environ['MAX_QUEUED_CONNECTIONS_POST'])

    server = PostServer(number_of_workers, number_of_queued_connections, HOST, PORT)
    server.run()
