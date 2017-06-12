
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# SQLite DB Name
DB_Name =  "home_6Jun.db"

connection = sqlite3.connect(DB_Name)
cursor = connection.cursor()

level1Set = set([1,2,3])
level2Set = set([1,2,3,4])
level1 = 0
level2 = 0
startDate = datetime(2017,1,1)
endDate = datetime(2017,1,1)
dataSelected = []
sensorid = []
timestamp = []
temperature = []
voltageList = []
roomTemperatureList = []
outsideTemperatureList = []
dayTimeList = []
rooms = dict({1:'Lounge', 2:'Conservatory', 3:'Workshop', 4:'Outside'})


def level1Menu():
    global level1
    while (not level1 in level1Set): 
        print ("LEVEL 1 MENU")
        print ("1.\tTemperature")
        print ("2.\tVoltage")
        print ("3.\tExit")
        level1 = int(input("Enter 1, 2, or 3: "))

def level2Menu():
    global level2
    print ("LEVEL 2 MENU")
    print ("1.\tLounge")
    print ("2.\tConservatory")
    print ("3.\tWorkshop")
    print ("4.\tBack")
    level2 = int(input("Enter 1, 2, 3 or 4: "))

def level3Menu():
    startDay = 1
    startMonth = 6
    startYear = 2017
    timeNow = datetime.now()
    endDay = timeNow.day
    endMonth = timeNow.month
    endYear = timeNow.year
    print ("LEVEL 3 MENU")
    userInput = input("Enter start day: ")
    if (userInput != ''):
        startDay = int(userInput)
    userInput = input("Enter start month: ")
    if (userInput != ''):
        startMonth = int(userInput)
    userInput = input("Enter start year: ")
    if (userInput != ''):
        startYear = int(userInput)
    userInput = input("Enter end day: ")
    if (userInput != ''):
        endDay = int(userInput)
    userInput = input("Enter end month: ")
    if (userInput != ''):
        endMonth = int(userInput)
    userInput = input("Enter end year: ")
    if (userInput != ''):
        endYear = int(userInput)
    print(startDay, startMonth, startYear, endDay, endMonth, endYear)
    startDate = datetime(startYear, startMonth, startDay)
    endDate = datetime(endYear, endMonth, endDay)

def main():
    global startDay, startMonth, startYear
    global endDay, endMonth, endYear
    global level1, level2
    global rooms
    while (level1 == 0):
        level1Menu()
        if (level1 == 3):
            print("bye")
            exit()
        level2Menu()
        if (level2 == 4):
            level1 = 0 #reset menu choices
            level2 = 0 #reset menu choices
    level3Menu()
    cursor.execute("SELECT sensorid, date, temp, voltage FROM sensordata WHERE sensorID=? LIMIT 5", [rooms[level1].strip('\'')])    ##fetch all the data selected
    dataSelected = cursor.fetchall()
    for row in dataSelected:
        print(row)
                   

main()


#testing stuff here
print("level1: ", end ='')
print(level1)
print("level2: ", end ='')
print(level2)


##chosenRoom = input("Which room? ")
###define a function to return the key for sorting
##def getKey(row):
##    return row[2]
##
##cursor.execute("SELECT sensorid, date, temp FROM sensordata WHERE date > 20170509 and sensorID=?", [chosenRoom])
###fetch all the data selected
##dataSelected = cursor.fetchall()
##
##sortedDataSelected = sorted(dataSelected, key = getKey)
###split the data intio separate lists so they can be plotted
##for row in dataSelected:
##    sensorid.append(row[0])
##    timestamp.append(row[1])
##    temperature.append(row[2])
##    ##print (row)
##
###convert timestamp to datetime format
##timestamp = [datetime.strptime(x, '%Y%m%d %H:%M:%S') for x in timestamp]
##
###startDate = datetime(2017,6,5)
###endDate = datetime(2017,6,6)
##startMonth = int(input("Start month? "))
##startDay = int(input("Start day? "))
##endMonth = int(input("End month? "))
##endDay = int(input("End day? "))
##
##startDate = datetime(2017, startMonth, startDay)
##endDate = datetime(2017, endMonth, endDay)
##
##
##
###print ("The highest temperature was: ",max(temperature))
###print ("The lowest temperature was: ",min(temperature))
##
####content = [x.strip() for x in content]
####
####contentFloat = []
####for value in content:
####    contentFloat.append(float(value))
####
####xAxis = []
####for i in range (0, len(dataSelected)):
####    xAxis.append(i)
####
####plt.scatter(timestamp, temperature)
##plt.plot(timestamp, temperature)
##plt.scatter(timestamp, temperature)
##plt.title('Room Temperature')
##plt.ylabel('Degrees C')
####plt.legend()
##plt.xlim(startDate, endDate)
##plt.ylim(0, 50)
##plt.show()
