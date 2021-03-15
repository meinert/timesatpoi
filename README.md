# timesatpoi
Very simple python script that count the number of times you have been at a point and generates a list of when you have been at the point.

    NOTE: The implementation is very quick and dirty. Please submit a pull request with improvements 

    NOTE: Currently only support 2018, 2019, 2020 due to the quick and dirty implementation

Based on my python project template: https://github.com/meinert/pythonprojecttemplate

Clone the repository

Go to: https://takeout.google.com/settings/takeout

Download location history as JSON

Place the location history JSON file in the root of the repo (might be +1 GB)

Install all dependencies with pip install .

Edit the user paramters in runme.py

Run runme.py

It will take some time to load the locations file.

When done iformation regarding the number of times at the POI coordinates will be printed and a list of all the times you have been at the location grouped by the selected interval, e.g.

    Point 847406  --  Date: 2020-11-27 07:09:50  --  Distance to POI: 354m
        Group of 163 points
    Point 849530  --  Date: 2020-12-01 06:56:01  --  Distance to POI: 258m
        Group of 103 points
    Point 850730  --  Date: 2020-12-04 06:52:16  --  Distance to POI: 281m
        Group of 151 points
    Point 852256  --  Date: 2020-12-07 06:58:47  --  Distance to POI: 239m
        Group of 413 points
        
    Start: 2018-01-01 00:00:00.000000
    End: 2020-12-31 00:00:00.000000
    Number of visit during periode: {'2018': 123, '2019': 321, '2020': 111}

 


