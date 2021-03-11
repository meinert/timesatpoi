#!/usr/bin/env python

import numpy as np
import datetime

# Helper functions
def date_ymd_to_timestamp_ms(y,m,d):
    return datetime.datetime(y,m,d).timestamp()*1e3


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