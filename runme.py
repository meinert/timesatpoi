from timeline import timesatpoi
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

timesatwork = timesatpoi.AtPOI(json_file, begin_ts, end_ts, poi, radius_max, group_size, group_verbosity)

timesatwork.load_file()

timestampMs, positions, accuracy = timesatwork.preparedata()

timesatwork.locationsatpoi(timestampMs, positions, accuracy)

