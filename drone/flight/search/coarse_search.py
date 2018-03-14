from ..helper import get_distance_metres
from dronekit import LocationGlobalRelative, VehicleMode
import numpy
import math
import time

GRANULARITY = 2

def start(vehicle, area, search_altitude):

    A = area["A"]
    B = area["B"]
    C = area["C"]
    D = area["D"]

    dt = GRANULARITY

    #Define the grid
    A1 = LocationGlobalRelative(A[0], A[1], search_altitude)
    B1 = LocationGlobalRelative(B[0], B[1], search_altitude)
    C1 = LocationGlobalRelative(C[0], C[1], search_altitude)
    D1 = LocationGlobalRelative(D[0], D[1], search_altitude)
    L1 = get_distance_metres(A1, B1)
    L2 = get_distance_metres(A1, D1)
    print 'L1 = ',L1
    print 'L2 = ',L2
    
    Nt = L2/dt + 1
    Nt = int(math.ceil(Nt))
    t = numpy.linspace(0,L2,num=Nt)
    y1= numpy.zeros((2, Nt))
    y2= numpy.zeros((2, Nt))

    for i in range(0, Nt):
        y1[0, i] = A[0] + t[i]*(D[0]-A[0])/L2
        y1[1, i] = A[1] + t[i]*(D[1]-A[1])/L2
        y2[0, i] = B[0] + t[i]*(C[0]-B[0])/L2
        y2[1, i] = B[1] + t[i]*(C[1]-B[1])/L2
    dt_check = L2/(Nt-1)
    print 'The calculated dt is', dt_check, 'm'

    #Go to corner A
    goto_position(vehicle, LocationGlobalRelative(y1[0,0], y1[1,0], search_altitude))
    print "Reached A"
    #Go to corner B
    goto_position(vehicle, LocationGlobalRelative(y2[0,0], y2[1,0], search_altitude))
    print "Reached B"
    side = 1
    for i in range(1, Nt):
        if side is 1:
            goto_position(vehicle, LocationGlobalRelative(y2[0, i], y2[1, i], search_altitude))
            goto_position(vehicle, LocationGlobalRelative(y1[0, i], y1[1, i], search_altitude))
            side = 0
        elif side is 0:
            goto_position(vehicle, LocationGlobalRelative(y1[0, i], y1[1, i], search_altitude))
            goto_position(vehicle, LocationGlobalRelative(y2[0, i], y2[1, i], search_altitude))
            side = 1
        print 'Starting new iteration! Current iteration', 'i = ',i, ' Side = ',side 
  
    vehicle.mode = VehicleMode("RTL")
    print 'Returning home. Mission not completed'
    vehicle.close()


def goto_position(vehicle, position):

# Send drone to position
    vehicle.simple_goto(position)

#While the drone is flying to new position, wait
    while get_distance_metres(vehicle.location.global_relative_frame, position) >= 0.5:
            print "Flying to specified location. Current altitude: ", vehicle.location.global_relative_frame.alt, "m",\
        "  Lateral distance to target: ", "%.2f" % get_distance_metres(vehicle.location.global_relative_frame, position), "m"
            time.sleep(1)
    print "Reaced target location"
