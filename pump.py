import RPi.GPIO as GPIO
import time
import logging
import sys

#set up logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='pump.log', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger("ex")

pumpRunSeconds = 5
pinsDict = {1: 17, 2:27}
GPIO.setmode(GPIO.BCM)
# set two GPIO pins to outputs to switch the two pumps
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
# set both outputs low to ensure pumps are off
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)

try:
    # check if an argument has been provided and if it is 1 or 2
    logging.info(sys.argv)
    if len(sys.argv) == 2:
        pump = int(sys.argv[1])
        #check if pump is either 1 or 2 
        if pump == 1 or pump == 2:
            pin = pinsDict[pump]
            logging.info("Starting pump {}".format(pump))
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(pumpRunSeconds)
            GPIO.output(pin, GPIO.LOW)
            logging.info("Stopped pump {}".format(pump))
            logging.info("GPIO {0} actual status {1}".format(pin, GPIO.input(pin)))
        else:
            print("Argument must be 1 or 2")
        
    else:
        print("Invalid number of arguments supplied")
                  
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
