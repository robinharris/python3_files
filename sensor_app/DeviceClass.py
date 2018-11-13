'''
Class definition of an object to represent a home automation sensor unit.
    Data attributes:
    Name - string
    Location - string
    Battery type - string
    Battery capacity mAh - integer
    Sketch name - string
    deviceList - list of objects called sessions which start at the end of charging
                and end when the battery is fully discharged

    Author: Robin Harris
    Version: 1.0
    Date: 28th March 2018
'''
from RunTimeClass import RunTime
import os
from datetime import datetime

class Device:
    '''
    A sensor unit for home automation
    '''
    # Class attribute to keep track of the number of devices
    numberOfDevices = 0

    def __init__(self, name):
        self.name = name
        self.location = input("Location: ")
        self.location = self.location[:16].lower()
        self.batteryType = input("Battery type: ")
        self.batteryType = self.batteryType[:16].lower()
        self.batteryCapacity = int(input("Capacity mAh: "))
        self.sketchName = input("Sketch name (Max 16 characters): ")
        self.location = self.location[:16]
        self.sessions = []
        self.averageRunTime = 0
        self.averageRunTimePermAh = 0
        Device.numberOfDevices+= 1

    @staticmethod
    def _getTimestamp():
        os.system('clear')
        isValid = False
        year = 2018
        while not isValid:
            month = int(input("Month number: "))
            if month <= 12:
                isValid = True
        isValid = False
        while not isValid:
            day = int(input("Day number: "))
            if month == 2:
                if day <= 28:
                    isValid = True
            elif (month == 4 or month == 6 or month == 9 or month == 11):
                if day <= 30:
                    isValid = True
            else:
                if (day <= 31):
                    isValid = True
        isValid = False
        while not isValid:
            hour = int(input("Hour (24 hour): "))
            if hour <= 23:
                isValid = True
        isValid = False
        while not isValid:
            minute = int(input("Minute: "))
            if minute <= 59:
                isValid = True
        enteredTimestamp = datetime(year, month, day, hour, minute)
        return(enteredTimestamp)

    @staticmethod
    def _calculateMeanRunTime(self):
        '''
        Calculates the average run time on a charge in minutes
        Also calculates the average run time per mAh
        '''
        if len(self.sessions) == 0:
            self.averageRunTime = 0
            self.averageRunTimePermAh = 0
            print("Set averages to zero")
        else:
            runningTotal = 0
            for session in self.sessions:
                if session.durationMinutes:
                    runningTotal += session.durationMinutes
                    self.averageRunTime = int(runningTotal / (len(self.sessions))) 
                    self.averageRunTimePermAh = self.averageRunTime / self.batteryCapacity



    def describeDevice(self):
        '''
        Prints the attributes of a device
        '''
        print ("\nName: ", self.name)
        print ("Location: ", self.location)
        print ("Battery Type: ", self.batteryType)
        print ("Capacity: ", str(self.batteryCapacity))
        print ("Sketch: ", self.sketchName)
        print ("Average run time: \t", self.averageRunTime)
        print ("Average run time per mAh:\t {0:6.2f}". format(self.averageRunTimePermAh))
        for session in self.sessions:
            session.printSession()
        print("\n")

    def editDevice(self):
        '''
        Provides an ability to change any device attribute EXCEPT sessions
        '''
        self.describeDevice()
        try:
            userInput = None
            userInput = input("\nName: " + self.name + "  Type new name or enter to keep  ")
            if userInput:
                self.name = userInput
                print("\nName changed to " + self.name)
            userInput = None
            userInput = input("\nLocation: " + self.location + "  Type new location or enter to keep  ")
            if userInput:
                self.location = userInput
                print("\nLocation changed to " + self.location)
            userInput = None
            userInput = input("\nBattery type: " + self.batteryType + "  Type new battery type or enter to keep  ")
            if userInput:
                self.batteryType = userInput
                print("\nBattery type changed to " + self.batteryType)
            userInput = None
            userInput = input("\nBattery capacity: " + str(self.batteryCapacity) + "  Type new battery capacity or enter to keep  ")
            if userInput:
                self.batteryCapacity = int(userInput)
                print("\nBattery capacity changed to " + str(self.batteryCapacity))
            userInput = None
            userInput = input("\nName: " + self.sketchName + "  Type new sketch name or enter to keep  ")
            if userInput:
                self.sketchName = userInput
                print("\nSketch name changed to " + self.sketchName)
        except ValueError:
            print("Battery capacity must be an integer")


    def updateSession(self):
        '''
        If 'start' is chosen, creates a new session that is added to the deviceList list.
        If 'finish' is chosen, adds the finish time to a previous created session.
        '''
        # experimental code to auto detect start or finish
        timeStamp = Device._getTimestamp()
        if len(self.sessions) > 0:
            if self.sessions[-1].endTime == None:
                self.sessions[-1].addEndTime(timeStamp)
                Device._calculateMeanRunTime(self)
        else:
            self.sessions.append(RunTime(timeStamp))

        
        
        # valueToAdd = input("s for start of f for finish: ")
        # timeStamp = Device._getTimestamp()
        # if valueToAdd.lower() == "s":
        #     self.sessions.append(RunTime(timeStamp))
        # elif valueToAdd.lower() == "f":
        #     self.sessions[-1].addEndTime(timeStamp)
        #     Device._calculateMeanRunTime(self)
        # else:
        #     print("Try again....")

    def deleteSession(self):
        '''
        Remove the selected session from the list
        '''
        for count in range(1, len(self.sessions) + 1):
                    print(str(count) + ".\t")
                    print(self.sessions[count - 1].printSession())
        isValid = False
        try:
            while not isValid:
                userInput = int(input("\nEnter session number:  "))
                if userInput > 0 and userInput <= len(self.sessions) + 1:
                    sessionNumber = userInput - 1
                    isValid = True
        except ValueError:
            print("Not a valid session, try again")
        del self.sessions[sessionNumber]
        print(len(self.sessions))
        Device._calculateMeanRunTime(self)
        print("Session deleted and new averages calculated")

        