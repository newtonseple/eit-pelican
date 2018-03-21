from dronekit import LocationGlobalRelative as Pos
import math

def generate_area(coords, alt):
    return (Pos(coords[0], coords[1], alt),
            Pos(coords[2], coords[3], alt),
            Pos(coords[4], coords[5], alt),
            Pos(coords[6], coords[7], alt) )

def get_distance_metres(aLocation1, aLocation2):
    # https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
