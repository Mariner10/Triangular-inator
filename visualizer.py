import os
from tkinter import *
from PIL import ImageTk, Image  
from tkintermapview import TkinterMapView
from tkcalendar import Calendar, DateEntry
import csv

root = Tk()
root.title('Location Viewer')
root.iconbitmap("")
root.geometry("900x800")
root.resizable(0,0)
map_widget = TkinterMapView(root, width=600, height=600, corner_radius=0)
map_widget.set_zoom(1)
main_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__)))) + "/"


Dict = {}
names = []
dates = []
name = ""
csv_Files = []
def collect_data(name):
    #Getting all of the CSV Files
    for path, subdirs, files in os.walk(main_path + "logs/" + name):
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

def helperText():
    title = Label(root,text="Life 360 Circle Members:", font= ("Helvetica Neue", 24,'bold'))
    title.place(x=10,y=10)

    calLabel = Label(root,text="Viewable Dates", font= ("Helvetica Neue", 18,'bold'))
    calLabel.place(x=750,y=210,anchor="center")

    nameLabel = Label(root,text="Currently Viewing", font= ("Helvetica Neue", 18,'bold'))
    nameLabel.place(x=480,y=10,anchor="center")

    logLabel = Label(root,text="Logs", font= ("Helvetica Neue", 18,'bold'))
    logLabel.place(x=655,y=445,anchor="center")


def calWidget():
    def print_sel():
        print(cal.selection_get())
        cal.see(datetime.date(year=2016, month=2, day=5))

    

    import datetime
    today = datetime.date.today()

    mindate = datetime.date(year=2022, month=11, day=21)


    cal = Calendar(root, font="Arial 14", foreground="black", selectmode='day', locale='en_US',
                   mindate=mindate, disabledforeground='red',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.place(x=750,y=320,anchor="center")

dateBox = Listbox(root,width=10,height=15,selectmode="multiple")
dateBox.place(x=665,y=600,anchor="center")
scrollbar = Scrollbar(root,orient=VERTICAL,command=dateBox.yview)

dateBox['yscrollcommand'] = scrollbar.set

scrollbar.place(x=605,y=600,height=255,anchor="center")

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


def mapSettings():

    mapSettingsLabel = Label(root,text="Map Settings", font= ("Helvetica Neue", 18,'bold'))
    mapSettingsLabel.place(x=730,y=20,anchor="center")

    satButton = Button(root,text = "Satalite", font=("Helvetica Neue", 14,'bold'),command=lambda ewq = "" : map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22), background="blue", disabledforeground="yellow")
    satButton.place(x=650,y=60,anchor="center")

    streetButton = Button(root,text = "Regular", font=("Helvetica Neue", 14,'bold'),command=lambda ewq = "" :map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22), background="blue", disabledforeground="yellow")
    streetButton.place(x=650,y=100,anchor="center")

    classicButton = Button(root,text = "Classic", font=("Helvetica Neue", 14,'bold'),command=lambda ewq = "" :map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"), background="blue", disabledforeground="yellow")
    classicButton.place(x=650,y=140,anchor="center")


def reset_map():
    global map_widget
    map_widget.place_forget()
    
    map_widget = TkinterMapView(root, width=600, height=600, corner_radius=0)
    map_widget.set_zoom(1)
    map_widget.place(x=300,y=500,anchor="center")

classicButton = Button(root,text = "Reset Map", font=("Helvetica Neue", 10,'bold'),command=lambda ewq = "" :reset_map(), background="blue", disabledforeground="yellow")
classicButton.place(x=800,y=100,anchor="center") 


def personButtonCommand(name):
    filtered_data = []
    selectedDates = []
    unique_positions = set()
    
    for i in dateBox.curselection():
        selectedDates.append(dateBox.get(i))

    
    for value in Dict[name]:

        
        if value[4] in selectedDates:
            
            # Extract the latitude and longitude from the current item
            lat_long = (round(float(value[1]), 4), round(float(value[2]), 4))

            # Check if the current latitude and longitude pair is already in the set
            if lat_long not in unique_positions:
                unique_positions.add(lat_long)
                filtered_data.append(value)

                

        
    
    for value in filtered_data:
        map_widget.set_position(float(value[1]),float(value[2]), marker=True, text= str(value[0]) + " @ " + str(value[3]) + "|" + str(value[4]))



    
def calculateIt():
    reset_map()
    for person in activeNames:
        personButtonCommand(person)

calcButton = Button(root,text = "Calculate!", font=("Helvetica Neue", 24,'bold'),command=lambda ewq = "" : calculateIt(), background="blue", disabledforeground="yellow")
calcButton.place(x=750,y=760,anchor="center")

 

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


mapSettings()
helperText()
calWidget()
map_widget.place(x=300,y=500,anchor="center")
getDates()
root.mainloop()