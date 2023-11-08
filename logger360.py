from life360 import life360
from constants import life360_password,life360_username,debugMode,timeZone
from time import sleep
from datetime import datetime
import os
from pytz import timezone, all_timezones_set
import csv

if timeZone == "":
    print('all the supported timezones set:', all_timezones_set, '\n')
else:
    tz = timezone(timeZone)

mainpath = str(os.path.join(os.path.dirname(os.path.abspath(__file__)))) + "/"
if debugMode == True: print("Mainpath: " + mainpath + "\n")
logpath = mainpath + "logs/"
if debugMode == True: print("Logpath: " + logpath + "\n")


username = life360_username
password = life360_password
# basic authorization hash (base64 if you want to decode it and see the sekrets)
# this is a googleable or sniffable value. i imagine life360 changes this sometimes. 
authorization_token = "Y2F0aGFwYWNyQVBoZUtVc3RlOGV2ZXZldnVjSGFmZVRydVl1ZnJhYzpkOEM5ZVlVdkE2dUZ1YnJ1SmVnZXRyZVZ1dFJlQ1JVWQ=="

#instantiate the API
api = life360(authorization_token=authorization_token, username=username, password=password)

#Authenticate! 
names = []

class Person:
    def __init__(self,firstName,lastName,latitude,longitude,batteryLevel,batteryCharging,inTransit,speed,startTimestamp,since):
        self.firstName = firstName
        self.lastName = lastName
        self.latitude = latitude
        self.longitude = longitude
        self.batteryLevel = batteryLevel
        self.batteryCharging = batteryCharging
        self.inTransit = inTransit
        self.speed = speed
        self.startTimestamp = startTimestamp
        self.since = since
    
    def saveMyFile(self):
        if debugMode == True: print("Func- log_user_data(" + self.firstName + ")" + "\n")

        # get current date and time
        current_datetime = datetime.now(tz)
        string = str(current_datetime)
        dateAndTime = string.split()
        date = dateAndTime[0]

        # convert datetime obj to string

        isExist = os.path.exists(logpath + self.firstName + "/" + date + "_" + self.firstName + ".csv")

        if debugMode == True: print(logpath + self.firstName + "/" + date + "_" + self.firstName + ".csv" + "\n")
        if debugMode == True: print(str(isExist) + "\n")

        if isExist == False:
            # create a file object along with extension
            filename = logpath + self.firstName + "/" + date + "_" + self.firstName + ".csv"
            file = open(filename, 'w')
            
            print("File created : ", str(filename))
            file.close()

            filename = logpath + self.firstName + "/" + date + "_" + self.firstName + ".csv"
            fields = ['Name', 'Coordinates', 'Time', 'Battery Level', "Currently Charging?", "In Transit?", "Current Speed", "Start Timestamp", "End Timestamp"]
            with open(filename, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the fields
                csvwriter.writerow(fields)

        else:
            print("file exists")
            pass
        
        data = [self.firstName,self.lastName,self.latitude,self.longitude,self.batteryLevel,self.batteryCharging,self.inTransit,self.speed,self.startTimestamp,self.since]
        

        current_datetime = datetime.now(tz).strftime("%I:%M %p")

        if data[0] == "Life-360_Error":
            if debugMode == True: print("Life-360 Couldn't Authenticate" + "\n")
            pass

        else:
            filename = logpath + self.firstName + "/" + date + "_" + self.firstName + ".csv"
            with open(filename, 'a') as file:
                writer = csv.writer(file)
                row = [data[0] + " " + data[1], data[2] + "," + data[3], current_datetime, data[4] + "%", data[5], data[6], data[7],data[8],data[9]]
                if debugMode == True: print("Writing row: " + str(row) + "\n")
                writer.writerow(row)

def format_date( d):
    diff = datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day'
    elif diff.days > 1:
        return '{} days'.format(diff.days)
    elif s <= 1:
        return 'Active'
    elif s < 60:
        return '{} seconds'.format(s)
    elif s < 120:
        return '1 minute'
    elif s < 3600:
        return '{} minutes'.format(s/60)
    elif s < 7200:
        return '1 hour'
    else:
        return '{} hours'.format(s/3600)



def collect_data():
    personData = Person("Tomato","Head","Tomato","Town","3 mini sheilds","100 sheild","dropping in tilted","battlebus speed","Storm","Closing")
    if api.authenticate():
        #Grab some circles returns json
        circles =  api.get_circles()
        #grab id
        id = circles[0]['id']
        #Let's get your circle!
        circle = api.get_circle(id)
        print(circle)
        for m in circle['members']:
            print("\tName:", m['firstName'],m['lastName'])
            personData.firstName = m['firstName']
            personData.lastName = m['lastName']
            avatar = m['avatar']
            email = m['loginEmail']
            phone = m['loginPhone']
            print("\tLocation:" , m['location']['shortAddress'], m['location']['address2'])
            personData.startTimestamp = datetime.fromtimestamp(int(m['location']['startTimestamp']))
            personData.since = format_date(datetime.fromtimestamp(int(m['location']['since']))) # YOU NEED TO USE strftime('%Y-%m-%d %H:%M:%S') TO USE THESE DATETIME OBJECTs!!!!

            personData.latitude = m['location']['latitude']
            personData.longitude = m['location']['longitude']
            personData.inTransit = m['location']['inTransit']
            personData.speed = m['location']['speed']
            print("\tBattery level:" , m['location']['battery'] +"%")
            personData.batteryLevel = m['location']['battery']
            print("\tCharging?", m['location']['charge'])
            personData.batteryCharging = m['location']['charge']
            print("\t")

            personData.saveMyFile()
            
            
if __name__ == "__main__":
    while True:
        try:
            collect_data()
            sleep(55)

        except KeyboardInterrupt:
            if debugMode == True: print("Exiting..." + "\n")
            exit()
