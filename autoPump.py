import RPi.GPIO as GPIO
import time
import logging
import sys
from datetime import timedelta, date

#set up logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='autoPump.log', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger("ex")

# set up variables
pumpRunSeconds = 5
startDate = datetime(2017,9,12)
# initialise previousDate to currentDate
previousDate = datetime.now()


# set up GPIO to use BCM pins 17 and 27 for the pumps
pinsDict = {1: 17, 2:27}
GPIO.setmode(GPIO.BCM)
# set two GPIO pins to outputs to switch the two pumps
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
# set both outputs low to ensure pumps are off
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)


try:
    while True:
        currentDate = datetime.now()
        print (currentDate)
        if currentDate > previousDate.timedelta(day=1):
            for pump in range(1,3):
                logging.info("Starting pump {}".format(pump))
                GPIO.output(pinsDict(pump), GPIO.HIGH)
                time.sleep(pumpRunSeconds)
                GPIO.output(pinsDict(pump), GPIO.LOW)
                logging.info("Stopped pump {}".format(pump))
                logging.info("GPIO {0} actual status {1}".format(pin, GPIO.input(pin)))
            previousDate = currentDate
        time.sleep(60)
                      
except KeyboardInterrupt:
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    print("Interrupted - stopping")
    logging.warning("GPIO 17 actual status {}".format(GPIO.input(17)))
    logging.warning("GPIO 27 actual status {}".format(GPIO.input(27)))

except:
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    logging.exception("An error occured")
    logging.warning("GPIO 17 actual status {}".format(GPIO.input(17)))
    logging.warning("GPIO 27 actual status {}".format(GPIO.input(27)))
    
finally:
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.cleanup()
    print("All done and cleaned up")
    logging.info("All done and cleaned up")
