import datetime

currentTime = datetime.datetime.now()
testTime = datetime.datetime(2017,9,7)

print ("Current time is: {}".format(currentTime))

for i in range(30):
    futureTime = currentTime + datetime.timedelta(days=i)

    print(f"Future time is: {futureTime}")
        
    if futureTime < testTime:

        print("Waiting for the time to pass")

    else:
        print ("Passed the test date")


