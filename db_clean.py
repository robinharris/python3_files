"""
Imports sensor data from an SQLITE3 database
Removes and rows where the temperature is out of range
Converts any rows where the date is in the wrong format
"""

import sqlite3
from datetime import datetime

database = 'home_26sep.db'

def removeInvalidTemp():
	try:
		con = sqlite3.connect(database)
		cur = con.cursor()

		#count rows with out of range temperature
		cur.execute('SELECT * from sensordata WHERE temp <-10 OR temp >50')
		data = cur.fetchall()

		print(50*'=')
		print("Number of rows with out of range temperature {}".format(len(data)))

		#Delete rows with out of range temperature
		print('Starting to delete')
		cur.execute('DELETE from sensordata WHERE temp < -10 OR temp > 50')
		
		#run the select again to confirm that out of range temperatures have been deleted
		cur.execute('SELECT * from sensordata WHERE temp < -10 OR temp > 50')
		data = cur.fetchall()
		print('Number of rows with out of range temperatures now {}'.format(len(data)))
		print(50*'=')

		con.commit()

		#now select all rows with a date that does not start with 2017 or later
		cur.execute('SELECT * FROM sensordata WHERE date <"2017"')
		data = cur.fetchall()
		# print('Total number of rows {}'.format(len(cur.fetchall())))
		

		# cur.execute('DELETE FROM sensordata WHERE date < "2017"')
		print('Number of rows with date not starting with 2017 {}'.format(len(data)))
		for row in data:
			print(row)

		data_list=list(data)
		dataToUpdate=[]

		for row in data_list:
			year = row[2][6:10]
			month = row[2][3:5]
			day = row[2][0:2]
			hour = row[2][10:12]
			minute = row[2][14:16]
			second = row[2][17:19]
			newdate = year + month + day + ' ' + hour + ':' + minute + ':' + second
			dataToUpdate.append((row[0], row[1], newdate, row[3]))
			
		#UPDATE all the records with date in the wrong format
		for i in range(len(dataToUpdate)):
			updatestring = ("""
			UPDATE sensordata
				SET date = '{}'
				WHERE id = {}
			;
			""".format(dataToUpdate[i][2], dataToUpdate[i][0]))
			cur.execute(updatestring)
			con.commit()


	except sqlite3.Error as e:
		print("Database error!  Rolling back")
		print(str(e))
		con.rollback()

	finally:
		if con:
			con.close()







def main():
	removeInvalidTemp()




if __name__ == '__main__':
	main()