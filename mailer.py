from constants import deviceType,timeZone,debugMode,yourGmail,gmail_SENDING_appPass
from logger360 import collect_data
from datetime import datetime,timedelta
import os
from pytz import timezone
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
import geopy.distance
from random import randint
from time import sleep

geolocator = Nominatim(user_agent="Triangular-inator")


tz = timezone(timeZone)

now = datetime.now(tz)

month = now.month
day = now.day
year = now.year

timeNow = datetime.now(tz)
timStirng = str(timeNow.strftime("%m-%d-%Y %I:%M:%S%p"))
dateTimestring = timStirng.split()
datetring = dateTimestring[0]
timetring = dateTimestring[1]


print(" ~ Program Executed ~ \n| Name: mailer.py \n| Time: " + timetring + "\n| Date: " + datetring)


main_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__))))
if deviceType == "windows":
    iHateWindows = "\logs\ "
    logPath = main_path + iHateWindows.strip()
else:
    logPath = main_path + "/logs/"


def minutes_to_hours(minutes : int):
    time = '{}:{}'.format(minutes//60,minutes%60)
    return time 

def hours_to_days(hours : int):
    time = '{}:{}'.format(hours//24,hours%24)
    return time 

Dict = {}
names = []
dates = []
name = ""
csv_Files = []
def collect_csv_through_dates(name,pastTimeDelta,date):
    week_ago = date - timedelta(days=pastTimeDelta)
    #Getting all of the CSV Files
    if debugMode == True: print("Processing the following files:\n")
    for path, subdirs, files in os.walk(logPath + name):
        for name in files:
            if ".csv" in name:
                nameDateTime = datetime.strptime(name[:10],'%Y-%m-%d').date()
                if nameDateTime >= week_ago:
                    csv_Files.append(str(os.path.join(path, name)))
                    
                    if debugMode == True: print("| " + name + " |")
                    

            else:
                pass

    if debugMode == True: print("Done.\n")
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
                name = row[0]
                time = row[2]
                battery = row[3]
                batteryCharging = row[4]
                inTransit = row[5]
                speed = row[6]
                timeArrivedAtLocation = row[7]
                timeSinceArrivingAtLocation = row[8]
                if name in names:
                    pass
                else:
                    names.append(name)
                Dict.setdefault(name, []).append([name, latitude, longitude, time, dateFromFilename, battery,batteryCharging,inTransit,speed,timeArrivedAtLocation,timeSinceArrivingAtLocation])



avatarList, emailList = collect_data(False)
temp = []
for avatar in avatarList:
    if avatar not in temp:
        temp.append(avatar)
avatarList = temp
temp = []
for email in emailList:
    if email not in temp:
        temp.append(email)
emailList = temp
temp = []


#Collecting all of the users from the database

winnerName = "Tomato"
winnerSpeed = float(9207.23)

def  count_low_battery_instances(data):
    from collections import defaultdict
    low_battery_count = defaultdict(int)
    tethered_count = defaultdict(int)
    print(names)
    for name in names:

        for entry in Dict[name]:
            name, latitude, longitude, time, date, battery, battery_charging, in_transit, speed, start_timestamp, duration = entry

            # Assuming 'battery' is the index for battery level in your data
            battery = round(float(str(battery).split("%")[0]),2)
            if battery < 10:
                low_battery_count[name] += 1
            if int(battery_charging) == 1:
                tethered_count[name] += 1

    result_list = [[name, low_battery_count[name], tethered_count[name]] for name in names]

    return result_list


speedRunnerUps = []

def getSpeedWinners():
    topSpeed = float(0)
    winner = "Tomatohead"
    tmpNames = []
    winners=[]
    collect_csv_through_dates("",7,datetime.now(tz).date())
    for name in names:
        for value in Dict[name]:
            if float(value[8]) >= 10:
                speed = float(value[8])
                
                if float(speed) > topSpeed:
                    winner = name
                    topSpeed = float(speed)
                    strSpeed = str(round(float(topSpeed * 2.237),2)) 
                    if debugMode == True: print("new top speed is: " + str(strSpeed) + " by " + name)

    
    highest_speeds = {}

    for name in names:
        # Initialize variables for the current person
        current_speed = float(0)
        current_winner = ""
        if name != winner:
            # Iterate through the values for the current person
            for value in Dict[name]:
                if float(value[8]) >= 10:
                    speed = float(value[8])
                    if speed > current_speed:
                        current_winner = name
                        current_speed = speed

            # Update the highest_speeds dictionary with the highest speed for the current person
            if current_winner not in highest_speeds or current_speed > highest_speeds[current_winner]:
                highest_speeds[current_winner] = current_speed

    # Convert the dictionary to a list of pairs
    winners = [[name, str(round(float(speed * 2.237),2))] for name, speed in highest_speeds.items()]
    # Filter out unneccesary ['', 0.0] data point.
    winners = [entry for entry in winners if entry[0] != '' and entry[1] != 0.0]


         
    return winner,winners,topSpeed

winnerName,runnerUpList, winnerSpeed = getSpeedWinners()

if debugMode == True: 
    for name,speed in runnerUpList:
        print(name + " " + speed + " mph")

text = winnerName + " won this weeks speed record with a speed of " + str(winnerSpeed)


def getDistance(person):
    lat2 = ""
    long2 = ""
    firstIteration = True
    distance = 0
    for name in names:
        if name == person:
            for value in Dict[name]:
                if value[7] != -1:
                    lat = value[1]
                    long = value[2]
                    if firstIteration == True:
                        lat2 = lat
                        long2 = long
                        firstIteration = False
                    else:
                        meters = geopy.distance.geodesic((float(lat),float(long)), (float(lat2),float(long2))).miles
                        firstIteration = True
                        distance += meters

            return distance


html = """<p style="text-align:center">"""

for avatar in avatarList:
    html += f'<img alt="" src="{avatar}" style="height:43px; width:40px" />'

headers = ["Your Riveting Week: Spoiler Alert - You Moved. Again. 🙄🌎","Breaking News: Your Weekly Speed Update. Because Life's a Race, Right? 🏁😒","Master of Geography: Your Weekly Location Report. Try to Keep Up. 🤨🗺️","Rapid Reality Check: Your Weekly Journey Recap. Bet You Forgot Already. 🚀😏","Epic Travels Unleashed: Your Weekly Pathetic Attempt at Speed. 😂🌐","Lap of... Whatever: Your Weekly 'Fast' Facts. Buckle Up for Mediocrity! 🤷‍♂️🚗"]
ourHeader = headers[randint(0,5)]

html += f'<p style="text-align:center"><strong><span style="font-size:14px"><span style="font-family:Courier New,Courier,monospace">{month} / {day} / {year}</span></span></strong></p> <h1 style="text-align:center">{ourHeader}</h1> <hr /> <p style="text-align:center">Our top speed winner this week was:&nbsp;</p> <p style="text-align:center"><span style="font-size:18px">{winnerName}!</span></p> <p style="text-align:center">With a speed of:&nbsp;</p> <p style="text-align:center"><em><span style="font-size:24px"><span style="color:#e74c3c"><strong>🔥 {str(round(winnerSpeed * 2.237,2))} MPH! 🔥</strong></span></span></em></p> <p>&nbsp;</p>'


html += f'<h2 style="text-align:center">Speed Runner-Ups:</h2>'

  
for name,speed in runnerUpList:
    html += f'<p style="text-align:center">{name}&nbsp; -&nbsp; {speed} mph</p>'


peopleTravels = []
for name in names:
        peopleTravels.append((name,str(round(getDistance(name),2))))
        print(name,str(round(getDistance(name),2)) + " miles")

def putDistanceInEmail():
    global html
    html += f'<p style="text-align:center"><span style="font-size:22px"><u>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</u></span></p>'
    html += f'<h2 style="text-align:center">Now for how far everyone went!&nbsp; 🚗💨 🏃</h2>'
    highest_distance = 0
    winner = "Kitbash"
    for name,distance in peopleTravels:
        if float(distance) > highest_distance:
            highest_distance = float(distance)
            winner = name
    html += f'<p style="text-align:center">{winner}, takes the cake with {highest_distance} miles!</p>'
    html += f'<h2 style="text-align:center">Everyone else:</h2>'

  
    for name,distance in peopleTravels:
        print(winner)
        if name != winner:
            html += f'<p style="text-align:center">{name}&nbsp; -&nbsp; {distance} miles</p>'

putDistanceInEmail()

def emailBatteryFormat():
    global html
    html += '<p>&nbsp;</p> <p>&nbsp;</p> <hr /> <h2 style="text-align:center"><strong>⚡️ BATTERY STATS 🔋</strong></h2> <p>&nbsp;</p> <table align="center" border="1" cellpadding="1" cellspacing="1" style="width:500px"> <thead> <tr> <th style="background-color:#cccccc; border-color:#ff0000; height:50px; text-align:center; vertical-align:middle; width:33%">Name</th> <th style="background-color:#cccccc; border-color:#ff0000; height:50px; text-align:center; vertical-align:middle; width:33%">Time spent below 10%</th> <th style="background-color:#cccccc; border-color:#ff0000; height:50px; text-align:center; vertical-align:middle; width:33%">Time spent charging</th> </tr> '
    battery_instances = count_low_battery_instances(collect_csv_through_dates("",7,datetime.now(tz).date()))
    for pair in battery_instances:
        print(pair)
        battName = pair[0]


        if int(pair[1]) == 0:
            timeSpentBelow10 = "None!"
        else:
            timeSpentBelow10 = minutes_to_hours(int(pair[1])//3)

            if int(timeSpentBelow10.split(":")[0]) >= 24:
                timeSpentBelow10 = hours_to_days(int(timeSpentBelow10.split(":")[0]))
                timeSpentBelow10 = str(timeSpentBelow10).split(":")[0] + " Days & " + str(timeSpentBelow10).split(":")[1] + " Hrs"
            else:
                timeSpentBelow10 = str(timeSpentBelow10).split(":")[0] + " Hrs & " + str(timeSpentBelow10).split(":")[1] + " min"
                


        if int(pair[2]) == 0:
            timeSpentCharging = "How..?"
        else:
            timeSpentCharging = minutes_to_hours(int(pair[2])//3)

            if int(timeSpentCharging.split(":")[0]) >= 24:
                timeSpentCharging = hours_to_days(int(timeSpentCharging.split(":")[0]))
                timeSpentCharging = str(timeSpentCharging).split(":")[0] + " Days & " + str(timeSpentCharging).split(":")[1] + " Hrs"

            else:
                timeSpentCharging = str(timeSpentCharging).split(":")[0] + " Hrs & " + str(timeSpentCharging).split(":")[1] + " min"


        
        html += f'<tr> <th style="background-color:#cccccc; border-color:#000000; height:25px; text-align:center; vertical-align:middle; width:33%"><span style="font-size:10px">{battName}</span></th> <th style="background-color:#cccccc; border-color:#000000; height:25px; text-align:center; vertical-align:middle; width:33%"><span style="font-size:10px">{timeSpentBelow10}</span></th> <th style="background-color:#cccccc; border-color:#000000; height:25px; text-align:center; vertical-align:middle; width:33%"><span style="font-size:10px">{timeSpentCharging}</span></th> </tr>'


    html += '</thead> <tbody> </tbody> </table> '

emailBatteryFormat()



def POI_gen():
    global html
    Adresses = []
    peoplePlaces = []
    from significantLocations import sort_data
    special_places = sort_data(40,300,4)
    print("Loading...")
    for place in special_places:
        owner = place['Name']
        lat = place['Lattitude']
        long = place['Longitude']
        location = geolocator.reverse("{}, {}".format(lat,long))
        if location.address not in Adresses:
            Adresses.append(location.address)
            peoplePlaces.append((owner,location.address))
    print("\nDone!")


    placeTitle = 1
    tempOwner = ""
    for owner,place in peoplePlaces:
        print(owner,tempOwner,place,placeTitle)
        if tempOwner == owner:
            placeTitle = 0
        if placeTitle == 1:
            html += """<p>{} had the following points of interest:</p>""".format(owner)
            html += """<ul>"""
            html += """<li>{}</li>""".format(place)
            html += """</ul>"""
            placeTitle = 0
        else:
            html += """<ul>"""
            html += """<li>{}</li>""".format(place)
            html += """</ul>"""
            placeTitle = 0

        tempOwner = owner
        placeTitle = 1
	


def send_email_out(recipient):
    global html
    
    if debugMode == True: print(html)
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    html += '<p>'
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(yourGmail, gmail_SENDING_appPass)
    mail.sendmail(yourGmail, recipient, msg.as_string())
    mail.quit()

def groupEmail():
    global msg
    #for email in emailList:
    if 1==1:
        email = "carterbeaudoin@gmail.com"
        print("Sending email to " + email)
        msg = MIMEMultipart('alternative')
        subjects = ["Moved. Again. Seriously?","Speed: Barely Noticed.","Location Recap: Whatever.","Fast? Doubtful Week.",
                    "Epic Slowpoke Journey.","Zoom Level: Yawn.","Travel Who Cares?","Speed: Snail Status.",
                    "Location, Lost Again.","Week: Zero Excitement.","Journey: Mildly Interesting.","Speedy Snooze Fest."]
        ourSubject = subjects[randint(0,11)]
        msg['Subject'] = ourSubject
        msg['From'] = yourGmail
        msg['To'] = email
        send_email_out(email)
        print("Sent! Waiting a sec to send next email!\n")
        sleep(1)

sundayFlag = False

def prepareEmail():
    global sundayFlag
    time = datetime.now(tz).hour
    now = datetime.now(tz)
    weekday = datetime.weekday(now) 
    if weekday == 6:
        if sundayFlag != True:
            if time >= 15:
                sundayFlag = True
                print("Sending the emails out!\n")
                groupEmail()

    else:
        sundayFlag = False

while True:
    try:
        #prepareEmail()
        groupEmail()
        sleep(500)
    except Exception as e:
        print(e)
        exit()