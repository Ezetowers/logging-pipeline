class LogRequest(object):
    """docstring for ."""
    def __init__(self, type, args):
        self.type = type
        self.args = args

    def get_type(self):
        return self.type

    def get_args(self):
        return self.args
