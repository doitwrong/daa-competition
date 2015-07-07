__author__ = 'kaloyan'

class ValidationFailure(Exception):
    def __init__(self, msg):
        self.msg = msg
