__author__ = 'kaloyan'
from datetime import datetime, timedelta

class TimeConfiguration:
    ''' nastroiki na vremeto za saztezanie'''
    start_date = datetime(2015, 7, 7, 7)
    duration = timedelta(hours=1)
    expires = start_date + duration

# print(format(start_date, '%Y.%m.%d %H:%M:%S'))
# print(format(expires, '%Y.%m.%d %H:%M:%S'))
