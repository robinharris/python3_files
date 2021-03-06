#------------------------------------------
#--- Author: Robin Harris
#--- Date: 28th December 2018
#--- Version: 3.0 local testing 
#--- Python Ver: 3.6
#
# This version receives MQTT messages from a broker.
# The keys MUST include a "dev" which is the unique device identifer.  Other valid keys:
# "timestamp", "temp", "humidity", "pressure", "PM10", "PM25"
# "timestamp" is used for a device generated date and time
# if it is not present a date and time will be generated by this program
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
dbHost="94.72.215.27"
dbUser="robinusr"
dbPassword="spanTHEr1v3r"
dbName="robindb"

print("Starting to run the local test version of chDataLoadV2.py")

def on_connect(mqttc, obj, flags, rc):
    print("Connected to broker")
    print("rc: " + str(rc))
    if rc==0:
        print("connected OK Returned code=" + str(rc))
        mqttc.subscribe(topicToSubscribe, 0)
    else:
        print("Bad connection Returned code=",str(rc))

def on_message(mqttc, obj, msg):
    # {"dev":"aq2","temp":19.28, "humidity" : 52.02, "pressure" : 1026.79, "PM10" : 3.48, "PM25" : 1.56}
    print(str(msg.payload))
    payloadJson = json.loads(msg.payload.decode("utf-8"))
    dev_id = temperature = pressure = humidity = pm10 = pm25 = dateTimeString = None
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
        # create a Python datetime object from the dateTimeString
        dateTimeObject = datetime.datetime.strptime(dateTimeString, '%a %b %d %Y %H:%M:%S %Z%z')
    else:
        # if the message does not contain a key "timestamp", create a received time now
        dateTimeObject = datetime.datetime.now()
    # dateT is a string in the database format
    dateT = dateTimeObject.strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO aq_data_json (dateTime, dev_id, temperature, pressure, humidity, pm10, pm25) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    vals = (dateT, dev_id, temperature, pressure, humidity, pm10, pm25)
    try:
        # check if the database connection is still open and if not reconnect
        mydb.ping(reconnect=True, attempts=5, delay=1)
        # execute SQL to insert a row
        mycursor.execute(sql, vals)
        # commit the change
        mydb.commit()
    except Exception as e:
        print("Database error")
        print (e)

def on_subscribe(mqttc,obj,mid,granted_qos):
    print("Subscribed: " + str(mid))

mqttc = paho.Client()
mqttc.username_pw_set(username= mqttClientUser, password=mqttClientPassword)

# set MQTT callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe

# connect to the MQTT broker
mqttc.connect(mqttBroker)

# open a database connection
try:
    mydb = mysql.connector.connect(
    host=dbHost,
    user=dbUser,
    passwd=dbPassword,
    database=dbName
    )
    mycursor = mydb.cursor()
    print("Opened a database connetion")
except Exception as e:
    print("Error connecting to the database")
    print(e)

# Start the MQTT loop that runs forever and is blocking.
mqttc.loop_forever()

