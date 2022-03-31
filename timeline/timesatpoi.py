#!/usr/bin/env python

import numpy as np
import re
import locale
import timeline.helpers as helpers
from datetime import datetime, timedelta

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

class AtPOI():

    skiplines = 50000000;
    numberofpoints = 0;
    locations = []


    def __init__(self, locationhistory_file, begin_ts, end_ts, poi, radius_max=500, group_size=timedelta(weeks=0, days=1, hours=0, minutes=0, seconds=0, milliseconds=0), group_verbosity=1):
        self.locationhistory_file = locationhistory_file
        self.begin_ts = begin_ts
        self.end_ts = end_ts
        self.poi = poi
        self.radius_max = radius_max
        self.group_size = group_size
        self.group_verbosity = group_verbosity

    def load_file(self):
        # LOAD DATA
        # Read the file
        print("Loading '{}' ...".format(self.locationhistory_file))

        locations = []

        line_number = 0
        points = 0
        point_in_periode = 0

        timestamp_date = None
        timestamp_ms = None
        lat = None
        long = None
        accuracy = None

        with open(self.locationhistory_file) as infile:
            for line in infile:
                line_number = line_number + 1

                if line_number < self.skiplines:

                    if line_number % 1000000 == 0:
                        print(f'{line_number:n}')

                    continue

                line = line.split(":", maxsplit=1)

                if 'timestamp' in line[0]:
                    timestamt_str = line[1].replace('"', '')[1:20]
                    timestamp_date = datetime.strptime(timestamt_str, '%Y-%m-%dT%H:%M:%S')
                    timestamp_ms = helpers.datetime_to_timestamp_ms(timestamp_date)

                if 'latitudeE7' in line[0]:
                    lat = int(re.sub('[^0-9]', '', line[1]))

                if 'longitudeE7' in line[0]:
                    long = int(re.sub('[^0-9]', '', line[1]))

                if 'accuracy' in line[0]:
                    accuracy = (int(re.sub('[^0-9]', '', line[1])))

                if timestamp_ms is not None and lat is not None and long is not None and accuracy is not None:
                    points = points + 1

                    if points%10000 == 0:
                        print("Linenumber: {}   --   Points: {}    --     Points in periode: {}".format(f'{line_number:n}', f'{points:n}', str(point_in_periode)))

                    if timestamp_ms >= self.begin_ts and timestamp_ms <= self.end_ts:
                        point_in_periode = point_in_periode + 1

                        locations.append({
                            "timestampMs": timestamp_ms,
                            "latitudeE7": lat,
                            "longitudeE7": long,
                            "accuracy": accuracy
                        })

                    timestamp_ms = None
                    lat = None
                    long = None
                    accuracy = None

                        # if point_in_periode > 210:
                        #     break



                # if i > 100:
                #     break;

                # print(line)

        self.numberofpoints = len(locations)  # Number of timesteps
        self.locations = locations

        print("JSON file loaded")

    def preparedata(self):
        # Build arrays of basic data
        print("Extracting relevant data...")
        timestampMs = np.zeros(self.numberofpoints)   # in milliseconds
        positions = np.zeros([self.numberofpoints, 2])  # in degrees
        accuracy = np.zeros(self.numberofpoints)      # don't know the unit
        # activity = {}         # Don't store activity since we don't use it

        for i in range(self.numberofpoints):
            point = self.locations[i]
            if 'timestampMs' in point:
                timestampMs[i] = float(point['timestampMs'])
            if ('latitudeE7' in point) and ('longitudeE7' in point):
                positions[i] = np.array([float(point['latitudeE7']), float(point['longitudeE7'])])/1e7
            if 'accuracy' in point:
                accuracy[i] = point['accuracy']
            # if 'activity' in point:
            #     activity[i] = point['activity']

        # n_act = len(activity.keys())
        # print("Total number of points with activity: %d  (%0.1f%%)"%(n_act,int(n_act/n*100)))
        print("Total number of points: {}".format(self.numberofpoints))

        # Free some memory
        self.locations.clear()
        # main_dict.clear()

        return timestampMs, positions, accuracy

    def locationsatpoi(self, timestampMs, positions, accuracy):
        # Converter
        # ts2datetime = lambda x: datetime.utcfromtimestamp(int(x/1e3)).strftime('%Y-%m-%d %H:%M:%S')

        # Get time boundary index
        # np.searchsorted is a fast way to find the first element that is larger than the threshold. 1 is for True
        begin_index = np.searchsorted(timestampMs >= self.begin_ts, 1)
        end_index = np.searchsorted(timestampMs >= self.end_ts, 1)

        # Get group_size in milliseconds
        grpsMs = self.group_size.total_seconds()*1000

        # Get all points that are within radius_max of the poi
        close_points = []
        dist2poi = []
        # Check positions only after the specified date.
        for i in range(begin_index,end_index):
            # Compute distance to point of interest
            dist = helpers.dist_btw_two_points(self.poi, positions[i])
            if dist < self.radius_max:
                close_points.append(i)
                dist2poi.append(dist)

        close_points = np.array(close_points)
        print("Number of close points: %d\n"%close_points.size)


        prev = 0    # Keeps in memory the last timestamp displayed

        times_at_poi = helpers.generate_time_at_poi(self.begin_ts, self.end_ts)

        # times_at_poi = {'2018-01': 0,
        #                '2019': 0,
        #                '2020': 0}

        for i in range(close_points.size):
            # If the delta between timestamps is bigger than the group size, or if it's the beginning or the end.
            if timestampMs[close_points[i]]-timestampMs[close_points[prev]] > grpsMs or i == 0 or i == close_points.size-1:
                # If it's not the beginning and there are at least 2 points to make a group.
                if i>0 and i-prev > 2:
                    if i == close_points.size-1: i=i+1
                    if self.group_verbosity == 1:
                        print("\tGroup of %d points"%(i-prev-2))
                    if self.group_verbosity == 2:
                        print("\n\tGroup of %d points: %d -> %d"%(i-prev-2,close_points[prev+1],close_points[i-1]))
                        pt_date_im1 = helpers.ts2datetime(timestampMs[close_points[i-1]])
                        pt_date_prevp1 = helpers.ts2datetime(timestampMs[close_points[prev+1]])
                        print("\tFrom: %s"%pt_date_prevp1)
                        print("\tTo  : %s"%pt_date_im1)
                        print("\tMean dist to POI: %0.1fm\n"%np.mean(dist2poi[prev+1:i]))

                # if group_verbosity == 2: print()    # Add space between lines
                # Else, display the point, unless it's the end
                if i != close_points.size:
                    pt_date = helpers.ts2datetime(timestampMs[close_points[i]])
                    dt = datetime.strptime(pt_date, '%Y-%m-%d %H:%M:%S')
                    times_at_poi[helpers.year_month_string(dt)] = times_at_poi[helpers.year_month_string(dt)] + 1
                    print("Point %d  --  Date: %s  --  Distance to POI: %dm" % (close_points[i], pt_date, dist2poi[i]))
                    prev = i


        s = self.begin_ts / 1000.0
        begin = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')

        s = self.end_ts / 1000.0
        end = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')

        print("Start: {}".format(begin))
        print("End: {}".format(end))
        print("Number of visit during periode: {}".format(times_at_poi))
