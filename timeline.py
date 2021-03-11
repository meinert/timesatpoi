#!/usr/bin/env python

import numpy as np
import datetime
import re
import locale
import timeline.helpers as helpers
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'


#############
# USER INPUT
#############

json_file = "Placeringshistorik.json"

# Get first and last timestamps of interest
begin_ts = helpers.date_ymd_to_timestamp_ms(2018, 1, 1)
end_ts = helpers.date_ymd_to_timestamp_ms(2020, 12, 31)
# end_ts = timestampMs[-1]    # Last one

# Point of interest
poi = np.array([56.71370324568134,10.113683819381745])    # in degrees
radius_max = 500                         # in meters

# Define the interval of time below which timestamps should be grouped together
group_size = datetime.timedelta(weeks=0, days=1, hours=0, minutes=0, seconds=0, milliseconds=0)
# Amount of info to show about each group:
# 0: None
# 1: Number of points in group
# 2: Add point IDs, first/last datetime in group, avg dist to POI
group_verbosity = 1

####################
# END OF USER INPUT
####################

# LOAD DATA
# Read the file
print("Loading '%s' ..."%json_file)

locations = []

line_number = 0
points = 0
point_in_periode = 0

with open(json_file) as infile:
    for line in infile:
        line_number = line_number + 1

        if line_number < 24000000:

            if line_number % 1000000 == 0:
                print(f'{line_number:n}')

            continue

        line = line.split(":")

        if 'timestamp' in line[0]:
            timestampMs = (float(re.sub('[^0-9]', '', line[1])))

        if 'latitudeE7' in line[0]:
            lat = int(re.sub('[^0-9]', '', line[1]))

        if 'longitudeE7' in line[0]:
            long = int(re.sub('[^0-9]', '', line[1]))

        if 'accuracy' in line[0]:
            accuracy = (int(re.sub('[^0-9]', '', line[1])))

            points = points + 1

            if points%10000 == 0:
                print("Linenumber: {}   --   Points: {}    --     Points in periode: {}".format(f'{line_number:n}', f'{points:n}', str(point_in_periode)))

            if timestampMs >= begin_ts and timestampMs <= end_ts:
                point_in_periode = point_in_periode + 1

                locations.append({
                    "timestampMs": timestampMs,
                    "latitudeE7": lat,
                    "longitudeE7": long,
                    "accuracy": accuracy
                })

                # if point_in_periode > 210:
                #     break



        # if i > 100:
        #     break;

        # print(line)

data = locations

# file = open(json_file)
# Lines = file.readlines()
# main_dict = ijson.parse(file)

# for post in main_dict:
#     print(post)


# main_dict = json.load(open(json_file))   # This can take a bit of time
print("JSON file loaded")
# data is a big list of dicts.
# data = main_dict['timelineObjects']
n = len(data)   # Number of timesteps

# Discovery of the dataset
# # Some dicts only contain basic info : timestamp, latitude, longitude and accuracy
# print(data[0])
# # Others also have an activity :
# print(data[300])
#
# # It seems that the list is ordered by timestamp.
#
# # More recent points have more info :
# print(data[-1])

# Build arrays of basic data
print("Extracting relevant data...")
timestampMs = np.zeros(n)   # in milliseconds
positions = np.zeros([n, 2])  # in degrees
accuracy = np.zeros(n)      # don't know the unit
# activity = {}         # Don't store activity since we don't use it

for i in range(n):
    point = data[i]
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
print("Total number of points: %d"%n)

# Free some memory
data.clear()
# main_dict.clear()

# Converter
ts2datetime = lambda x: datetime.datetime.utcfromtimestamp(int(x/1e3)).strftime('%Y-%m-%d %H:%M:%S')

# Get time boundary index
# np.searchsorted is a fast way to find the first element that is larger than the threshold. 1 is for True
begin_index = np.searchsorted(timestampMs >= begin_ts, 1)
end_index = np.searchsorted(timestampMs >= end_ts, 1)

# Get group_size in milliseconds
grpsMs =  group_size.total_seconds()*1000

# Get all points that are within radius_max of the poi
close_points = []
dist2poi = []
# Check positions only after the specified date.
for i in range(begin_index,end_index):
    # Compute distance to point of interest
    dist = dist_btw_two_points(poi, positions[i])
    if dist < radius_max:
        close_points.append(i)
        dist2poi.append(dist)

close_points = np.array(close_points)
print("Number of close points: %d\n"%close_points.size)


prev = 0    # Keeps in memory the last timestamp displayed
times_at_poi = { '2018': 0,
                 '2019': 0,
                 '2020': 0}

for i in range(close_points.size):
    # If the delta between timestamps is bigger than the group size, or if it's the beginning or the end.
    if timestampMs[close_points[i]]-timestampMs[close_points[prev]] > grpsMs or i == 0 or i == close_points.size-1:
        # If it's not the beginning and there are at least 2 points to make a group.
        if i>0 and i-prev > 2:
            if i == close_points.size-1: i=i+1
            if group_verbosity == 1:
                print("\tGroup of %d points"%(i-prev-2))
            if group_verbosity == 2:
                print("\n\tGroup of %d points: %d -> %d"%(i-prev-2,close_points[prev+1],close_points[i-1]))
                pt_date_im1 = ts2datetime(timestampMs[close_points[i-1]])
                pt_date_prevp1 = ts2datetime(timestampMs[close_points[prev+1]])
                print("\tFrom: %s"%pt_date_prevp1)
                print("\tTo  : %s"%pt_date_im1)
                print("\tMean dist to POI: %0.1fm\n"%np.mean(dist2poi[prev+1:i]))

        # if group_verbosity == 2: print()    # Add space between lines
        # Else, display the point, unless it's the end
        if i != close_points.size:
            pt_date = ts2datetime(timestampMs[close_points[i]])
            dt = datetime.datetime.strptime(pt_date, '%Y-%m-%d %H:%M:%S')
            times_at_poi[str(dt.year)] = times_at_poi[str(dt.year)] + 1
            print("Point %d  --  Date: %s  --  Distance to POI: %dm" % (close_points[i], pt_date, dist2poi[i]))
            prev = i


s = begin_ts / 1000.0
begin = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')

s = end_ts / 1000.0
end = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')

print("Start: {}".format(begin))
print("End: {}".format(end))
print("Number of visit during periode: {}".format(times_at_poi))