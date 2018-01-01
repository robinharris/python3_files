import sqlite3
database = 'home_26sep.db'
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
# style.use('fivethirtyeight')

class roomSensor():
	"""An object that reperesents a room"""
	def __init__(self, id):
		self.id = id

	#holds the daily stats for all days
	dailystats=[()]

	def getdailydata(self, data):
		self.data = data

		numberofrows = len(data)
		#set the first date to match
		daytomatch = data[0][2][0:8]
		lastdate = data[numberofrows-1][2][0:8]

		#used to calculate the daily min, max and average.
		#overwritten by next day so not persistent
		daydata = []

		dailystats = []

		#used to confirm all rows have been processed
		cumulativerowsadded = 0

		for row in range(0, numberofrows):
			if row == numberofrows-1:
				daydata.append(data[row])
				cumulativerowsadded += 1
				listoftemps=[]
				totaloftemps=0
				for day in daydata:
					totaloftemps += day[3]
					listoftemps.append(day[3])
				averagetemp = totaloftemps / len(daydata)
				# print('{}  {}  Min  {:4.1f}  Max  {:4.1f}  Ave  {:5.2f}'.format(self.id, daytomatch, min(listoftemps), max(listoftemps), averagetemp))
				print('Cumulative rows added for {} : {}'.format(self.id, cumulativerowsadded))
				# self.printdailystats(dailystats)

			elif data[row][2][0:8] == daytomatch:
				daydata.append(data[row])
				cumulativerowsadded += 1
			
			else:
				#holds temperatures for one day - needed to get min and max
				listoftemps=[]
				#holds a daily total of temperatures - needed to calculate average
				totaloftemps=0

				for day in daydata:
					totaloftemps += day[3]
					listoftemps.append(day[3])
				averagetemp = totaloftemps / len(daydata)

				#now store the daily data as a tuple
				dailystats.append((daytomatch, min(listoftemps), max(listoftemps), averagetemp))

				# print('{}  {}  Min  {:4.1f}  Max  {:4.1f}  Ave  {:5.2f}'.format(self.id, daytomatch, min(listoftemps), max(listoftemps), averagetemp))
				daytomatch = data[row][2][0:8]
				daydata=[]
				daydata.append(data[row])
				cumulativerowsadded += 1
		return dailystats

def graph(room, datatograph):
	"""
	takes a list of lists - each list contains a date and a daily stats
	"""
	dates = []
	values = []

	for i in range (len(datatograph)):
		date_tmp = datatograph[i][0]
		year_tmp = int(date_tmp[0:4])
		month_tmp = int(date_tmp[4:6])
		day_tmp = int(date_tmp[6:8])
		date_daytime = datetime.date(year_tmp, month_tmp, day_tmp)
		dates.append(date_daytime)
		values.append(datatograph[i][3])

	# plt.figure()
	# plt.subplot(221)
	plt.ylim(min(values) - 2, max(values) + 2)
	plt.yticks(np.arange(int(min(values)-2), max(values)+2, 2))
	plt.plot_date(dates, values, '-', label = room, color = 'green', linewidth = 0.5)
	plt.title(room, color = 'green', weight = 'bold', fontsize = 16)
	plt.ylabel('Temperature')
	plt.show()

def main():

	"""
	First create a set of objects using 'roomlist'.  The objects are held
	in 'roomobjects'
	"""
	roomlist = ('Outside','Conservatory','Workshop','Bedroom','Lounge')
	roomobjects =[]
	for room in roomlist:
		roomobjects.append(roomSensor(room))


	"""
	For each roomobject first get the data from SQLITE3
	Then within each room call the roomSensor method 'getdailydata'
	to parse the raw data into daily stats
	"""
	for room in roomobjects:
		try:
			con = sqlite3.connect(database)
			cur = con.cursor()

			selectstring = "SELECT * FROM sensordata WHERE sensorid = '{}'".format(room.id)
			cur.execute(selectstring)
			#room.data (specific for each instance) holds the raw data
			room.data = cur.fetchall()
			print("Total number of rows retrieved for {} {}".format(room.id, len(room.data)))

			#Call getdailydata to calculate daily stats
			room.dailystats = room.getdailydata(room.data)

		except sqlite3.Error as e:
			print('Database error!  Rolling back')
			print(str(e))
			con.rollback()

		finally:
			if con:
				con.close()


	"""
	Now ask user if any summary data is required and if so which room
	"""
	# while True:
	# 	if (input("Print any room summary? ")) == 'n':
	# 		break
	# 	roomtoprint = int(input("Enter room (1 - 5): ")) - 1
	# 	for row in roomobjects[roomtoprint].dailystats:
	# 		print('{}  {}  Min  {:4.1f}  Max  {:4.1f}  Ave  {:5.2f}'.format(roomobjects[roomtoprint].id, row[0], row[1], row[2], row[3]))
	
	for i in range(5):
		graph(roomobjects[i].id, roomobjects[i].dailystats)

if __name__ == '__main__':
	main()