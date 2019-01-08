#------------------------------------------
#--- Author: Robin Harris
#--- Date: 1st January 2019
#--- Version: 1.0
#--- Python Ver: 3.6
#
# This version receives MQTT messages from a broker.
# The keys MUST include a "dev" which is the unique device identifer.  Other valid keys:
# "timestamp", "temp", "humidity", "pressure", "PM10", "PM25"
# "timestamp" is used for a device generated date and time
# if it is not present a date and time will be generated by this program
#
# Incoming data is stored to a MariaDb database on Soekris
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
dbHost="192.168.0.136"
dbUser="robinusr"
dbPassword="spanTHEr1v3r"
dbName="aq_db"

print("Starting to run chDataLoad_JSON.py")

def dbUpdate(sql, vals):
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

def on_connect(mqttc, obj, flags, rc):
    print("Connected to broker")
    print("rc: " + str(rc))
    if rc==0:
        print("connected OK Returned code=" + str(rc))
        mqttc.subscribe(topicToSubscribe, 0)
    else:
        print("Bad connection Returned code=",str(rc))

def on_message(mqttc, obj, msg):
    payloadJson = json.loads(msg.payload.decode("utf-8"))
    # set all variables to None
    device_id = device_name = temperature = pressure = humidity = pm10 = pm25 = dateTimeString = None
    recordedOnString = recordedOnObject = None
    receivedOnString = receivedOnObject = None
    readings_id = None

    # first get the device_id from the device_name by looking it up in the database
    try:
        device_name = payloadJson['dev']
        # SQL SELECT to find device_id
        sql = "SELECT device_id FROM devices WHERE device_name = %s"
        vals = (device_name,)
        try:
            # check if the database connection is still open and if not reconnect
            mydb.ping(reconnect=True, attempts=5, delay=1)
            # execute SQL to insert a row
            mycursor.execute(sql, vals)
            device_id = mycursor.fetchone()[0]
        except Exception as e:
            print("Database error - unable to provide required data")
            print (e)
    except Exception:
        print("no device_name provided")
        print("device_name is: {}   device_id is: {}".format(device_name, device_id))

    # Next decode the incoming message and set up the variables to be inserted
    # construct a dictionary of parameters and values
    parameters = {}
    if 'temp' in payloadJson:
        print(payloadJson)
        parameters["temperature"] = payloadJson['temp']
    if 'humidity' in payloadJson:
        parameters["humidity"] = payloadJson['humidity']
    if 'pressure' in payloadJson:
        parameters["pressure"] = payloadJson['pressure']
    if 'PM10' in payloadJson:
        parameters["PM10"] = payloadJson['PM10']
    if 'PM25' in payloadJson:
        parameters["PM25"] = payloadJson['PM25']
    if 'timestamp' in payloadJson:
        dateTimeString = payloadJson['timestamp']
        # create a Python datetime object from the dateTimeString
        recordedOnObject = datetime.datetime.strptime(dateTimeString, '%a %b %d %Y %H:%M:%S %Z%z')
        # recordedONString is a string in the required database format
        recordedOnString = recordedOnObject.strftime('%Y-%m-%d %H:%M:%S')
        print(recordedOnString)

    # now update readings table with a timestamp supplied by the device, device_id and raw JSON
    sql = "INSERT INTO readings (recordedon, device_id, raw_json) VALUES (%s, %s, %s)"
    vals = (recordedOnString, device_id, str(payloadJson))
    dbUpdate(sql, vals)
    
    # get the readings_id for the reading just inserted
    mycursor.execute("SELECT id FROM readings ORDER BY id DESC LIMIT 1")
    readings_id = mycursor.fetchone()[0]
    print(readings_id)

    # next insert each parameter's reading into reading_values
    sql = "INSERT INTO reading_values (reading_id, value, reading_value_types_id) VALUES (%s, %s, %s)"
    for key, value in parameters.items():
        vals = (readings_id, value, key)
        dbUpdate(sql, vals)


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
    print("Opened a database connection")
except Exception as e:
    print("Error connecting to the database")
    print(e)

# Start the MQTT loop that runs forever and is blocking.
mqttc.loop_forever()

