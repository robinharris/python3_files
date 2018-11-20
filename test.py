print("hello")
import paho.mqtt.client as mqtt
import time
print ("Hello Rob")

#mqtt settings
mqttBroker = "mqtt.connectedhumber.org" 
mqttClientUser = "connectedhumber"
mqttClientPassword = "3fds8gssf6"

mqttc = mqtt.Client()
mqttc.username_pw_set(username = mqttClientUser, password = mqttClientPassword)

def on_connect(client, userdata, flags, rc):
    print("connected OK Returned code=",rc)
    sys.stdout.flush()
    mqttc.subscribe("air/rh/#")

mqttc.on_connect = on_connect

print("Connecting")
mqttc.connect(mqttBroker)
mqttc.loop_start()
time.sleep(300)
mqttc.loop_stop()

print("End")