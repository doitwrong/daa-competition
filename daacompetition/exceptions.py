__author__ = 'kaloyan'

class SubmitTaskFailure(Exception):
    def __init__(self, msg):
        self.msg = msg
