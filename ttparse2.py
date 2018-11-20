#
# Runs an MQTT client to receive messages from ttn_graph
# Parses the message into JSON
# INSERTS chosen fields into a mySQL database
#
# 17th November 2018
# Robin Harris


import json
import ttn
import time

app_id = "2301195604031956"
access_key = "ttn-account-v2.S6W7llns7NVnp9Yvau66bDE4i4H12DD5OWuYbahron8"

def uplink_callback(msg, client):
    print("Received uplink from: ", msg.dev_id)
    print(msg)

handler = ttn.HandlerClient(app_id, access_key)

# use mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()
# time.sleep(60)

#using application manager client
app_client = handler.application()
my_app = app_client.get()
print(my_app)
my_devices = app_client.devices()
print(my_devices)

