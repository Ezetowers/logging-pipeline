import os
import signal
import sys
sys.path.append('../')

from common.web_servers import GetServer

HOST = '0.0.0.0'
PORT = 6070

if __name__ == '__main__':
    number_of_workers = 4 #int(os.environ['NUMBER_OF_THREADS'])
    number_of_queued_connections = 10 #int(os.environ['MAX_QUEUED_CONNECTIONS'])

    server = GetServer(number_of_workers, number_of_queued_connections, HOST, PORT)
    server.run()
