#------------------------------------------
#--- Author: Robin Harris
#--- Date: 23rd November 2018
#--- Version: 2.0
#--- Python Ver: 3.6
#------------------------------------------

import paho.mqtt.client as paho
import datetime
import mysql.connector
import time

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

# create instances of the device class
aq1 = device('rh', None, None, None, None, None, None, None)
aq2 = device('rh', None, None, None, None, None, None, None)
ESP_Easy = device('ms', None, None, None, None, None, None, None)
ajaqi_1 = device('aj', None, None, None, None, None, None, None)
#set up a dictionary of devices
deviceDict = {"aq1": aq1, "aq2":aq2, "ESP_Easy": ESP_Easy, "ajaqi_1": ajaqi_1 }

#mqtt settings
mqttBroker = '172.26.6.1'
mqttClientUser = "connectedhumber"
mqttClientPassword = "3fds8gssf6"

dev_id = None

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    if rc==0:
        print("connected OK Returned code=" + str(rc))
        mqttc.subscribe("#", 0)
    else:
        print("Bad connection Returned code=",str(rc))

def on_message(mqttc, obj, msg):
    global dev_id
    print("message received:  " + str(msg.topic))
    topic = str(msg.topic)
    if topic.startswith('/'):
        topic = topic[1:]
    topicTree = topic.split("/")
    topicTreeLevels = len(topicTree)

    owner = topicTree[1]
    print("Updated owner")

    # for level in range(2 , (topicTreeLevels - 1)):
    #     dev_id += topicTree[level]
    dev_id = topicTree[2]
    print("Updated dev_id") 
    deviceDict[dev_id].now = datetime.datetime.now()

    field = topicTree[-1]
    value = msg.payload.decode("utf-8")
    value = float(value)
    value = round(value)
    print("Update field: ", field)
    print("Update value: ", value)
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

def on_subscribe(mqttc,obj,mid,granted_qos):
    print("Subscribed: " + str(mid))

mqttc = paho.Client()
mqttc.username_pw_set(username= mqttClientUser, password=mqttClientPassword)

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect(mqttBroker)

mydb = mysql.connector.connect(
  host="localhost",
  user="robinusr",
  passwd="spanTHEr1v3r",
  database="robindb"
)
mycursor = mydb.cursor()

while (True):
    if (((dev_id == 'aq1') or (dev_id == 'aq2')  or (dev_id =='ajaqi_1')) and (not None in (deviceDict[dev_id].temperature,
     deviceDict[dev_id].pressure, deviceDict[dev_id].humidity, deviceDict[dev_id].pm10, deviceDict[dev_id].pm25))):
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, temperature, pressure, humidity, pm10, pm25) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        vals = (deviceDict[dev_id].now, deviceDict[dev_id].owner, dev_id, deviceDict[dev_id].temperature, deviceDict[dev_id].pressure,
         deviceDict[dev_id].humidity, deviceDict[dev_id].pm10, deviceDict[dev_id].pm25)
        mycursor.execute(sql, vals)
        mydb.commit()
        time.sleep(1)
        print("Inserted an rh/aj record")
        deviceDict[dev_id].temperature = deviceDict[dev_id].humidity = deviceDict[dev_id].pressure = deviceDict[dev_id].pm10 = deviceDict[dev_id].pm25 = deviceDict[dev_id].now = None

    if (dev_id == 'ESP_Easy' and (not None in (deviceDict[dev_id].pm10, deviceDict[dev_id].pm25))):
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, pm10, pm25) VALUES (%s, %s, %s, %s, %s)"
        vals = (deviceDict[dev_id].now, deviceDict[dev_id].owner, dev_id,
         deviceDict[dev_id].pm10, deviceDict[dev_id].pm25)
        mycursor.execute(sql, vals)
        mydb.commit()
        time.sleep(1)
        print("Inserted an ms record")
        deviceDict[dev_id].temperature = deviceDict[dev_id].humidity = deviceDict[dev_id].pressure = deviceDict[dev_id].pm10 = deviceDict[dev_id].pm25 = deviceDict[dev_id].now = None
    mqttc.loop()
# loop forever
