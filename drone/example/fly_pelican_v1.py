import math
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time


#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
    

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)


    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    # after Vehicle.simple_takeoff will execute immediately).
    while vehicle.location.global_relative_frame.alt <= aTargetAltitude*0.95:
        print " Altitude: ", vehicle.location.global_relative_frame.alt      
        time.sleep(1)
    
    print " Reached Target Altitude"

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


arm_and_takeoff(10)

print "Set default/target airspeed to 3 m/s"
vehicle.airspeed = 3


# Set target location in global-relative frame
a_location1 = LocationGlobalRelative(63.412040,10.409221,12)
vehicle.simple_goto(a_location1)


while get_distance_metres(vehicle.location.global_relative_frame, a_location1) >= 0.3:
    print " Flying to specified location. Current altitude: ", vehicle.location.global_relative_frame.alt, "m",\
    "  Lateral distance to target: ", get_distance_metres(vehicle.location.global_relative_frame, a_location1), "m"
    time.sleep(1)
print "Reaced target location"

# Set target location in global-relative frame
a_location2 = LocationGlobalRelative(63.412167,10.409146,8)
vehicle.simple_goto(a_location2)

while get_distance_metres(vehicle.location.global_relative_frame, a_location2) >= 0.3: 
    print "Flying to specified location. Current altitude: ", vehicle.location.global_relative_frame.alt, "m",\
    "  Lateral distance to target: ", get_distance_metres(vehicle.location.global_relative_frame, a_location2), "m"
    time.sleep(1)
print "Reaced target location"

a_location3 = LocationGlobalRelative(63.412220,10.409240,10)
vehicle.simple_goto(a_location3)

while get_distance_metres(vehicle.location.global_relative_frame, a_location3) >= 0.3:
    print "Flying to specified location. Current altitude: ", vehicle.location.global_relative_frame.alt, "m",\
    " Lateral distance to target: ", get_distance_metres(vehicle.location.global_relative_frame, a_location3), "m"
    time.sleep(1)
print "Reaced target location"

print "Returning to launch site"
vehicle.mode = VehicleMode("RTL")

vehicle.close()
