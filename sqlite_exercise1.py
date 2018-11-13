import sqlite3
database = 'home.db'

def Main():
	try:
		con = sqlite3.connect(database)
		cur = con.cursor()
		cur.execute("""
			SELECT * FROM sensordata WHERE temp >25
			""")

		data = cur.fetchall()

		con.close()

		#convert tuple to list so can use min
		data_list = [list(x) for x in data]
		
		#create a list of just temperatures
		temp_list=[]
		for row in data_list:
			temp_list.append(row[3])

		temp_list.sort()
		print(*temp_list, sep='\n')

	except sqlite3.Error:
		print("Error!  Rolling back")
		con.rollback()

	finally:
		if con:
			con.close()

def delete_rows():
	try:
		con = sqlite3.connect(database)
		cur = con.cursor()
		cur.execute("""
			DELETE FROM sensordata WHERE
			temp  > 50
			""")
		con.commit()

	except sqlite3.Error():
		print('Error deleting! Rolling back')

	finally:
		if con:
			con.close()



	


if __name__ == '__main__':
	Main()

	delete_rows()
