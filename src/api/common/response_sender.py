import json

def send_response(app, status, status_msg):
    return app.response_class(
        response=json.dumps({"status": status_msg}),
        status=status,
        mimetype='application/json')
