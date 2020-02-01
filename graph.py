#!/usr/bin/python3

import csv
# import plotly.graph_objects as go
import plotly.express as px
import plotly
import time
import numpy as np
import sklearn.datasets
import os
import sys

TIME  = 1
XGYRO = 2
ZACCL = 3
YGYRO = 4
ZGYRO = 5
XACCL = 6
XMAG  = 7
YMAG  = 8
ZMAG  = 9
YACCL = 10
TEAM  = 11
ACTIVITY   = 12
FILE_INDEX = 13

def build_dataDict():
    res = {
        "driving-0-xmag": [],
        "driving-0-ymag": [],
        "driving-0-zmag": [],
        "driving-0-tmag": [],
        "standing-0-xmag": [],
        "standing-0-ymag": [],
        "standing-0-zmag": [],
        "standing-0-tmag": [],
        "walking-0-xmag": [],
        "walking-0-ymag": [],
        "walking-0-zmag": [],
        "walking-0-tmag": [],
        "jumping-0-xmag": [],
        "jumping-0-ymag": [],
        "jumping-0-zmag": [],
        "jumping-0-tmag": [],
        "driving-1-xmag": [],
        "driving-1-ymag": [],
        "driving-1-zmag": [],
        "driving-1-tmag": [],
        "standing-1-xmag": [],
        "standing-1-ymag": [],
        "standing-1-zmag": [],
        "standing-1-tmag": [],
        "walking-1-xmag": [],
        "walking-1-ymag": [],
        "walking-1-zmag": [],
        "walking-1-tmag": [],
        "jumping-1-xmag": [],
        "jumping-1-ymag": [],
        "jumping-1-zmag": [],
        "jumping-1-tmag": [],

        "driving-0-xaccl": [],
        "driving-0-yaccl": [],
        "driving-0-zaccl": [],
        "driving-0-taccl": [],
        "standing-0-xaccl": [],
        "standing-0-yaccl": [],
        "standing-0-zaccl": [],
        "standing-0-taccl": [],
        "walking-0-xaccl": [],
        "walking-0-yaccl": [],
        "walking-0-zaccl": [],
        "walking-0-taccl": [],
        "jumping-0-xaccl": [],
        "jumping-0-yaccl": [],
        "jumping-0-zaccl": [],
        "jumping-0-taccl": [],
        "driving-1-xaccl": [],
        "driving-1-yaccl": [],
        "driving-1-zaccl": [],
        "driving-1-taccl": [],
        "standing-1-xaccl": [],
        "standing-1-yaccl": [],
        "standing-1-zaccl": [],
        "standing-1-taccl": [],
        "walking-1-xaccl": [],
        "walking-1-yaccl": [],
        "walking-1-zaccl": [],
        "walking-1-taccl": [],
        "jumping-1-xaccl": [],
        "jumping-1-yaccl": [],
        "jumping-1-zaccl": [],
        "jumping-1-taccl": [],

        "driving-0-xgyro": [],
        "driving-0-ygyro": [],
        "driving-0-zgyro": [],
        "driving-0-tgyro": [],
        "standing-0-xgyro": [],
        "standing-0-ygyro": [],
        "standing-0-zgyro": [],
        "standing-0-tgyro": [],
        "walking-0-xgyro": [],
        "walking-0-ygyro": [],
        "walking-0-zgyro": [],
        "walking-0-tgyro": [],
        "jumping-0-xgyro": [],
        "jumping-0-ygyro": [],
        "jumping-0-zgyro": [],
        "jumping-0-tgyro": [],
        "driving-1-xgyro": [],
        "driving-1-ygyro": [],
        "driving-1-zgyro": [],
        "driving-1-tgyro": [],
        "standing-1-xgyro": [],
        "standing-1-ygyro": [],
        "standing-1-zgyro": [],
        "standing-1-tgyro": [],
        "walking-1-xgyro": [],
        "walking-1-ygyro": [],
        "walking-1-zgyro": [],
        "walking-1-tgyro": [],
        "jumping-1-xgyro": [],
        "jumping-1-ygyro": [],
        "jumping-1-zgyro": [],
        "jumping-1-tgyro": [],
    }
    return res

def main(csv_path):
    # collect data from csv file
    with open(csv_path, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        # containers for the data
        collector = build_dataDict()
        for row in datareader:
            if row[TEAM] != 'team6':
                continue

            # extract data from csv file
            activity = row[ACTIVITY].lower()
            index = row[FILE_INDEX]

            collector[activity + "-" + index + "-xmag"].append(float(row[XMAG]))
            collector[activity + "-" + index + "-ymag"].append(float(row[YMAG]))
            collector[activity + "-" + index + "-zmag"].append(float(row[ZMAG]))
            collector[activity + "-" + index + "-tmag"].append(float(row[TIME]))

            collector[activity + "-" + index + "-xaccl"].append(float(row[XACCL]))
            collector[activity + "-" + index + "-yaccl"].append(float(row[YACCL]))
            collector[activity + "-" + index + "-zaccl"].append(float(row[ZACCL]))
            collector[activity + "-" + index + "-taccl"].append(float(row[TIME]))

            collector[activity + "-" + index + "-xgyro"].append(float(row[XGYRO]))
            collector[activity + "-" + index + "-ygyro"].append(float(row[YGYRO]))
            collector[activity + "-" + index + "-zgyro"].append(float(row[ZGYRO]))
            collector[activity + "-" + index + "-tgyro"].append(float(row[TIME]))

        # directory management
        if not os.path.exists("graphs"):
            os.mkdir("graphs")
        
        # at least 24 graphs in total (4 activities, 2 indexes, 3 variables)
        figs = []
        for activity in ['driving', 'walking', 'jumping', 'standing']:
            for index in range(2):
                for var in ['mag', 'gyro', 'accl']:
                    print(activity + " " + str(index) + " " + var)
                    fig = px.scatter_3d(x=collector[activity + "-" + str(index) + "-x" + var],
                                        y=collector[activity + "-" + str(index) + "-y" + var],
                                        z=collector[activity + "-" + str(index) + "-z" + var],
                                        color=collector[activity + "-" + str(index) + "-t" + var])
                    # fig.write_image("graphs/" + activity + "_" + var + "_" + str(index) + ".png")
                    fig.update_layout(title=activity + "_" + var + "_" + str(index))
                    figs.append(fig)
        
        for fig in figs:
            fig.show()


if __name__ == '__main__':
    # plotly.io.orca.ensure_server()
    # print("Waiting for server...")
    # time.sleep(10)
    # print("Good to go!")
    main(sys.argv[1])
    input("Press any key to continue...")
