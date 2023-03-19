# Triangular-inator
Uses life360 API to access circle data, and store it away in daily .csv files for later viewing and data analysis.

### Credits to Harper Reed  (```https://github.com/pnbruckner/life360.git```) for creating the life360 client I used for this project.

## Setup

Make sure you make ammends to ```constants.py``` with your life360 username and password in order to effectively access the API. Also you need to create sub-folders within the logs folder, one for each member's ***first*** name in your group's circle.

> _For example_
```
   Triangular-inator/logs/Bob
   Triangular-inator/logs/Dylan
   Triangular-inator/logs/Pete
```
The ```life360.py``` file is the framework to actually connect to life-360. ***I did not make this.*** I made both ```logger360.py``` & ```visualizer.py```.

logger360 is intended to run headlessly on a computer with constant wifi access. It will continuously scrape life360's server for data on your circle, at which point it will log this data to a .csv file.

logger360 logs the following:

- lattitude
- longitude
- battery health
- name
- date
- current time

It was *supposed* to log driving and wifi-status as well, but it seems to be broken on either the ```life360.py```'s end or on life360's servers.

visualizer is for viewing any and all data that is collected in the csv files. just ensure it is in a directory that has a proper logs folder format (as mentioned above) as well as the csv files and it should run without a problem.

