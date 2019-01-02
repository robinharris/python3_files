/* example use of EEPROM on an Arduino to store an integer
* that survives power down.
* This example uses the simple methods provided by EEPROM.h and
* uses a fixed location in EEPROM for the two bytes.
* Robin Harris
* 26th November 2018
*/

#include <EEPROM.h> // include the required library

// EEPROM locations store a single 8 bit byte
// Locations are addressed by numbers in the range 0 to 1023 
// Each location can be read infinitely but typically will only
// be reliable for 100,000 writes.
// Therefore take care NOT to write to EEPROM on every loop!
// An int variable in Arduino is 16 bits or two bytes and will
// therefore require two EEPROM locations

int eeAddress = 0; // address to store the first byte
// normally bytes are written in sequential locations so the second byte
// will go to eeAddress + 1
// colud be any value between 0 and 1023 (minus one so there is room for
// two bytes together) on an Uno.  Some Arduino boards have different amounts of EEPROM

int valueToStore = 2345; // an example integer to store
int valuePotPin = 0; // an int variable to hold the position of the pot
int valueRetrieved = 0; // an int variable to be loaded from EEPROM
const int potPin = 0; // declare the pin number as a constant (it will not change)

void setup(){
    // no setup needed for EEPROM

    Serial.begin(9600);
    Serial.println("Starting");
    pinMode (potPin, INPUT); // set potPin (A0) to be an input

    // read in the value stored in EEPROM before power down
    // first get the highbyte
    byte highByteRetrieved = EEPROM.read(eeAddress);
    // then get the low byte from the next address
    byte lowByteRetrieved = EEPROM.read(eeAddress + 1);
    // next combine the two bytes into one integer
    // take the high byte and multiply by 256 then add the low byte
    valueRetrieved = (highByteRetrieved * 256) + lowByteRetrieved;
    // print out the value - first time it will be zero then it will be 2345
    Serial.print("valueRetrieved: \t");
    Serial.println(valueRetrieved);                            
}

void loop(){
    // read the current value of the potPin each time round the loop
    valuePotPin = analogRead(potPin); 
    Serial.print("valuePotPin: \t");
    Serial.println(valuePotPin);
    // check if the current value of potPin has changed
    // if there has been a change more than a preset amount go ahead and write the new value to EEPROM
    // first take the absolute value of the difference 
    int difference = abs(valuePotPin - valueToStore);
    // if the difference is greater than, say, 10 (to avoid writing very small fluctuations to EEPROM )
    if (difference > 10){
        Serial.println("difference is greater than 10 so storing new value in EEPROM");
        // first store the high byte part of the int in a variable
        // called highByteToStore (declared as type 'byte')
        byte highByteToStore = highByte(valueToStore);
        // then store the low byte art of the int in a variable
        // called lowByteToStore (declared as type 'byte')
        byte lowByteToStore = lowByte(valueToStore);

        // Write the two bytes to EEPROM
        //first highByteToStore goes into the starting address we declared
        EEPROM.write(eeAddress, highByteToStore);
        
        // then the lowByteToStore goes into the next location
        EEPROM.write(eeAddress + 1, lowByteToStore);
        Serial.println("Written two bytes to EEPROM");
    }
    // just to stop the loop running very fast and printing too many lines to read
    delay(2000); 
}
    




