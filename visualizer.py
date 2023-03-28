import os
from tkinter import *
from PIL import ImageTk, Image  
from tkintermapview import TkinterMapView
from tkcalendar import Calendar, DateEntry
import csv
import datetime
from analysis import create_location_dictionary,clean_location_dictionary
from elapsedTime import calculate_time_spent
from constants import deviceType,remote_logs_directory,local_logs_directory,serverHostname,serverPort,serverUser,serverPass
import sys

root = Tk()
root.title('Location Viewer')
root.iconbitmap("")
root.geometry("900x800")
root.resizable(0,0)
map_widget = TkinterMapView(root, width=600, height=600, corner_radius=0)
map_widget.set_position(38.06699076662477, -78.87535905288384)
map_widget.set_zoom(6)
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
def collect_data(name):
    #Getting all of the CSV Files
    for path, subdirs, files in os.walk(logPath + name):
        for name in files:
            if ".csv" in name:
                csv_Files.append(str(os.path.join(path, name)))

            else:
                pass

    #Reading all of the CSV files and converting their data to a dictionary
    
    # ^ empty dictionary
    
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
                if name in names:
                    pass
                else:
                    names.append(name)
                Dict.setdefault(name, []).append([name, latitude, longitude, time, dateFromFilename, battery])
           
collect_data("")

def getDates():
    
    for name in names:
        for value in Dict[name]:
            date = value[4]
            if date not in dates:
                dates.append(date)
            else:
                pass
    dates.sort()
getDates()





precision_var = IntVar()
frequency_var = IntVar()
latlongLabel = Label(root,text="~111 km \n\n~11.1 km \n\n~1.1 km \n\n~110 m \n\n~11 m \n\n~1.1 m \n\n~0.11 m", font= ("Helvetica Neue", 9,'italic'))
latlongLabel.place(x=670,y=280,anchor="center")

    


    

def PointsOfInterest():
    precisionScale = Scale(root,from_=0,to=6,variable=precision_var,orient='vertical',length=150)
    precisionScale.place(x=618,y=280,anchor="center")

    frequencyScale = Scale(root,from_=10,to=5000,variable=frequency_var,orient='vertical',resolution=10,length=200)
    frequencyScale.place(x=865,y=300,anchor="center")

def reset_map():
    global map_widget
    map_widget.place_forget()
    map_widget = TkinterMapView(root, width=600, height=600, corner_radius=0)
    map_widget.set_position(38.06699076662477, -78.87535905288384)
    map_widget.set_zoom(6)
    map_widget.place(x=300,y=500,anchor="center")

def helperText():
    title = Label(root,text="Life 360 Circle Members:", font= ("Helvetica Neue", 24,'bold'))
    title.place(x=10,y=10)

    nameLabel = Label(root,text="Currently Viewing", font= ("Helvetica Neue", 18,'bold'))
    nameLabel.place(x=480,y=10,anchor="center")

    logLabel = Label(root,text="Logs", font= ("Helvetica Neue", 18,'bold'))
    logLabel.place(x=655,y=445,anchor="center")


    poi_accuracyLabel = Label(root,text="Accuracy", font= ("Helvetica Neue", 13,'bold'))
    poi_accuracyLabel.place(x=640,y=190,anchor="center")

    poi_frequencyLabel = Label(root,text="How many coordinates\n makes a POI", font= ("Helvetica Neue", 10,'bold'))
    poi_frequencyLabel.place(x=840,y=180,anchor="center")


def calWidget():

    calLabel = Label(root,text="Viewable Dates", font= ("Helvetica Neue", 18,'bold'))
    calLabel.place(x=750,y=210,anchor="center")
    def print_sel():
        print(cal.selection_get())
        cal.see(datetime.date(year=2016, month=2, day=5))

    today = datetime.date.today()

    mindate = datetime.date(year=2022, month=11, day=21)


    cal = Calendar(root, font="Arial 14", foreground="black", selectmode='day', locale='en_US',
                   mindate=mindate, disabledforeground='red',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.place(x=750,y=320,anchor="center")

dateBox = Listbox(root,width=10,height=15,selectmode="multiple")
dateBox.place(x=665,y=590,anchor="center")
scrollbar = Scrollbar(root,orient=VERTICAL,command=dateBox.yview)

dateBox['yscrollcommand'] = scrollbar.set

scrollbar.place(x=610,y=590,height=255,anchor="center")

def data_analysis(pin_precision,frequency_cutoff):
    
    if pin_precision != "" and frequency_cutoff != "":
        precision_value = pin_precision
        frequency_value = frequency_cutoff

    else:
        precision_value = int(precision_var.get())
        frequency_value = int(frequency_var.get())

    reset_map()
    ourList = create_location_dictionary(Dict,precision_value)
    unique = clean_location_dictionary(ourList,frequency_value)

    locations = []
    for key, value in unique.items() :
        for dit in value:
            if dit["coordinates"] not in locations:
                locations.append(dit["coordinates"])

   
    for value in locations:
            val = str(value)
            lat, long = val.split(", ")
            marker = map_widget.set_position(float(lat),float(long), marker=True, text= str("POI"),marker_color_circle = "black",marker_color_outside = "grey", text_color = "black")
            

analyzeButton = Button(root,text = "Analyze POIs", font=("Helvetica Neue", 20,'bold'),command=lambda ewq = "" : data_analysis("",""), background="blue", disabledforeground="yellow")
analyzeButton.place(x=755,y=400,anchor="center")

def dateViewManager():
    for date in dates:
        dateBox.insert("end", date)

dateViewManager()



activeNames = []
listbox = Listbox(root,width=20,height=len(names))
listbox.place(x=480,y=95,anchor="center")

def trackingViewManger(name):
    if name not in activeNames:
        activeNames.append(name)
        
        listbox.insert("end",name)
    else:
        activeNames.remove(name)
    
        idx = listbox.get(0, "end").index(name)
        listbox.delete(idx)


togglePaths = BooleanVar()
toggleMarkers = BooleanVar()
togglePOI = BooleanVar()



def mapSettings():

    mapSettingsLabel = Label(root,text="Map Settings", font= ("Helvetica Neue", 18,'bold'))
    mapSettingsLabel.place(x=730,y=20,anchor="center")

    satButton = Button(root,text = "Satalite", font=("Helvetica Neue", 14,'bold'),command=lambda ewq = "" : map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22), background="blue", disabledforeground="yellow")
    satButton.place(x=600,y=60,anchor="w")

    streetButton = Button(root,text = "Google Maps", font=("Helvetica Neue", 14,'bold'),command=lambda ewq = "" :map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22), background="blue", disabledforeground="yellow")
    streetButton.place(x=600,y=90,anchor="w")

    classicButton = Button(root,text = "Regular", font=("Helvetica Neue", 14,'bold'),command=lambda ewq = "" :map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"), background="blue", disabledforeground="yellow")
    classicButton.place(x=600,y=120,anchor="w")

    pathToggle = Checkbutton(root,text = "Show Paths",variable=togglePaths, onvalue=True, offvalue=False,)
    
    pathToggle.place(x=780,y=60,anchor="w")

    markerToggle = Checkbutton(root,text = "Show Markers",variable=toggleMarkers, onvalue=True, offvalue=False)
    markerToggle.select()
    markerToggle.place(x=780,y=90,anchor="w")

    POIToggle = Checkbutton(root,text = "Show POI's",variable=togglePOI, onvalue=True, offvalue=False,)
    
    POIToggle.place(x=780,y=120,anchor="w")



classicButton = Button(root,text = "Reset Map", font=("Helvetica Neue", 10,'bold'),command=lambda ewq = "" :reset_map(), background="blue", disabledforeground="yellow")
classicButton.place(x=600,y=150,anchor="w") 


def personButtonCommand(name,color,pathColor,multiplePeople):
    filtered_data = []
    selectedDates = []
    unique_positions = set()
    MultipleDates = False
    
    precision_value = int(precision_var.get())
    
    for i in dateBox.curselection():
        selectedDates.append(dateBox.get(i))

    
    for value in Dict[name]:

        
        if value[4] in selectedDates:
            
            # Extract the latitude and longitude from the current item
            lat_long = (round(float(value[1]), precision_value), round(float(value[2]), precision_value))

            # Check if the current latitude and longitude pair is already in the set
            if lat_long not in unique_positions:
                unique_positions.add(lat_long)
                filtered_data.append(value)

    if len(selectedDates) > 1:
        MultipleDates = True
    
    if togglePaths.get():
        personPath = map_widget.set_path([(float(filtered_data[0][1]),float(filtered_data[0][2])),(float(filtered_data[1][1]),float(filtered_data[1][2]))],color = pathColor)
        nametag = map_widget.set_marker(float(filtered_data[0][1]),float(filtered_data[0][2]),text=filtered_data[0][0],marker_color_circle = pathColor,marker_color_outside = color, text_color = "black")
        skipFirst2coords = 0

    if togglePOI.get():
        data_analysis("","")

    for value in filtered_data:
        text = str(value[3])
        if multiplePeople == True:
            text = str(value[0]) + " @ " + str(value[3])
        if MultipleDates == True:
            text = str(value[3]) + "|" + str(value[4])
        if multiplePeople == True and MultipleDates == True:
            text = str(value[0]) + " @ " + str(value[3]) + "|" + str(value[4])

        if toggleMarkers.get():
            map_widget.set_position(float(value[1]),float(value[2]), marker=True, text=text,marker_color_circle = pathColor,marker_color_outside = color, text_color = "black")

        if togglePaths.get():
            if skipFirst2coords > 2:
                personPath.add_position(float(value[1]),float(value[2]))
            else:
                skipFirst2coords += 1
        


    
def calculatePaths():
    reset_map()
    color = "deeppink1"
    pathColor = "deeppink4"
    colorCount = 0
    colors = ["firebrick2","lightsalmon4","gold1","chartreuse","royalblue1","darkorchid1","magenta","maroon","slategray1"]
    pathColors = ["firebrick4","darkorange","orange3","springgreen3","dodgerblue4","darkorchid4","magenta4","sienna4","slategray4"]
    prevName = activeNames[0]
    multiplePeople = False

    if len(activeNames) > 1:
        multiplePeople = True

    for person in activeNames:
        if person != prevName:
            color = colors[colorCount]
            pathColor = pathColors[colorCount]
            colorCount += 1
        personButtonCommand(person,color,pathColor,multiplePeople)


calcButton = Button(root,text = "Plot Data", font=("Helvetica Neue", 24,'bold'),command=lambda ewq = "" : calculatePaths(), background="blue", disabledforeground="yellow")
calcButton.place(x=820,y=760,anchor="center")

def getLogs():
    from sftp_handler import fileGrab
    import shutil
    try:
        for subdirs in os.walk(logPath):
            for dir in subdirs:
                shutil.rmtree(dir)
    except TypeError:
        print("deleted all logs!")

    print("\nRedownloading now!")
    os.mkdir(logPath)
    fileGrab(serverHostname,serverPort,serverUser,serverPass,remote_logs_directory,local_logs_directory)
    exit()



getLogsButton = Button(root,text = "Download Logs", font=("Helvetica Neue", 12,'bold'),command=lambda ewq = "" : getLogs(), background="blue", disabledforeground="yellow")

getLogsButton.place(x=670,y=740,anchor="center")

gridRow = 60
gridColumn = 80


def createButton(name,gridRow,gridColumn):
            
    def buttonGlyph():
        theirButton = Button(root,text=name,command=lambda j = name : trackingViewManger(j))

        theirButton.place(x=gridRow,y=gridColumn,anchor="center")

    buttonGlyph()

for value in names:

    if gridColumn >= 200:
        gridColumn = 80
        gridRow += 115
            
    createButton(value,gridRow,gridColumn)
    gridColumn += 40


#print(calculate_time_spent(Dict))

mapSettings()
helperText()
PointsOfInterest()
#calWidget()
map_widget.place(x=300,y=500,anchor="center")
getDates()
root.mainloop()