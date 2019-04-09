import sys

from flask import Flask, request
import json

sys.path.append('../../')
from common.worker_socket import WorkerSocket

sys.path.append('../')
import common.parser as parser

DB_SERVER_WRITE_PORT = 6061

app = Flask(__name__)

@app.route("/log/<appId>", methods = ['POST'])
def postLog(appId):
    json_request_log = request.get_json()
    log = parser.from_json_to_log(json_request_log)

    skt = WorkerSocket()
    skt.connect("db-server", DB_SERVER_WRITE_PORT)

    skt.send_log(log)

    status = skt.receive_write_status()

    skt.close()

    return app.response_class(
        response=json.dumps({"status": status}),
        status=200,
        mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
