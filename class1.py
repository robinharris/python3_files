print("Starting")

class Bike:

	numberOfBikes = 0

	@classmethod
	def printBike(cls):
		print("In this database there are: ", cls.numberOfBikes)

	def __init__(self,id,type):
		self.id = id
		self.type = type
		Bike.numberOfBikes += 1

	def gears(self):
		self.chainring = int(input("Chainring: "))
		print("Chainring size = " + str(self.chainring))
		self.sprocket = int(input("Sprocket:"))
		print("Sprocket size = " + str(self.sprocket))
		

	def showGears(self):
		print ("Chainring = " + str(self.chainring) + "\t" + "Sprocket = " +str(self.sprocket))

	def gearRatio(self):
		return self.chainring / self.sprocket

print("Number of bikes: ", str(Bike.numberOfBikes))
first = Bike("race", "road")
print("Number of bikes: ", str(Bike.numberOfBikes))
second = Bike("mtb", "downhill")
print("Number of bikes: ", str(Bike.numberOfBikes))

first.gears()

first.showGears()
print ("Gear ratio: {:2.2f}".format(first.gearRatio()))
Bike.printBike()



print("Finished")
# print(first.id,first.type, first.gears(2, 3))
# print(second.id,second.type, second.gears(2, 3))
