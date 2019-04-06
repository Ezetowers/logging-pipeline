from flask import Flask, request

import json

app = Flask(__name__)

@app.route("/log/<appId>", methods = ['POST'])
def postLog(appId):
    return app.response_class(
        response=json.dumps(request.get_json()),
        status=200,
        mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
