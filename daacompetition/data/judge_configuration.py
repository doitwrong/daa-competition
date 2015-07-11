__author__ = 'kaloyan'
from datetime import datetime, timedelta
import os


class TimeConfiguration:
    ''' nastroiki na vremeto za saztezanie
    '''
    def __init__(self):
        fn = os.path.join(os.path.dirname(__file__), 'configuration')

        lines = []
        with open(fn, 'r') as f:
            lines = f.readlines()
        d = {}
        for line in lines:
            (key, val) = line.split('|')
            d[key] = val

        self.start_date = datetime.strptime(d['start_date'].rstrip('\n'), '%b %d %Y %I:%M%p')
        self.duration = timedelta(hours=int(d['duration'].rstrip('\n')))
        self.expires = self.start_date + self.duration

