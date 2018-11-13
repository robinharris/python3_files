'''
Class definition of an object to hold information about the duration of a discharge cycle
for a device (an object).
    Data attributes:
    Charge complete - timestamp
    Last reading - timestamp
    Duration running on the charge

    Author:  Robin Harris
    Version: 1.0
    Date 27th March 2018 
'''

from datetime import datetime, timedelta
class RunTime():
    '''
    Holds attributes about a single run time period for a device.

    Requires one parameter - start time (timestamp) on construction.
    end time (timestamp) usually added later.  Calculates run time in minutes
    '''
    #This method is the same for all instances so is static
    @staticmethod
    def calculateDuration(self):
        '''
        Calculates number of minutes uptime for a single session.
        '''
        durationDateTime = self.endTime - self.startTime
        self.durationMinutes = int(durationDateTime / timedelta(minutes = 1))

    def __init__ (self, startTime):
        self.startTime = startTime
        self.endTime = None
        self.durationMinutes = None

    def printSession(self):
        formatDate = "%d %b %H:%M"
        if self.endTime == None:
            print("Start:", self.startTime.strftime(formatDate))
        else:
            print("Start:", self.startTime.strftime(formatDate),\
            "\tEnd: ", self.endTime.strftime(formatDate),\
            "\tDuration (minutes): ", self.durationMinutes)

    def addEndTime(self, endTime):
        '''
        Adds an endTime (timestamp).
        '''
        self.endTime = endTime
        RunTime.calculateDuration(self)

