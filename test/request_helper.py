import json
import sys
sys.path.append('../src')

from common.worker_socket import WorkerSocket

def post_log(log_body):
    skt = WorkerSocket()
    skt.connect('0.0.0.0', 6060)
    skt.send_request('POS', json.dumps(log_body))
    status, response = skt.receive_response()
    skt.close()

    print("Mi status es {} y mi response {}".format(status, response))
    return status, json.loads(response)

def get_logs(read_info):
    skt = WorkerSocket()
    skt.connect('0.0.0.0', 6070)
    skt.send_request('GET', json.dumps(read_info))
    status, response = skt.receive_response()
    skt.close()

    print("Mi status es {} y mi response {}".format(status, response))
    return status, json.loads(response)
