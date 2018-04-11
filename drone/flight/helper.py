from dronekit import LocationGlobalRelative as Pos
import math

def generate_area(coords, alt):
    return (Pos(coords[0], coords[1], alt),
            Pos(coords[2], coords[3], alt),
            Pos(coords[4], coords[5], alt),
            Pos(coords[6], coords[7], alt) )

def get_distance_metres(aLocation1, aLocation2)
    # Distance formula based on Haversine formula
    R = 6371230  # m, Mean Earth Radius
    phi1 = aLocation1.lat * math.atan(1) * 4 / 180
    phi2 = aLocation2.lat * math.atan(1) * 4 / 180
    theta1 = aLocation1.lon * math.atan(1) * 4 / 180
    theta2 = aLocation2.lon * math.atan(1) * 4 / 180

    A = (math.sin((phi2 - phi1) / 2)) ^ 2
    B = math.cos(phi1) * math.cos(phi2)
    C = (math.sin((theta2 - theta1) / 2)) ^ 2

    return 2 * R * math.asin(math.sqrt(A + B * C))
