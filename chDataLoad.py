#------------------------------------------
#--- Author: Robin Harris
#--- Date: 21st November 2018
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
    mydb = mysql.connector.connect(
        host="localhost",
        # host="db.connectedhumber.org",
        user="robinusr",
        passwd="spanTHEr1v3r",
        database="robindb"
    )
    mycursor = mydb.cursor()
    temperature = humidity = pressure = pm10 = pm25 = 0
    dev_id = ""
    topic = ""
    now = datetime.datetime.now()
    topic = str(msg.topic)
    if topic.startswith('/'):
        topic = topic[1:]
    topicTree = topic.split("/")
    topicTreeLevels = len(topicTree)
    owner = topicTree[1]
    for level in range(2 , (topicTreeLevels - 1)):
        dev_id += topicTree[level]
    value = msg.payload.decode("utf-8")
    value = float(value)
    value = round(value)
    if 'temperature' in topic:
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, temperature) VALUES (%s, %s, %s, %s)"
    elif 'humidity' in topic:
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, humidity) VALUES (%s, %s, %s, %s)"
    elif 'pressure' in topic:
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, pressure) VALUES (%s, %s, %s, %s)"
    elif 'pm25' in topic:
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, pm25) VALUES (%s, %s, %s, %s)"
    elif 'pm10' in topic:
        sql = "INSERT INTO aq_data (dateTime, owner, dev_id, pm10) VALUES (%s, %s, %s, %s)"
    
    vals = (now, owner, dev_id, value)
    mycursor.execute(sql, vals)
    mydb.commit()
    time.sleep(1)

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

mqttc.loop_forever()
