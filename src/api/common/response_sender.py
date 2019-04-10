import json

def send_response(app, status, status_msg):
    '''Returns a response to an app with a given status and a message status'''
    return app.response_class(
        response=json.dumps({"status": status_msg}),
        status=status,
        mimetype='application/json')
