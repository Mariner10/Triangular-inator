from constants import deviceType,timeZone,debugMode,yourGmail,gmail_SENDING_appPass
from logger360 import collect_data
from sftp_handler import getLogs
from datetime import datetime,timedelta
import os
from pytz import timezone
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
import geopy.distance
from time import sleep
geolocator = Nominatim(user_agent="Triangular-inator")


tz = timezone(timeZone)

now = datetime.now(tz)

month = now.month
day = now.day
year = now.year


main_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__))))
if deviceType == "windows":
    iHateWindows = "\logs\ "
    logPath = main_path + iHateWindows.strip()
else:
    logPath = main_path + "/logs/"


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
                if name in names:
                    pass
                else:
                    names.append(name)
                Dict.setdefault(name, []).append([name, latitude, longitude, time, dateFromFilename, battery,batteryCharging,inTransit,speed])



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

def getSpeedWinner():
    topSpeed = float(0)
    winner = "Tomatohead"
    collect_csv_through_dates("",7,datetime.now(tz).date())
    for name in names:
        for value in Dict[name]:
            if float(value[8]) >= 10:
                speed = float(value[8])

                if float(speed) > topSpeed:
                    winner = name
                    topSpeed = float(speed)
                    if debugMode == True: print("new top speed is: " + str(topSpeed) + " by " + name)

    topSpeed = str(float(topSpeed * 2.237))[:4]                
    return winner,topSpeed

winnerName, winnerSpeed = getSpeedWinner()

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

html += f'<p style="text-align:center"><strong><span style="font-size:14px"><span style="font-family:Courier New,Courier,monospace">{month} / {day} / {year}</span></span></strong></p> <h1 style="text-align:center">Your weekly life360 data update!</h1> <p style="text-align:center">Our top speed winner this week was:&nbsp;</p> <p style="text-align:center"><span style="font-size:18px">{winnerName}!</span></p> <p style="text-align:center">With a speed of:&nbsp;</p> <p style="text-align:center"><em><span style="font-size:24px"><span style="color:#e74c3c"><strong>🔥 {winnerSpeed} MPH! 🔥</strong></span></span></em></p> <p>&nbsp;</p>'

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
    for email in emailList:
        print("Sending email to " + email)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Weekly Update!"
        msg['From'] = yourGmail
        msg['To'] = email
        #send_email_out(email)
        print("Sent! Waiting a sec to send next email!\n")
        sleep(1)