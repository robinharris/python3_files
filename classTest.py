import datetime


class testClass:
	"""A class to represent people"""

	def __init__(self,name):
		names_title=[]
		names=name.split(" ")
		map_output = map(lambda word: word.title(), names)
		for item in map_output:
			names_title.append(item)
		number_of_names=len(names_title)
		print ('That name has', number_of_names, 'words')
		for word in range (number_of_names):
			print(names_title[word],)

	def age(dob):
		today = datetime.date.today()
		dob_date = datetime.date(int(dob[4:8]), int(dob[2:4]), int(dob[0:2]))
		age = today-dob_date
		print(type(age.days))
		print('Number of days old: ',age.days)
		print('Number of years old: ', age.days//365 )
		return age.days/65



def main():
	dob=''
	name=input('Enter a full name: ')
	person1 = testClass(name)
	while len(dob) != 8:
		dob = input('Date of birth (ddmmyyyy): ')
	person1.dob = dob
	person1.age = testClass.age(dob)


if __name__ == "__main__":
	main()
