__author__ = 'kaloyan'


class DAAException(Exception):
    def __init__(self, msg):
        self.msg = msg


class SubmitTaskFailure(DAAException):
    def __init__(self, msg="problem pri izprashtane na reshenie"):
        DAAException.__init__(self, msg)


class TimeoutError(Exception):
    pass
