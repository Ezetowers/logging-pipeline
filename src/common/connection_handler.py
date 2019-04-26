import multiprocessing
import threading
import signal
import os
import uuid

from .worker_socket import WorkerSocket

class ConnectionHandlerSocketCloser(threading.Thread):
    def __init__(self, finished_sockets, sockets):
        threading.Thread.__init__(self)
        self.sockets = sockets
        self.finished_sockets = finished_sockets

    def run(self):
        while True:
            skt_to_close = self.finished_sockets.get()
            if not skt_to_close:
                break
            self.sockets.get(skt_to_close).close()

'''A connection handler that receives incomming connections and spawns
process for processing them'''
class ConnectionHandler(multiprocessing.Process):
    def __init__(self, number_of_workers, number_of_queued_connections, host, port):
        '''Initializer for the DbHandler object, it takes a LogFileManager,
        the number of workers that it has, the number of maximum queued
        connections, a host and a port to listen to'''
        multiprocessing.Process.__init__(self)

        self.host = host
        self.port = port
        self.skt = WorkerSocket()
        self.stop_running = multiprocessing.Event()
        self.number_of_workers = number_of_workers
        self.number_of_queued_connections = number_of_queued_connections

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def _spawn_worker(self, requests, finished_requests):
        '''Returns a thread to use everytime a connections is accepted'''
        raise NotImplementedError("Abstract method!")

    def run(self):
        '''Run function, it accepts connections and spawns threads with
        that new connections'''
        print("-------------Empiezo el run-----------")

        requests = multiprocessing.Queue()
        finished_requests = multiprocessing.Queue()
        sockets = {}

        self.skt.settimeout(1)

        self.skt.bind(self.host, self.port)
        print("----------------Me conecto a {}:{}-----------".format(self.host, self.port))
        self.skt.listen(self.number_of_queued_connections)
        print("----------------Escucho-----------")

        closing_worker = ConnectionHandlerSocketCloser(finished_requests, sockets)
        workers = []

        for i in range(self.number_of_workers):
            worker = self._spawn_worker(requests, finished_requests)
            #worker.daemon = True
            worker.start()
            workers.append(worker)

        closing_worker.start()

        while not self.stop_running.is_set():
            print("----------------Estoy por aceptar una conexion-----------")
            request_skt, addr = self.skt.accept()
            print("-------------Acepto una coneccion-----------")
            print("-------------Mi pid es {}--------------------".format(os.getpid()))
            print("")
            print("Mi keep_running es: {}".format(self.stop_running.is_set()))
            if not request_skt:
                continue

            socket_id = str(uuid.uuid4())
            sockets[socket_id] = request_skt

            requests.put((socket_id, request_skt))

        self.skt.close()

        print("")
        print("-----------Cerre el socket-------------")

        while not requests.empty():
            requests.get().close()

        print("")
        print("-----------Limpio los requests------------")

        for worker in workers:
            requests.put((None, None))

        finished_requests.put(None)

        print("")
        print("-----------Pongo los None------------")

        for worker in workers:
            worker.join()

        closing_worker.join()

        print("")
        print("-----------Le doy join a los workers-------------")

        print("-----------Sali-------------")

        return

    def stop(self, signum, frame):
        '''Tells the DbHandler to stop its execution'''
        self.stop_running.set()
        print("Recibi el stop, mi pid es {}".format(os.getpid()))
        print("")
