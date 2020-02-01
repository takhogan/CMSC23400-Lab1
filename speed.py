#!/usr/bin/python3

# a small tool for exporting speed

import csv
import os
import sys
import math

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
        "standing-0-dt": [],
        "standing-0-t": [],
        "walking-0-dt": [],
        "walking-0-t": [],
        "jumping-0-dt": [],
        "jumping-0-t": [],
        "standing-0-dt": [],
        "standing-0-t": [],
        "driving-0-dt": [],
        "driving-0-t": [],

        "standing-1-dt": [],
        "standing-1-t": [],
        "walking-1-dt": [],
        "walking-1-t": [],
        "jumping-1-dt": [],
        "jumping-1-t": [],
        "standing-1-dt": [],
        "standing-1-t": [],
        "driving-1-dt": [],
        "driving-1-t": [],
    }
    return res


def main(csv_path):
    # collect data from csv file
    with open(csv_path, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        collector = build_dataDict()
        # get relevant data to our team
        for row in datareader:
            if row[TEAM] != 'team6':
                continue
            
            # extract data from csv file
            activity = row[ACTIVITY].lower()
            index = row[FILE_INDEX]

            # when retreaving z acceleration, subtract 1g
            collector[activity + "-" + index + "-dt"].append(math.sqrt(
                                                             pow(float(row[XACCL]), 2) +
                                                             pow(float(row[YACCL]), 2) +
                                                             pow(float(row[ZACCL]) - 1000, 2)
                                                            ))
            collector[activity + "-" + index + "-t"].append(float(row[TIME]))
        
        if not os.path.exists("dataout"):
            os.mkdir("dataout")

        with open("dataout/speeds.csv", mode="w") as dataout:
            outwriter = csv.writer(dataout, delimiter=',', quotechar='|')
            outwriter.writerow(["activity", "index", "velocity", "upper-bound (seconds)"])
            for activity in ["standing", "jumping", "driving", "walking"]:
                for index in ["0", "1"]:
                    ave = sum(collector[activity + "-" + index + "-dt"])
                    outwriter.writerow([activity, index, ave, max(collector[activity + "-" + index + "-t"])])


if __name__ == '__main__':
    main(sys.argv[1])