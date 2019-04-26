import multiprocessing
import socket
import sys
import json
sys.path.append('../../')

from .parser import from_json_to_read_info, from_json_to_log, from_log_to_json
from .validator import is_log_valid
from common.worker_socket import WorkerSocket

POST_TYPE = "POS"
GET_TYPE = "GET"
DB_SERVER_READ_PORT = 6071
DB_SERVER_WRITE_PORT = 6061

''''''
class GetWorker(multiprocessing.Process):
    def __init__(self, queue, finished_queue):
        ''''''
        multiprocessing.Process.__init__(self)

        self.queue = queue
        self.finished_queue = finished_queue
        self.keep_running = True

    def run(self):
        '''Run function, it gets connected sockets from its queue and then
        writes the requested information'''
        print("----------------RUN GET worker-----------")
        while self.keep_running:
            id_skt, skt = self.queue.get()
            print("----------------Levanto un socket en GET-----------")
            if (not skt):
                self.keep_running = False
                continue

            log_request = skt.receive_request()
            print("----------------Recibo el request en GET-----------")
            if (not log_request.get_type() == GET_TYPE):
                return skt.send_response(404, "Error, invalid request")

            json_request_info = json.loads(log_request.get_args())
            read_info = from_json_to_read_info(json_request_info)

            db_skt = WorkerSocket()

            try:
                db_skt.connect("db-server", DB_SERVER_READ_PORT)
                print("--------------Me conecto a la db en GET-----------")
            except socket.error as serr:
                if serr.errno == errno.ECONNREFUSED:
                    return skt.send_response(503, "Error, our servers are full, try later")

            db_skt.send_read_info(read_info)
            print("----------------Envio la info a la db en GET-----------")
            logs_read = db_skt.receive_logs()
            print("--------------Recibo info de la db en GET-----------")
            pattern = json_request_info.get('pattern')

            json_logs_read = [from_log_to_json(log) for log in logs_read if (not pattern or pattern in log.get_msg())]

            db_skt.close()

            print("--------------Envio los logs {}-----------".format(json_logs_read))
            skt.send_response(200, json.dumps({"logs": json_logs_read}))
            print("----------------Envio response en GET-----------")

            skt.close()
            self.finished_queue.put(id_skt)

''''''
class PostWorker(multiprocessing.Process):
    def __init__(self, queue, finished_queue):
        ''''''
        multiprocessing.Process.__init__(self)

        self.queue = queue
        self.finished_queue = finished_queue
        self.keep_running = True

    def run(self):
        '''Run function, it gets connected sockets from its queue and then
        writes the requested information'''
        while self.keep_running:
            id_skt, skt = self.queue.get()

            if (not skt):
                self.keep_running = False
                continue

            log_request = skt.receive_request()

            if (not log_request.get_type() == POST_TYPE):
                return skt.send_response(404, "Error, invalid request")

            json_request_log = json.loads(log_request.get_args())
            log = from_json_to_log(json_request_log)

            if (not is_log_valid(log)):
                return skt.send_response(503, "Error, missing atributes")

            db_skt = WorkerSocket()

            try:
                db_skt.connect("db-server", DB_SERVER_WRITE_PORT)
            except socket.error as serr:
                if serr.errno == errno.ECONNREFUSED:
                    return skt.send_response(503, "Error, our servers are full, try later")

            db_skt.send_log(log)

            status = db_skt.receive_write_status()

            db_skt.close()

            skt.send_response(200, json.dumps({"msg": status}))

            skt.close()
            self.finished_queue.put(id_skt)
