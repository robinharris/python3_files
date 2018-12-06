#------------------------------------------
#--- Author: Robin Harris
#--- Date: 6th December 2018
#--- Version: 1.0
#--- Python Ver: 3.6
#------------------------------------------

import paho.mqtt.client as paho
import datetime
# import mysql.connector
import time
import json

#mqtt settings
mqttBroker = 'mqtt.connectedhumber.org'
mqttClientUser = "connectedhumber"
mqttClientPassword = "3fds8gssf6"

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    if rc==0:
        print("connected OK Returned code=" + str(rc))
        mqttc.subscribe("air/data/", 0)
    else:
        print("Bad connection Returned code=",str(rc))

def on_message(mqttc, obj, msg):
    print("message received:  " + str(msg.topic))
    topic = str(msg.topic)
    now = datetime.datetime.now()
    print(msg.payload)

    payloadJson = json.loads(msg.payload.decode("utf-8"))
    temperature = payloadJson["Temp"]
    print(temperature)

def on_subscribe(mqttc,obj,mid,granted_qos):
    print("Subscribed: " + str(mid))

mqttc = paho.Client()
mqttc.username_pw_set(username= mqttClientUser, password=mqttClientPassword)

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
print("connecting to broker")
mqttc.connect(mqttBroker)

while(True):
    mqttc.loop()
    time.sleep(1)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="robinusr",
#   passwd="spanTHEr1v3r",
#   database="robindb"
# )
# mycursor = mydb.cursor()