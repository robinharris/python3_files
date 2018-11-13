import json
import sqlite3
from numpy import arange
import matplotlib.pyplot as plt
from matplotlib.dates import drange, DayLocator, HourLocator, DateFormatter
import datetime

time_format = '%Y-%m-%dT%H:%M:%S'
DATABASE = 'ttn.db'
number_of_points = 600


def get_data():
    """
    retrieves all rows from the database
    """

    try:
        con = sqlite3.connect(DATABASE)
        cursor = con.cursor()

        # execute the SQL command
        cursor.execute('SELECT * FROM ttn_data')
        data = cursor.fetchall()

        print("Number of rows retrieved: " + str(len(data)))

        return data

    except sqlite3.Error:
        print("Error extractng data, rollng back")
        con.rollback()

    finally:
        if con:
            con.close()


def create_X_and_Y(data):
    '''
    argument is a list of lists with each inner list being a row from ttn.db. The sensor data
    is mixed as it is in the db.
    Creates an x and y axis for rfm95-1 and rfm95-2 from this data.  x is a datetime object and
    y is temperature as a float.
    '''
    xaxis_1 = []
    yaxis_1 = []
    xaxis_2 = []
    yaxis_2 = []
    for row in data:
        if row[1]== 'rfm95-1':
            yaxis_1.append(row[3])
            xaxis_1.append(datetime.datetime.strptime(row[4][0:19], time_format))
        elif row[1] =='rfm95-2':
            yaxis_2.append(row[3])
            xaxis_2.append(datetime.datetime.strptime(row[4][0:19], time_format))
    return (xaxis_1, yaxis_1, xaxis_2, yaxis_2)


def main():
    data = get_data()
    # create axes for both sensors
    xaxis_1, yaxis_1, xaxis_2, yaxis_2 = create_X_and_Y(data)

    xaxis_1_plot = xaxis_1[-number_of_points:]
    yaxis_1_plot = yaxis_1[-number_of_points:]

    fig, ax = plt.subplots()
    ax.plot_date(xaxis_1_plot, yaxis_1_plot, fmt='b-')
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y %m %d'))
    ax.xaxis.set_minor_locator(HourLocator(arange(0,25,4)))
    ax.fmt_xdata = DateFormatter('%H:%M:%S')
    fig.autofmt_xdate()
    plt.title("RFM95-1 Temperature")
    plt.ylabel("Celsius")
    plt.show()

    # plt.plot_date(x=xaxis_1, y=yaxis_1)
    # plt.show()


if __name__ == '__main__':
    main()
