#------------------------------------------
#--- Author: Robin Harris
#--- Date: 3rd April 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#------------------------------------------

import json
import sqlite3
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = "azzura01"
emailAddressFrom = "robin.harris@ayelandsassociates.co.uk"
emailAddressTo = "robin.harris@ayelandsassociates.co.uk"

# SQLite DB Name
DB_Name =  "home.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database

# Function to save data to DB Table
def sensor_Data_Handler(jsonData):
    #Parse Data 
    json_Dict = json.loads(jsonData)
    sensorid = json_Dict['sensor_ID']
    date = (datetime.today()).strftime("%Y%m%d %H:%M:%S") 
    temperature = (json_Dict['Temperature']) / float(100)
    voltage = json_Dict['Voltage'] / float(100)
    print "sensorid: " + sensorid
    print "date: " + date
    print temperature
    print voltage
    #Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into sensordata (sensorid, date, temp, voltage) values (?,?,?,?)",[sensorid, date, temperature, voltage])
    del dbObj
    print "Inserted data into database."
    print ""
    if (sensorid == 'Workshop'):
	if (temperature > 18.0) and (sensor_Data_Handler.email == False):
	    msg = MIMEMultipart()
	    msg['From'] = emailAddressFrom
	    msg['To:'] = emailAddressTo
	    msg['Subject'] = "Alert from Home Temperature Monitor"
	    body = "Workshop Temperature: " + str(temperature) + "C"
	    msg.attach(MIMEText(body, 'plain'))
	    server = smtplib.SMTP('smtp.gmail.com',587)
	    server.starttls()
	    server.login(emailAddressFrom, password)
	    text = msg.as_string()
	    server.sendmail(emailAddressFrom, emailAddressTo, text)
	    server.quit()
	    sensor_Data_Handler.email = True 
	if (temperature < 18.0) and (sensor_Data_Handler.email  ==True):
	    sensor_Data_Handler.email = False

