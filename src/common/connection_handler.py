import multiprocessing
import signal

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

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def _spawn_worker(self, reading_requests):
        '''Returns a thread to use everytime a connections is accepted'''
        raise NotImplementedError("Abstract method!")

    def run(self):
        '''Run function, it accepts connections and spawns threads with
        that new connections'''
        print("-------------Empiezo el run-----------")
        requests = multiprocessing.Queue()

        self.skt.settimeout(1)

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
            #print("----------------Estoy por aceptar una conexion-----------")
            request_skt, addr = self.skt.accept()
            print("-------------Acepto una coneccion-----------")
            print("Mi keep_running es: {}".format(self.keep_running))
            if not request_skt:
                print("No tengo request skt!")
                continue

            requests.put(request_skt)

        print("")
        print("------------------I am hier!-------------------")

        self.skt.close()

        print("")
        print("-----------Cerre el socket-------------")

        while not requests.empty():
            requests.get().close()

        print("")
        print("-----------Limpio los requests------------")

        for worker in workers:
            requests.put(None)

        print("")
        print("-----------Pongo los None------------")

        for worker in workers:
            worker.join()

        print("")
        print("-----------Le doy join a los workers-------------")

        print("-----------Sali-------------")

        return

    def stop(self, signum, frame):
        '''Tells the DbHandler to stop its execution'''
        self.keep_running = False
        print("Recibi el stop")
        print("")
