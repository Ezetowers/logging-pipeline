import errno
import multiprocessing

from .worker_socket import WorkerSocket

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
        self.keep_running = True
        self.number_of_workers = number_of_workers
        self.number_of_queued_connections = number_of_queued_connections

    def _spawn_worker(self, reading_requests):
        '''Returns a thread to use everytime a connections is accepted'''
        raise NotImplementedError("Abstract method!")

    def run(self):
        '''Run function, it accepts connections and spawns threads with
        that new connections'''
        requests = multiprocessing.Queue()

        self.skt.bind(self.host, self.port)
        print("----------------Me conecto a {}:{}-----------".format(self.host, self.port))
        self.skt.listen(self.number_of_queued_connections)
        print("----------------Escucho-----------")

        workers = []

        for i in range(self.number_of_workers):
            worker = self._spawn_worker(requests)
            #worker.daemon = True
            worker.start()
            workers.append(worker)

        while self.keep_running:
            try:
                print("----------------Estoy por aceptar una conexion-----------")
                request_skt, addr = self.skt.accept()
                print("-------------Acepto una coneccion-----------")
                requests.put(request_skt)
            except IOError as serr:
                if serr.errno != errno.EINVAL:
                    raise serr

        while not requests.empty():
            requests.get().close()

        for worker in workers:
            requests.put(None)

        for worker in workers:
            worker.join()

    def stop(self):
        '''Tells the DbHandler to stop its execution'''
        self.keep_running = False
        self.skt.close()
