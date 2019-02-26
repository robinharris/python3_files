import requests
import json
from datetime import datetime
import csv
import paho.mqtt.client as paho
import time

print("starting https1")

# MQTT settings
mqttBroker = 'mqtt.connectedhumber.org'
mqttClientUser = "connectedhumber"
mqttClientPassword = "3fds8gssf6"
mqttTopic = "airquality/data"

def on_connect(mqttc, obj, flags, rc):
    print("Connected to broker")
    mqttc.subscribe(mqttTopic)

def on_message(mqttc, obj, msg):
    print("got a message")
    print(str(msg.payload))

def on_subscribe(mqttc,obj,mid,granted_qos):
    print("Subscribed: " + str(mid))

req = requests.get('https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries/266/getData?timespan=P1D/2019-02-26')
print("HTTP Status Code: " + str(req.status_code))
print(40 * '=', "\n\n")
print(req.headers)
print(40 * '=', "\n\n")
json_response = json.loads(req.content)

#     row = str(datetime.fromtimestamp(item['timestamp']/1000)), str(item['value'])
#     print(row)

for item in json_response['values']:
    t = datetime.fromtimestamp(item['timestamp']/1000)
    PM25 = item['value']
    recordedOnString = t.strftime('%Y-%m-%d %H:%M:%S')
    sendBuffer =  "{{\"dev\": \"FT\", \"PM25\": {}, \"timestamp\": {}}}".format(PM25, recordedOnString )
    print(sendBuffer)

mqttc = paho.Client()  # uses a random client id
mqttc.username_pw_set(username=mqttClientUser, password=mqttClientPassword)
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
print("starting broker")
mqttc.connect(mqttBroker)
mqttc.loop_start()
# message = "{\"timestamp\" : \"Mon Feb 25 2019 20:55:38 GMT+0000\",\"dev\":\"test\",\"temp\":10.86,\"PM10\" : 79.00, \"PM25\" : 57.00}"
# while True:
#     print("looping")
#     time.sleep(5)

# with open('freetown1.csv','w', newline='') as csvfile:
#     rowwriter = csv.writer(csvfile, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         rowwriter.writerow(row)
# while True:
#     time.sleep(0.5)
#     print("loop")
#     # mqttc.loop

