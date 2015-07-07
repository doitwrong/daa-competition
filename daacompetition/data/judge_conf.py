__author__ = 'kaloyan'
from datetime import datetime, timedelta

''' nastroiki na vremeto za saztezanie'''
start_date = datetime(2015, 7, 7, 9)
duration = timedelta(hours=300)
expires = start_date + duration

# print(format(start_date, '%Y.%m.%d %H:%M:%S'))
# print(format(expires, '%Y.%m.%d %H:%M:%S'))
