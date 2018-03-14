import math
from dronekit import LocationGlobalRelative as Pos

# def generate_area(coords, alt):
#     return {"A": Pos(coords[0], coords[1], alt),
#             "B": Pos(coords[2], coords[3], alt),
#             "C": Pos(coords[4], coords[5], alt),
#             "D": Pos(coords[6], coords[7], alt) }

def generate_area(coords, alt):
    return (Pos(coords[0], coords[1], alt),
            Pos(coords[2], coords[3], alt),
            Pos(coords[4], coords[5], alt),
            Pos(coords[6], coords[7], alt) )

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two `LocationGlobal` or `LocationGlobalRelative` objects.
    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


