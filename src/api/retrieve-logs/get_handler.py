import sys

from flask import Flask, request
import json

sys.path.append('../../')
from common.worker_socket import WorkerSocket

sys.path.append('../')
import common.parser as parser
import common.response_sender as response_sender

DB_SERVER_READ_PORT = 6071

app = Flask(__name__)

@app.route("/log/<appId>")
def getLog(appId):
    json_request_info = request.args
    read_info = parser.from_json_to_read_info(json_request_info, appId)

    print("---------------------------Recibo el get----------------------------------")

    skt = WorkerSocket()
    try:
        skt.connect("db-server", DB_SERVER_READ_PORT)
    except socket_error as serr:
        if serr.errno == errno.ECONNREFUSED:
            return response_sender.send_response(app, 503, "Error, our servers are full, try later")
    print("---------------------------Me conecto----------------------------------")

    skt.send_read_info(read_info)
    print("---------------------------Envio la info de lectura----------------------------------")
    logs_read = skt.receive_logs()
    print("---------------------------Recibo los logs leidos----------------------------------")

    json_logs_read = [parser.from_log_to_json(log) for log in logs_read]
    print("---------------------------Parseo los logs----------------------------------")
    skt.close()
    return app.response_class(
        response=json.dumps({"logs": json_logs_read}),
        status=200,
        mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
