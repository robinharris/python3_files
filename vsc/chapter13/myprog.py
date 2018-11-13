"""
GUI Application from Chapter 13
"""


class Adder(object):
    """
    Implements an adding machine using a Tkinter GUI
    Call the method display to initiate a display
    """


def display(self):
    """
    Display the user interface
    Returns when the interface is closed by the user
    """
    first_numer_label = Label(root, text='First number')
    first_numer_label.grid(sticky=E, padx=5, pady=5, row=0, column=0)

if __name__ == '__main__':
        app = Adder()
        app.display()



from tkinter import *
root = Tk()
