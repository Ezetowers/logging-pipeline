# Entry point for the PUBLISH feature of the logging pipeline.

import sys

from flask import Flask, request

sys.path.append('../../')
from common.worker_socket import WorkerSocket

sys.path.append('../')
import common.parser as parser
import common.validator as validator
import common.response_sender as response_sender

DB_SERVER_WRITE_PORT = 6061

app = Flask(__name__)

@app.route("/log/<appId>", methods = ['POST'])
def postLog(appId):
    json_request_log = request.get_json()
    log = parser.from_json_to_log(appId, json_request_log)

    if (not validator.is_log_valid(log)):
        return response_sender.send_response(app, 503, "Error, missing atributes")

    skt = WorkerSocket()

    try:
        skt.connect("db-server", DB_SERVER_WRITE_PORT)
    except socket_error as serr:
        if serr.errno == errno.ECONNREFUSED:
            return response_sender.send_response(app, 503, "Error, our servers are full, try later")

    skt.send_log(log)

    status = skt.receive_write_status()

    skt.close()

    return response_sender.send_response(app, 200, status)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
