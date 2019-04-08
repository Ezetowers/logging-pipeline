import sys

from flask import Flask, request
import json

sys.path.append('../../')
from common.worker_socket import WorkerSocket

sys.path.append('../')
import common.parser as parser

app = Flask(__name__)

@app.route("/log/<appId>")
def getLog(appId):
    print("---------------------------Estoy en el get-------------------------------", file=sys.stderr)

    json_request_info = request.args
    read_info = parser.from_json_to_read_info(json_request_info, appId)

    print("---------------------------Parsie-------------------------------", file=sys.stderr)

    skt = WorkerSocket()
    skt.connect("db-server", 6071)

    print("---------------------------Me conecte-------------------------------", file=sys.stderr)

    skt.send_read_info(read_info)
    print("----------------------------Envie la info------------------------------", file=sys.stderr)
    logs_read = skt.receive_logs()
    print("-------------------------------Recibi los logs---------------------------", file=sys.stderr)

    json_logs_read = [parser.from_log_to_json(log) for log in logs_read]

    print("-------------------------------Parsie los logs---------------------------", file=sys.stderr)
    return app.response_class(
        response=json.dumps({"logs": json_logs_read}),
        status=200,
        mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
