import mysql.connector
import paho.mqtt.client as mqtt

mqttClient = mqtt.Client("robin")
broker = "172.26.6.1"
mqttUser = "connectedhumber"
mqttPassword = "3fds8gssf6"

def on_message(client, userdata, message):
    rcvdMessage = str(message.payload.decode("utf-8"))
    print("client", client)
    print("Received message: ", rcvdMessage)
    print("user data: ", userdata)
    dateTime, count = rcvdMessage.split(',')
    print("dateTime: ", dateTime)
    print("count: ", count)
    mycursor = mydb.cursor()
    sql = "INSERT INTO peopleCounter (dateTime, count) VALUES (%s, %s)"
    vals =(dateTime ,count)
    mycursor.execute(sql, vals )
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def on_subscribe(client, object, mid, granted_qos):
    print("Subscribed")

def on_connect(client, object, flags, rc):
    print("Connected to mqtt broker")
    mqttClient.subscribe("pir")

# set callbacks
mqttClient.on_message=on_message
mqttClient.on_subscribe=on_subscribe
mqttClient.on_connect=on_connect

mqttClient.username_pw_set(username=mqttUser, password=mqttPassword)
mqttClient.connect(broker)

mydb = mysql.connector.connect(
  host="localhost",
  user="robinusr",
  passwd="spanTHEr1v3r",
  database="robindb"
)
mqttClient.loop_forever()
