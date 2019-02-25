import paho.mqtt.client as paho
import datetime
import mysql.connector
import time
import json


mqttc = paho.Client()
broker = "127.0.0.1"
topicToSubscribe = "airquality/data"

# database settings
dbHost="127.0.0.1"
dbUser="robinusr"
dbPassword="spanTHEr1v3r"
dbName="robindb"
print("Starting to run chaqTesLoad.py")

def on_message(mqttc, obj, msg):
    # {"dev":"aq2","temp":19.28, "humidity" : 52.02, "pressure" : 1026.79, "PM10" : 3.48, "PM25" : 1.56}
    payloadJson = json.loads(msg.payload.decode("utf-8"))
    device_name = temperature = pressure = humidity = pm10 = pm25 = dateTimeString = None
    recordedOnString = recordedOnObject = None
    receivedOnString = receivedOnObject = None
    device_name = payloadJson['dev']
    print(device_name)
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
        recordedOnObject = datetime.datetime.strptime(dateTimeString, '%a %b %d %Y %H:%M:%S %Z%z')
      # recordedONString is a string in the required database format
        recordedOnString = recordedOnObject.strftime('%Y-%m-%d %H:%M:%S')
        print(recordedOnString)
    sql = "INSERT INTO testData (dateTime, dev_id, temperature, pressure, humidity, pm10, pm25) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    vals = (recordedOnString, device_name, temperature, pressure, humidity, pm10, pm25)
    print(vals)
    try:
        # check if the database connection is still open and if not reconnect
        mydb.ping(reconnect=True, attempts=5, delay=1)
        # execute SQL to insert a row
        mycursor.execute(sql, vals)
        # commit the change
        mydb.commit()
        print("Added a row")
    except Exception as e:
        print("Database error")
        print (e)

def on_subscribe(mqttc, object, mid, granted_qos):
    print("Subscribed")

def on_connect(mqttc, object, flags, rc):
    print("Connected to mqtt broker")
    mqttc.subscribe(topicToSubscribe, 0)


# set callbacks
mqttc.on_message=on_message
mqttc.on_subscribe=on_subscribe
mqttc.on_connect=on_connect

mqttc.connect(broker)

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

