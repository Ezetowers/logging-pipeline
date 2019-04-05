from flask import Flask, request

import json

app = Flask(__name__)

@app.route("/log/<appId>")
def getLog(appId):
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    tag = request.args.get('tag')
    pattern = request.args.get('pattern')

    return app.response_class(
        response=json.dumps({"from": date_from, "to": date_to, "tag": tag, "pattern": pattern}),
        status=200,
        mimetype='application/json')

if __name__ == "__main__":
    app.run()
