from datetime import datetime, timedelta
from constants import deviceType
import sys
import csv
import datetime
import os

main_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__))))
if deviceType == "windows":
    iHateWindows = "\logs\ "
    logPath = main_path + iHateWindows.strip()
else:
    logPath = main_path + "/logs/"

names = []
dates = []
name = ""
csv_Files = []
uniqueCoordinates = []
POI_locations = {}

def collect_data(name,roundVal):
    #Getting all of the CSV Files
    for path, subdirs, files in os.walk(logPath + name):
        for name in files:
            if ".csv" in name:
                csv_Files.append(str(os.path.join(path, name)))

            else:
                pass

    #Reading all of the CSV files and converting their data to a dictionary
    
    
    
    for user_File in csv_Files:
        with open(user_File, 'r') as csvfile:
            filename = str(user_File).split("/20")
            filename = "20" + filename[1]
            filename = filename.split("_")
            dateFromFilename = filename[0]
            # creating a csv reader object
            heading = next(csvfile)
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                #adding all the values to a dictionary
                latitude , longitude = row[1].split(sep=",")

                roundLat = round(float(latitude),roundVal)
                roundLong = round(float(longitude),roundVal)
                roundedCoordinatePair = roundLat,roundLong
    
                if roundedCoordinatePair not in uniqueCoordinates:
                    uniqueCoordinates.append(roundedCoordinatePair)
                    POI_locations.setdefault(roundedCoordinatePair,{"Name" : row[0], "Lattitude" : roundLat, "Longitude" : roundLong, "Time" : row[2], "Date" : dateFromFilename, "Battery" : row[3], "Visits" : 1})

                else:
                    POI_locations[roundedCoordinatePair]["Visits"] += 1

significant_Locations = []  
def sort_data(lowSignificance,highSignificance,roundVal):
    collect_data("",roundVal)
    coords = []
    for Coordinates in POI_locations:
        coords.append(Coordinates)

    for coord in coords:
        if int(POI_locations[coord]["Visits"]) >= lowSignificance and int(POI_locations[coord]["Visits"]) <= highSignificance:
            significant_Locations.append(POI_locations[coord])

    return significant_Locations

