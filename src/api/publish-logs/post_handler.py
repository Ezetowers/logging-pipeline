import sys

from flask import Flask, request
import json

sys.path.append('../../')
from common.worker_socket import WorkerSocket

sys.path.append('../')
import common.parser as parser

app = Flask(__name__)

@app.route("/log/<appId>", methods = ['POST'])
def postLog(appId):
    json_request_log = request.args
    log = parser.from_json_to_log(json_request_log)

    skt = WorkerSocket()
    skt.connect("db-server", 6061)

    skt.send_log_info(log)

    status = skt.receive_write_status()

    return app.response_class(
        response=status,
        status=200,
        mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
