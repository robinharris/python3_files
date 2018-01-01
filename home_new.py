import sqlite3

database = 'home.db'


def get_all_data():
	"""retrieves all rthe rows from the database name given"""
	try:
		con = sqlite3.connect(database)
		cur = con.cursor()

		#select all the rows in the database
		cur.execute('SELECT * from sensordata')
		data = cur.fetchall()

		print(len(data))
		return data

	except sqlite3.Error:
		print('Error extracting data, rolling back')
		con.rollback()

	finally:
		if con:
			con.close()

def check_data(data):
	"""Checks the rows for tempemperature that is out of range
	or date in wrong format. Bad rows are put into a list for 
	deletion
	"""

	good_row = []
	bad_row = []
	for row in data:
		#add rows that have a valid temperature to one list
		if (row[3] < 50) and (row[3] > -10) and (len(row[2]) == 17) :
			good_row.append(row)
		#and add any out of range temperatures to another list
		else: bad_row.append(row)

	print('Total rows: ', len(good_row) + len(bad_row))
	print('Number of good rows: ',len(good_row))
	print('Number of bad rows: ',len(bad_row))

	return bad_row

def remove_bad_rows(bad_row):
	""" removes rows of data from the database
	where the temperature is out of range
	or the date is not in the correct format
	"""
	try:
		con = sqlite3.connect(database)
		cur = con.cursor()

		#delete all the bad rows
		for row in bad_row:
			selectstring = 'DELETE from sensordata WHERE id = ' + str(row[0])
			cur.execute(selectstring)
			con.commit()

	except sqlite3.Error as e:
		print("Error deleting rows, rolling back")
		print(e)

	finally:
		if con:
			con.close()


def main():
	#get all the data
	data = get_all_data()

	#check for number of good rows and bad rows.  Return bad rows
	bad_row = check_data(data)

	if len(bad_row) < 1:
		print("No bad rows to remove")
		return

	#remove bad rows
	delete = input('Delete bad rows? Y/n: ')

	if (delete == 'y' or delete == 'Y'):
		remove_bad_rows(bad_row)


if __name__ == '__main__':
	main()
