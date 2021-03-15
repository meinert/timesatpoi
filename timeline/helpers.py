#!/usr/bin/env python

import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Helper functions
def date_ymd_to_timestamp_ms(y,m,d):
    return datetime(y, m, d).timestamp()*1000


def deg2rad(a):
    return a*np.pi/180


def dist_btw_two_points(p1,p2):
    # p1 and p2 must be np.array([1,2])
    # Using https://en.wikipedia.org/wiki/Haversine_formula
    phi1 = deg2rad(p1[0])
    lba1 = deg2rad(p1[1])
    phi2 = deg2rad(p2[0])
    lba2 = deg2rad(p2[1])
    r = 6371*1e3    # Earth's radius: 6371kms in meters
    return 2*r*np.arcsin(np.sqrt(np.sin((phi2-phi1)/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin((lba2-lba1)/2)**2))

def ts2datetime(x):
    return datetime.fromtimestamp(int(x / 1000)).strftime('%Y-%m-%d %H:%M:%S')

def generate_time_at_poi(begin, end):
    # ts2datetime = lambda x: datetime.fromtimestamp(int(x / 1000)).strftime('%Y-%m-%d %H:%M:%S')

    dt_begin = datetime.strptime(ts2datetime(begin), '%Y-%m-%d %H:%M:%S')
    dt_end = datetime.strptime(ts2datetime(end), '%Y-%m-%d %H:%M:%S')

    dt_current = dt_begin

    times_at_poi = {}

    more = True

    while more:
        key = year_month_string(dt_current)
        times_at_poi[key] = 0

        dt_current = dt_current + relativedelta(months=1)

        if dt_current > dt_end:
            more = False

    return times_at_poi


def year_month_string(date: datetime):
    return str(date.year) + '-' + str(date.month)