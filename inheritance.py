class Room:

	def __init__(self, doors, windows):
		self.doors = doors
		self.windows = windows

	def floor(self):
		raise NotImplementedError('Subclass MUST implement abstract method')

class Bedroom(Room):

	def __init__(self, doors, windows):
		super().__init__(doors, windows)

	def floor(self):
		return 'First'


class Bathroom(Room):

	def __init__(self, doors, windows):
		super().__init__(doors, windows)

	def floor(self):
		return 'First'

class LivingArea(Room):

	def __init__(self, doors, windows):
		super().__init__(doors, windows)

	def floor(self):
		return 'Ground'



def main():

	bedroom1 = Bedroom(1,2)
	bedroom2 = Bedroom(1,1)
	lounge = LivingArea(2,2)
	dayroom = LivingArea(2,0)
	diningroom = LivingArea(1,1)

	print('Bedroom1 has:', bedroom1.windows, 'windows')
	print('is Bedroom1 a bedroom? ', isinstance(bedroom1, Bedroom))
	print('Is bedroom1 a room? ', isinstance(bedroom1, Room))
	print('Is bedroom1 a bathroom? ', isinstance(bedroom1, Bathroom))
	print ('Bedroom1 is on the ', bedroom1.floor(), 'floor')



if __name__ == '__main__':
	main()