#------------------------------------------
#--- Author: Robin Harris
#--- Date: 8th December 2018
#--- Version: 2.0
#--- Python Ver: 3.6
#
# This version receives MQTT messages from a broker - the message must contain a JSON dateTimeString
# The keys MUST include a "dev" which is the unique device identifer.  Other valid keys:
# "timestamp", "temp", "humidity", "pressure", "PM10", "PM25"
#
#------------------------------------------

import paho.mqtt.client as paho
import datetime
import mysql.connector
import time
import json

# MQTT settings
mqttBroker = 'mqtt.connectedhumber.org'
mqttClientUser = "connectedhumber"
mqttClientPassword = "3fds8gssf6"
topicToSubscribe = "airquality/data"

# database settings
dbHost="localhost"
dbUser="robinusr"
dbPassword="spanTHEr1v3r"
dbName="robindb"

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    if rc==0:
        print("connected OK Returned code=" + str(rc))
        mqttc.subscribe(topicToSubscribe, 0)
    else:
        print("Bad connection Returned code=",str(rc))

def on_message(mqttc, obj, msg):
    # print("message received:  " + str(msg.topic))
    print(str(msg.payload))
    payloadJson = json.loads(msg.payload.decode("utf-8"))
    dev_id = temperature = pressure = humidity = pm10 = pm25 = timestamp = None
    if 'dev' in payloadJson:
        dev_id = payloadJson['dev']
    if 'temp' in payloadJson:
        temperature = payloadJson['temp']
    if 'humidity' in payloadJson:
        humidity = payloadJson['humidity']
    if 'pressure' in payloadJson:
        pressure = payloadJson['pressure']
    if 'PM10' in payloadJson:
        pm10 = payloadJson['PM10']
    if 'PM25' in payloadJson:
        pm25 = payloadJson['PM25']
    if 'timestamp' in payloadJson:
        dateTimeString = payloadJson['timestamp']
    print("Device: " + dev_id) 
    print("PM25: " + str(pm25))
    print("Time: " + dateTimeString)
    dateTimeObject = datetime.datetime.strptime(dateTimeString, '%a %b %d %Y %H:%M:%S %Z%z')
    # print("dateTimeObject: " + dateTimeObject)
    dateTime = dateTimeObject.strftime('%Y-%m-%d %H:%M:%S')
    print(dateTime)
    sql = "INSERT INTO aq_data_json (dateTime, dev_id, temperature, pressure, humidity, pm10, pm25) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    vals = (dateTime, dev_id, temperature, pressure, humidity, pm10, pm25)
    print(vals)
    try:
        # check if the database connection is still open and if not reconnect
        mydb.ping(reconnect=True, attempts=5, delay=1)
        # execute SQL to insert a row
        mycursor.execute(sql, vals)
        # commit the change
        mydb.commit()
        # time.sleep(1)
    except Exception as e:
        print("Database error")
        print (e)

def on_subscribe(mqttc,obj,mid,granted_qos):
    print("Subscribed: " + str(mid))

mqttc = paho.Client()
mqttc.username_pw_set(username= mqttClientUser, password=mqttClientPassword)

# set MQTT callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# connect to the MQTT broker
try:
    mqttc.connect(mqttBroker)
except Exception as e:
    print("Error connecting to the broker")
    print(e)

# open a database connection
try:
    mydb = mysql.connector.connect(
    host=dbHost,
    user=dbUser,
    passwd=dbPassword,
    database=dbName
    )
    mycursor = mydb.cursor()
except Exception as e:
    print("Error connecting to the database")
    print(e)

# Start the MQTT loop that runs forever and is blocking.
mqttc.loop_forever()
