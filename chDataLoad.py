#------------------------------------------
#--- Author: Robin Harris
#--- Date: 23rd November 2018
#--- Version: 3.0
#--- Python Ver: 3.6
#------------------------------------------

import paho.mqtt.client as paho
import datetime
import mysql.connector
import time

# a class from which an instance of each device is created.  This enables fields to be collated into one device
# instance and when complete, inserted into the database
class device:
    def __init__(self, owner, now, temperature, pressure, humidity, pm10, pm25, voc):
        self.owner = owner
        self.now = now
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.pm10 = pm10
        self.pm25 = pm25
        self.voc = voc

# create instances of the device class with all fields set to None
aq1 = device('rh', None, None, None, None, None, None, None)
aq2 = device('rh', None, None, None, None, None, None, None)
ESP_Easy = device('ms', None, None, None, None, None, None, None)
ajaqi_1 = device('aj', None, None, None, None, None, None, None)
#set up a dictionary of devices
deviceDict = {"aq1": aq1, "aq2":aq2, "ESP_Easy": ESP_Easy, "ajaqi_1": ajaqi_1 }

#mqtt settings
mqttBroker = '172.26.6.1' # the internal IP address so we don't use chargeable bandwidth
mqttClientUser = "connectedhumber"
mqttClientPassword = "3fds8gssf6"

# global variables
dev_id = None

def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        mqttc.subscribe("#", 0)

def on_message(mqttc, obj, msg):
    global dev_id # use the global variable
    topic = str(msg.topic)

    # topic trees sometimes start with /air/rh etc. and sometimes with air/rh etc.  
    # remove the leading '/'
    if topic.startswith('/'):
        topic = topic[1:]
    # now split the topic tree into strings
    topicTree = topic.split("/")
    topicTreeLevels = len(topicTree) # the number of levels in the topic tree

    owner = topicTree[1] # owner is the second level - 0 is level 1 so 1 is level 2

    dev_id = topicTree[2] # the device_id is in the third level of the tree

    # set the time for this collation of fields to the time of the last one arriving
    deviceDict[dev_id].now = datetime.datetime.now()

    field = topicTree[-1] # the field is the last level in the topic tree
    value = msg.payload.decode("utf-8") # the value of the above field is the topic payload
    value = float(value) # convert the strong payload to a float
    value = round(value) # round the float to no decimal places

    # set the instance variable for the relevant device field
    if field == 'temperature':
        deviceDict[dev_id].temperature = value
    elif field == 'pressure':
        deviceDict[dev_id].pressure = value
    elif field == 'humidity':
        deviceDict[dev_id].humidity = value
    elif field == 'pm10':
        deviceDict[dev_id].pm10 = value
    elif field == 'pm25':
        deviceDict[dev_id].pm25 = value
    elif field == 'voc':
        deviceDict[dev_id].voc = value

mqttc = paho.Client() # create an instance of the paho Client
mqttc.username_pw_set(username= mqttClientUser, password=mqttClientPassword)

# set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect

# connect to the broker
mqttc.connect(mqttBroker)

# database connection.  Note that since this program runs on the same server as the database the
# host is localhost
mydb = mysql.connector.connect(
  host="localhost",
  user="robinusr",
  passwd="spanTHEr1v3r",
  database="robindb"
)

# create a cursor object
mycursor = mydb.cursor()

# loop forever checking the dev_id which is set by the callback on_message
# then check if the instance for that device is complete and if it is insert a record using the cursor object
# loop forever
try:
    while (True):
    if (((dev_id == 'aq1') or (dev_id == 'aq2')  or (dev_id =='ajaqi_1')) and (not None in (deviceDict[dev_id].temperature,
     deviceDict[dev_id].pressure, deviceDict[dev_id].humidity, deviceDict[dev_id].pm10, deviceDict[dev_id].pm25))):
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, temperature, pressure, humidity, pm10, pm25) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        vals = (deviceDict[dev_id].now, deviceDict[dev_id].owner, dev_id, deviceDict[dev_id].temperature, deviceDict[dev_id].pressure,
         deviceDict[dev_id].humidity, deviceDict[dev_id].pm10, deviceDict[dev_id].pm25)
        mycursor.execute(sql, vals)
        # commit the change
        mydb.commit()
        # seems to need time to complete the commit 
        time.sleep(1)
        # set all the instance fields to None to restart the collation process
        deviceDict[dev_id].temperature = deviceDict[dev_id].humidity = deviceDict[dev_id].pressure = deviceDict[dev_id].pm10 = deviceDict[dev_id].pm25 = deviceDict[dev_id].now = None

    if (dev_id == 'ESP_Easy' and (not None in (deviceDict[dev_id].pm10, deviceDict[dev_id].pm25))):
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, pm10, pm25) VALUES (%s, %s, %s, %s, %s)"
        vals = (deviceDict[dev_id].now, deviceDict[dev_id].owner, dev_id,
         deviceDict[dev_id].pm10, deviceDict[dev_id].pm25)
        mycursor.execute(sql, vals)
        # commit the change
        mydb.commit()
        # seems to need time to complete the commit 
        time.sleep(1)
        # set all the instance fields to None to restart the collation process
        deviceDict[dev_id].temperature = deviceDict[dev_id].humidity = deviceDict[dev_id].pressure = deviceDict[dev_id].pm10 = deviceDict[dev_id].pm25 = deviceDict[dev_id].now = None
    mqttc.loop()
except:
    print("An error occured in the main loop")
