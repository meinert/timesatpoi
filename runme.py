import locale
from timeline import timesatpoi
import numpy as np
import datetime
# import re
# import locale
import timeline.helpers as helpers
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'




#############
# USER INPUT
#############

json_file = "Records2024.json"

# Get first and last timestamps of interest
begin_ts = helpers.date_ymd_to_timestamp_ms(2022, 1, 1)
end_ts = helpers.date_ymd_to_timestamp_ms(2022, 12, 31)

begin_date = datetime.date(year=2023, month=1, day=1)
end_date = datetime.date(year=2023, month=12, day=31)

# Point of interest
    poi = np.array([56.71370324568134, 10.113683819381745])    # in degrees Hadsund
# poi = np.array([57.01252757476267, 9.987804015778735])    # in degrees Aalborg


radius_max = 1000                         # in meters

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

# test = helpers.generate_time_at_poi(begin_ts, end_ts)

timesatwork = timesatpoi.AtPOI(json_file, begin_ts, end_ts, poi, radius_max, group_size, group_verbosity)
# timesatwork = timesatpoi.AtPOI(json_file, begin_date, end_date, poi, radius_max, group_size, group_verbosity)

timesatwork.load_file()

timestampMs, positions, accuracy = timesatwork.preparedata()

timesatwork.locationsatpoi(timestampMs, positions, accuracy)

