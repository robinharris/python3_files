
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as gdate
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(filename='homeDataAnalysis.log', level = logging.INFO)
log = logging.getLogger("ex")

# SQLite DB Name
DB_Name =  "home.db"

connection = sqlite3.connect(DB_Name)
cursor = connection.cursor()

level1Set = set([1,2,3])
level2Set = set([1,2,3,4,5])
level1 = 0
level2 = 0
dataSelected = []
sensorid = []
timestamp = []
temperature = []
voltageList = []
roomTemperatureList = []
outsideTemperatureList = []
dayTimeList = []
rooms = dict({1:'Lounge', 2:'Conservatory', 3:'Workshop', 4:'Outside', 5:'Bedroom'})
dataType = dict({1:'temp', 2:'voltage'})

#define a function to return the key for sorting
def getKey(row):
   return row[1]


def level1Menu():
    global level1
    logging.info('Start level1 menu')
    while (not level1 in level1Set): 
        print ("LEVEL 1 MENU")
        print ("1.\tTemperature")
        print ("2.\tVoltage")
        print ("3.\tExit")
        level1 = int(input("Enter 1, 2, or 3: "))
    logging.info('Finished level1')


def level2Menu():
    global level2
    logging.info('Starting level2 menu')
    print ("LEVEL 2 MENU")
    print ("1.\tLounge")
    print ("2.\tConservatory")
    print ("3.\tWorkshop")
    print ("4.\tOutside")
    print ("5.\tBedroom")
    print ("6.\tBack")
    level2 = int(input("Enter 1, 2, 3, 4, 5 or 6: "))
    logging.info('Finished level2')

def level3Menu():
    global startDate, endDate
    logging.info('Starting level3')
    #set default start and end dates to speed things up on testing
    startDay = '15'
    startMonth = '04'
    startYear = '2017'
    timeNow = datetime.now()
    endDay = '25'
    endMonth = '07'
    endYear = '2017'
    print ("LEVEL 3 MENU")
    userInput = input("Enter start day: ")
    if (userInput != ''):
        if (len(userInput) == 1):
            userInput = '0' + userInput
        startDay = userInput
    userInput = input("Enter start month: ")
    if (userInput != ''):
        if (len(userInput) == 1):
            userInput = '0' + userInput
        startMonth = userInput
    userInput = input("Enter start year: ")
    if (userInput != ''):
        startYear = userInput
    startDate = startYear + startMonth + startDay
    userInput = input("Enter end day: ")
    if (userInput != ''):
        if (len(userInput) == 1):
            userInput = '0' + userInput        
        endDay = userInput
    userInput = input("Enter end month: ")
    if (userInput != ''):
        if (len(userInput) == 1):
            userInput = '0' + userInput           
        endMonth = userInput
    userInput = input("Enter end year: ")
    if (userInput != ''):
        endYear = userInput
        endDate = endYear + endMonth + endDay
    logging.info ('startDate %s', startDate)
    endDate = endYear + endMonth + endDay
    logging.info ('endDate %s', endDate)
    if (endDate < startDate):
        print("End date must be after start date, try again")
        endDate = '0'

def main():
    logging.info('Starting')
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
        if (level2 == 6):
            level1 = 0 #reset menu choices
            level2 = 0 #reset menu choices
    level3Menu()

    selectString = "SELECT sensorid, date, " + str(dataType[level1].strip('\''))
    selectString += " FROM sensordata WHERE sensorID = \'" + str(rooms[level2].strip('\'') + "\'")
    selectString += " AND date > \'" + startDate + "\'"
    selectString += " AND date < \'" + endDate + "\'"
    logging.info(selectString)
    try:
        cursor.execute(selectString) 
        dataSelected = cursor.fetchall()
    except Exception as e:
        log.exception("Error %s", e)
    
    for row in dataSelected:
        sensorid.append(row[0])
        timestamp.append(datetime.strptime(row[1], "%Y%m%d %H:%M:%S"))
        temperature.append(row[2])

    xAxis = []
    logging.info("Starting to create xAxis")
    for i in range(0, len(dataSelected)):
        xAxis.append(gdate.date2num(timestamp[i]))
    
    logging.info("Starting to graph")
    startX = gdate.date2num(datetime.strptime(startDate,"%Y%m%d"))
    endX = gdate.date2num(datetime.strptime(endDate,"%Y%m%d"))
    
    fig = plt.figure(figsize=(8,6))
    # fig.suptitle('Room Temperatures')
    fig.suptitle(rooms[level2] + " Temperature")
    ax1 = plt.subplot2grid((1,1),(0,0))
    # ax2 = plt.subplot2grid((2,1),(1,0))

    # Set major x ticks on Mondays.
    ax1.set_xlim(startX, endX)
    ax1.set_ylim(0, 50)
    # plt.plot(timestamp, temperature)

    # plt.subplots_adjust(hspace = 0.5)
    ax1.plot(timestamp, temperature, 'r.', ls='None',markersize =3, label='Temperature')

    for tick in ax1.xaxis.get_ticklabels():
        tick.set_rotation(90)

    ax1.xaxis.set_major_locator(
        gdate.WeekdayLocator(byweekday=gdate.MO)
    )
    ax1.xaxis.set_major_formatter(
        gdate.DateFormatter('%d %b')
    )
    plt.show()





main()

print ("The highest temperature was: ",max(temperature))
print ("The lowest temperature was: ",min(temperature))



##
##plt.show()
