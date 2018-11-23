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

#mqtt settings
mqttBroker = 'mqtt.connectedhumber.org'
mqttClientUser = "connectedhumber"
mqttClientPassword = "3fds8gssf6"

now = owner = dev_id = None
temperature = pressure = humidity = pm10 = pm25 = None

def loadData(dateTime, topic, value):
   pass 

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    if rc==0:
        print("connected OK Returned code=" + str(rc))
        mqttc.subscribe("#", 0)
    else:
        print("Bad connection Returned code=",str(rc))

def on_message(mqttc, obj, msg):
    global now, owner, dev_id
    global temperature, pressure, humidity, pm10, pm25
    print("message received:  " + str(msg.topic))
    topic = str(msg.topic)
    if topic.startswith('/'):
        topic = topic[1:]
    topicTree = topic.split("/")
    topicTreeLevels = len(topicTree)

    now = datetime.datetime.now()
    print("Updated now")

    owner = topicTree[1]
    print("Updated owner")

    # for level in range(2 , (topicTreeLevels - 1)):
    #     dev_id += topicTree[level]
    dev_id = topicTree[2]
    print("Updated dev_id")

    field = topicTree[-1]
    value = msg.payload.decode("utf-8")
    value = float(value)
    value = round(value)
    print("Update field: ", field)
    print("Update value: ", value)
    if field == 'temperature':
        temperature = value
    elif field == 'pressure':
        pressure = value
    elif field == 'humidity':
        humidity = value
    elif field == 'pm10':
        pm10 = value
    elif field == 'pm25':
        pm25 = value
    print(now, owner, dev_id, temperature, pressure, humidity, pm10, pm25)


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
    if (((dev_id == 'aq1') or (dev_id == 'aq2')) and (not None in (temperature, pressure, humidity, pm10, pm25))):
        sql = "INSERT INTO aq_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        vals = (now, owner, dev_id, temperature, pressure, humidity, pm10, pm25)
        mycursor.execute(sql, vals)
        mydb.commit()
        time.sleep(1)
        print("Inserted an rh record")
        temperature = humidity = pressure = pm10 = pm25 = now = None

    if (dev_id == 'ESP_Easy' and (not None in (pm10, pm25))):
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, pm10, pm25) VALUES (%s, %s, %s, %s, %s)"
        vals = (now, owner, dev_id, pm10, pm25)
        mycursor.execute(sql, vals)
        mydb.commit()
        time.sleep(1)
        print("Inserted an ms record")
        temperature = humidity = pressure = pm10 = pm25 = now = None
    mqttc.loop()
# loop forever
