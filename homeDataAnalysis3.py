import sqlite3
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(filename='homeDataAnalysis3.log', level = logging.INFO)
log = logging.getLogger("ex")

# SQLite DB Name
DB_Name =  "home_18sep.db"

connection = sqlite3.connect(DB_Name)
cursor = connection.cursor()

dataType = dict({1:'temp', 2:'voltage'})

def level1Menu():
    logging.info('Start level1 menu')
    level1 = 0
    level1Set = set([1,2,3])
    while (not level1 in level1Set): 
        print ("LEVEL 1 MENU")
        print ("1.\tTemperature")
        print ("2.\tVoltage")
        print ("3.\tExit")
        level1 = int(input("Enter 1, 2, or 3: "))
    logging.info('Finished level1')
    return level1

def level2Menu():
    level2 = 0
    level2Set = set([1,2,3,4,5])
    logging.info('Starting level2 menu')
    print ("LEVEL 2 MENU")
    print ("1.\tLounge")
    print ("2.\tConservatory")
    print ("3.\tWorkshop")
    print ("4.\tOutside")
    print ("5.\tBedroom")
    print ("6.\tBack")
    level2 = int(input("Enter 1, 2, 3, 4, 5 or 6: "))
    logging.info('Room selected: ' + str(level2))
    return level2

def level3Menu():
    #returns a list object containing startDate and endDate
    logging.info('Starting level3Menu')
    
    #set default start and end dates to speed things up on testing
    startDay = '15'
    startMonth = '04'
    startYear = '2017'
    endDay = '10'
    endMonth = '08'
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
    
    startDate = startYear + startMonth + startDay
    logging.info ('startDate %s', startDate)
    
    endDate = endYear + endMonth + endDay
    logging.info ('endDate %s', endDate)
    
    if (endDate < startDate):
        print("End date must be after start date, try again")
        endDate = '0'
    
    return (startDate, endDate)

def main():
    """Main calling code for plotting temperature or voltage from an sqlite3 database"""

    logging.info('Starting main')
    
    #get user choice to plot temperature or voltage via level1Menu
    tempOrVoltage = level1Menu()
    if (tempOrVoltage == 3):
        print("bye")
        exit()

    level2 = level2Menu()

    #get start and end dates from level3Menu.  
    (startDate, endDate) = level3Menu()
    logging.info("Start date: " + startDate)
    logging.info("End date: " + endDate)

    #set up a string ready to select data from the SQLite database
    selectString = "SELECT sensorid, date, " + str(dataType[tempOrVoltage].strip('\''))
    selectString += " FROM sensordata WHERE date > \'" + startDate + "\'"
    selectString += " AND date < \'" + endDate + "\'"
    selectString += " AND sensorid = 'Lounge' "
    logging.info(selectString)
    
    
    try:
        cursor.execute(selectString) 
        dataSelected = cursor.fetchall()
    except Exception as e:
        log.exception("Error %s", e)
    
    print (dataSelected)

main()
