aString = 'Hello Rob'
try:
	print("trying")
	integerString = int(aString)
	print ('First', integerString)
except:
	integerString = -1
	print ("now in except")

aString = '123'
integerString = int(aString)
print ('Second', integerString)