#------------------------------------------
#--- Author: Robin Harris
#--- Date: 28th November 2018
#--- Version: 1.0
#--- Python Ver: 3.6
#------------------------------------------

import paho.mqtt.client as paho
import datetime
import mysql.connector
import time
import json

#mqtt settings
mqttBroker = 'eu.thethings.network' # the internal IP address so we don't use chargeable bandwidth
mqttClientUser = "2301195604031956"
mqttClientPassword = "ttn-account-v2.S6W7llns7NVnp9Yvau66bDE4i4H12DD5OWuYbahron8"

def lineRead():
    fileToOpen = "aq3_ttn_2.txt"
    file = open(fileToOpen, 'r')
    for line in file:
        stringReceived= file.readline()
        processTTNMessage(stringReceived)

def processTTNMessage(ttnMessage):
    try:
        # jsonTTNMessage = json.loads(msg.payload.decode('utf-8'))
        jsonTTNMessage = json.loads(ttnMessage)
        device = jsonTTNMessage["dev_id"]
        payload_fields = jsonTTNMessage["payload_fields"]
        datetime = jsonTTNMessage["metadata"]["time"]
        datetime = datetime.replace('T', ' ') # replace T in the string with space
        datetime = datetime.replace('Z', '') # remove the training Z in the string
        gateways = jsonTTNMessage["metadata"]["gateways"]
        # print for every gateway that has received the message and extract RSSI
        for gw in gateways:
            gateway_id = gw["gtw_id"]
            rssi = gw["rssi"]
            # print(datetime + ", " + device + ", " +  ", "+ gateway_id + ", "+ str(rssi) + ", " + str(payload_fields))
        sql = "INSERT INTO aq_data_ttn (dateTime, dev_id, pm10, pm25, voc, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        vals = (datetime, device, payload_fields['pm10'], payload_fields['pm25'], payload_fields['volatiles'], payload_fields['latitude'], payload_fields['longitude'])
        mycursor.execute(sql, vals)
        # commit the change
        mydb.commit()
        # seems to need time to complete the commit 
        # time.sleep(1)
    except Exception as e:
        print(e)
        pass

    # jsonTTNMessage = json.loads(ttnMessage) # convert string to JSON
    # numberOfGateways = len(jsonTTNMessage["metadata"]["gateways"])
    # values = [jsonTTNMessage["metadata"]["time"],
    #  jsonTTNMessage["dev_id"],
    #  jsonTTNMessage["payload_fields"]["latitude"],
    #  jsonTTNMessage["payload_fields"]["longitude"],
    #  jsonTTNMessage["payload_fields"]["volatiles"],
    #  jsonTTNMessage["payload_fields"]["pm10"],
    #  jsonTTNMessage["payload_fields"]["pm25"]]
    # for gateway in range(0, numberOfGateways):
    #         gw_id = jsonTTNMessage["metadata"]["gateways"][gateway]["gtw_id"]
    #         gw_rssi = jsonTTNMessage["metadata"]["gateways"][gateway]["rssi"]
    #         values.append(gw_id)
    #         values.append(gw_rssi)
    # return values

def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        mqttc.subscribe("+/devices/+/up")

def on_message(mqttc, obj, msg):
    try:
        jsonTTNMessage = json.loads(msg.payload.decode('utf-8'))
        device = jsonTTNMessage["dev_id"]
        payload_fields = jsonTTNMessage["payload_fields"]
        datetime = jsonTTNMessage["metadata"]["time"]
        datetime = datetime.replace('T', ' ') # replace T in the string with space
        datetime = datetime.replace('Z', '') # remove the training Z in the string
        gateways = jsonTTNMessage["metadata"]["gateways"]
        dev_id = jsonTTNMessage
        # print for every gateway that has received the message and extract RSSI
        for gw in gateways:
            gateway_id = gw["gtw_id"]
            rssi = gw["rssi"]
            print(datetime + ", " + device + ", " + gateway_id + ", "+ str(rssi) + ", " + str(payload_fields))
        sql = "INSERT INTO aq_data_ttn (dateTime, dev_id, pm10, pm25, voc, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        vals = (datetime, device, payload_fields["pm10"], payload_fields["pm25"], payload_fields["volatiles"], payload_fields["latitude"], payload_fields["longitude"])
        mycursor.execute(sql, vals)
        # commit the change
        mydb.commit()
        # seems to need time to complete the commit 
        time.sleep(1)
    except Exception as e:
        print(e)
        pass

# set up a paho mqtt instance
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

# lineRead()

mqttc.loop_forever()