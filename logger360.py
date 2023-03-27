from life360 import life360
from datetime import datetime
from pytz import timezone
from constants import life360_username,life360_password,timeZone
tz = timezone(timeZone)
import csv
import os
from time import sleep



#logpath variable
mainpath = str(os.path.join(os.path.dirname(os.path.abspath(__file__)))) + "/"
logpath = mainpath + "logs/"


current_datetime = datetime.now(tz)
string = str(current_datetime)
dateAndTime = string.split()
date = dateAndTime[0]


if __name__ == "__main__":

    authorization_token = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="
    username = life360_username
    password = life360_password

    def collect_data(user):
        try:
            api = life360(authorization_token=authorization_token, username=username, password=password)
            if api.authenticate():

    
                circles =  api.get_circles()
                id = circles[0]['id']
                circle = api.get_circle(id)

        
                
                print("Circle name:", circle['name'])
                print("Members (" + circle['memberCount'] + "):")
                for m in circle['members']:

                    if (m['firstName'] != user):
                        pass
                    else:
                        print("Today's Date: " + str(dateAndTime[0] + "\n Current Time: " + str(dateAndTime[1])))
                        print("\tName:", m['firstName'],m['lastName'])
                        firstName = m['firstName']
                        lastName = m['lastName']
                        print("\tLocation:" , m['location']['shortAddress'], m['location']['address2'])
                        latitude = m['location']['latitude']
                        longitude = m['location']['longitude']
                        print("\tBattery level:" , m['location']['battery'] +"%")
                        batteryLevel = m['location']['battery']
                        drivingStatus = m['location']['isDriving']
                        print("\tCharging?", m['location']['charge'])
                        batteryCharging = m['location']['charge']
                        wifiStatus = m['location']['wifiState']
                        print("\t")
                        return(firstName,lastName,latitude,longitude,batteryLevel,batteryCharging,wifiStatus,drivingStatus)

            else:
                print("Error authenticating")

        except:
            return("Life-360_Error","","","","","","","")

def log_user_data(user):

    # get current date and time
    current_datetime = datetime.now(tz)
    string = str(current_datetime)
    dateAndTime = string.split()
    date = dateAndTime[0]

    # convert datetime obj to string

    isExist = os.path.exists(logpath + user + "/" + date + "_" + user + ".csv")

    if isExist == False:
        # create a file object along with extension
        filename = logpath + user + "/" + date + "_" + user + ".csv"
        file = open(filename, 'w')
        
        print("File created : ", str(filename))
        file.close()

        filename = logpath + user + "/" + date + "_" + user + ".csv"
        fields = ['Name', 'Coordinates', 'Time', 'Battery Level', "Currently Charging?", "WiFi Connection?", "Currently Driving?"]
        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(fields)

    else:
        print("file exists")
        pass

    data = collect_data(user)
    current_datetime = datetime.now(tz).strftime("%I:%M %p")

    if data[0] == "Life-360_Error":
        pass

    else:
        filename = logpath + user + "/" + date + "_" + user + ".csv"
        with open(filename, 'a') as file:
            writer = csv.writer(file)
            row = [data[0] + " " + data[1], data[2] + "," + data[3], current_datetime, data[4] + "%", data[5], data[6], data[7]]
            writer.writerow(row)
        sleep(10)
    

names = []
if __name__ == "__main__":
 
    authorization_token = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="
    

    username = life360_username
    password = life360_password

    api = life360(authorization_token=authorization_token, username=username, password=password)
    if api.authenticate():

        #Grab some circles returns json
        circles =  api.get_circles()
        
        #grab id
        id = circles[0]['id']

        #Let's get your circle!
        circle = api.get_circle(id)

        for userdata in circle['members']:
            name = str(userdata['firstName'])
            names.append(name)

while True:

    while True:

        for name in names:
            
            log_user_data(name)






