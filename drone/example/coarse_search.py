import math
import dronekit
import numpy
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
vehicle = connect(connection_string, wait_ready=True)


# FUNCTION DEFINITIONS ===================================================================================================================

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


def goto_position(position):

# Send drone to position
	vehicle.simple_goto(position)

#While the drone is flying to new position, wait
	while get_distance_metres(vehicle.location.global_relative_frame, position) >= 0.5:
    		print "Flying to specified location. Current altitude: ", vehicle.location.global_relative_frame.alt, "m",\
		"  Lateral distance to target: ", "%.2f" % get_distance_metres(vehicle.location.global_relative_frame, position), "m"
    		time.sleep(1)
print "Reaced target location"

def coarse_search(A, B, C, D, dt, search_altitude):

#Define the grid
    L1 = get_distance_metres(A,B)
    L2 = get_distance_metres(A,D)

    Nt = L2/dt + 1
    Nt = int(math.ceil(Nt))
    t = numpy.linspace(0,L2,num=Nt)
    y1= numpy.zeros((2, Nt))
    y2 = y1

    for i in range(0, Nt-1):
	y1[0, i] = A[0] + t[i]*(B[0]-A[0])/L2
	y1[1, i] = A[1] + t[i]*(B[1]-A[1])/L2
	y2[0, i] = C[0] + t[i]*(C[0]-B[0])/L2
	y2[1, i] = C[1] + t[i]*(C[1]-B[1])/L2

    dt_check = L2/(Nt-1)
    print('The calculated dt is', dt_check, 'm')

    #Go to corner A
    goto_position(LocationGlobalRelative(y1[0,0], y1[1,0], search_altitude))

    #Go to corner B
    goto_position(LocationGlobalRelative(y2[0,0], y2[1,0], search_altitude))

    side = 1
    for i in range(1, Nt):
        if side is 1:
            goto_position(LocationGlobalRelative(y2[0, i], y2[1, i], search_altitude))
            goto_position(LocationGlobalRelative(y1[0, i], y1[1, i], search_altitude))
            side = 0
        elif side is 0:
            goto_position(LocationGlobalRelative(y1[0, i], y1[1, i], search_altitude))
            goto_position(LocationGlobalRelative(y2[0, i], y2[1, i], search_altitude))
            side = 1

	vehicle.mode = VehicleMode("RTL")

#START CODE FROM HERE ===============================================================================================================
# Arm drone and take off to specified altitute [meters above take off position]
arm_and_takeoff(10)
coarse_search([63.41209483064148, 10.408899100524877], [63.41209483064148, 10.40934434722135], [63.412327722265836, 10.408899100524877], [63.412327722265836, 10.40934434722135], 1, 3)

			
			
