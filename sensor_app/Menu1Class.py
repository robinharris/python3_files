'''
Handles the top level menu
'''
import os
class Menu1:
    '''
    Displays a top level menu and accepts user choice.
    Validates input and initiates chosen action
    '''
    def __init__(self):
        self.choice = None

    def displayMenu1(self):
        while True:
            try:
                print('''
                Menu 1

                1) Edit a device
                2) Add session details
                3) Run reports on all devices
                4) Create a device
                5) Save devices to file
                6) Delete a session
                7) Exit
                
                ''')
                self.choice = int(input("Enter an option:  "))
                if self.choice not in [1,2,3,4,5,6,7]:
                    print("{0} is not in range".format(self.choice))
                else:
                    return
            except:
                os.system('clear')
                self.choice = None
                print("{0} is not a valid option".format(self.choice))
                print("Try again!  ")
        


        
                