'''
Main program of sensor_app which records attributes for home automation sensors in objects.
Objective is to monitor run time on a single battery charge by entering start and end times.

User interface is a command line menu system.

Program calculates duration of runtime and average for each device

Author:  Robin Harris
Version 1.0
Python Version: 3.6
Date 26th March 2018
'''

from DeviceClass import Device
from RunTimeClass import RunTime
from Menu1Class import Menu1

import pickle
from datetime import datetime
from time import sleep
import sys,os

pickleFile = "deviceList.pickle"
deviceList = []

def printDeviceList():
    global deviceList
    for device in deviceList:
        device.describeDevice()

def selectDevice():
    for count in range(1, len(deviceList) + 1):
                print(str(count) + ".\t", deviceList[count - 1].name)
    isValid = False
    try:
        while not isValid:
            userInput = int(input("\nEnter device number:  "))
            if userInput > 0 and userInput <= len(deviceList) + 1:
                deviceNumber = userInput - 1
                isValid = True
    except ValueError:
        print("Not a valid device, try again")
    return deviceList[deviceNumber]

        
def main():
    global deviceList
    try:
        restoreDevices = open(pickleFile, "rb")
        #restore the list of devices
        deviceList = pickle.load(restoreDevices)
        #restore the total number of devices
        Device.numberOfDevices = pickle.load(restoreDevices)
        # for device in deviceList:
        #     device.averageRunTime = 0
        #     device.averageRunTimePermAh = 0
        #     Device._calculateMeanRunTime(device)
    except pickle.PickleError as e:
        print("Unable to load: " + pickleFile)
        print(e)
        
    # construct a top level menu object
    top = Menu1()

    # create an endless loop - the only way out is to choose 'EXIT'
    while True:
        top.displayMenu1()
        if top.choice == 1:
            os.system('clear')
            focusDevice = selectDevice()
            focusDevice.editDevice()
        elif top.choice == 2:
            focusDevice = selectDevice()
            focusDevice.updateSession()
        elif top.choice == 3:
            for device in deviceList:
                device.describeDevice()
        elif top.choice == 4:
            deviceName = input("Enter the device name (Max 8 characters): ")
            deviceName = deviceName[:8].lower()
            try:
                newDevice = Device(deviceName)
            except Exception:
                print("\n\nFailed to create new device\n\n")
                del newDevice
            else:
                print("\n\nDevice created successfully")
                deviceList.append(newDevice)
                os.system('clear')

            printDeviceList()
            print ("Total number of devices now: " + str(Device.numberOfDevices))
        elif top.choice == 5:
            try:
                saveDevices = open(pickleFile, "wb")
                pickle.dump(deviceList, saveDevices)
                pickle.dump(Device.numberOfDevices, saveDevices)
                saveDevices.close()
                print("Devices saved")
            except:
                print("Error writing to file: " + pickleFile)
        elif top.choice == 6:
            focusDevice = selectDevice()
            focusDevice.deleteSession()
        elif top.choice == 7:
            sys.exit(0)

    


if __name__ == "__main__":
    main()
