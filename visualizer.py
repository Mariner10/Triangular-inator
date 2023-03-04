import os
from tkinter import *
from PIL import ImageTk, Image  
from tkintermapview import TkinterMapView
import csv

root = Tk()
root.title('Location Viewer')
root.iconbitmap("")
root.geometry("600x800")
root.resizable(0,0)
map_widget = TkinterMapView(root, width=600, height=600, corner_radius=0)
map_widget.set_zoom(1)
main_path = str(os.path.join(os.path.dirname(os.path.abspath(__file__)))) + "/"


Dict = {}
names = []
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

def personButtonCommand(name):
    filtered_data = []
    unique_positions = set()
    
    for value in Dict[name]:
        # Extract the latitude and longitude from the current item
        lat_long = (round(float(value[1]), 4), round(float(value[2]), 4))

        # Check if the current latitude and longitude pair is already in the set
        if lat_long not in unique_positions:
            unique_positions.add(lat_long)
            filtered_data.append(value)

        
    
    for value in filtered_data:
        map_widget.set_position(float(value[1]),float(value[2]), marker=True, text= str(value[0]) + " @ " + str(value[3]) + "|" + str(value[4]))


 

gridRow = 90
gridColumn = 50


def createButton(name,gridRow,gridColumn):
            
    def buttonGlyph():
        theirButton = Button(root,text=name,command=lambda j = name : personButtonCommand(j))

        theirButton.place(x=gridRow,y=gridColumn,anchor="center")

    buttonGlyph()

for value in names:

    if gridColumn >= 200:
        gridColumn = 50
        gridRow += 130
            
    createButton(value,gridRow,gridColumn)
    gridColumn += 50


map_widget.place(x=300,y=500,anchor="center")
root.mainloop()