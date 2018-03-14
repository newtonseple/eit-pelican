from dronekit import connect, VehicleMode
import time

def connect_to_drone(connection_string):

    #Simulator
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default(lat=63.411976, lon=10.408972)
        connection_string = sitl.connection_string()

    return connect(connection_string, wait_ready=True)


def arm_and_takeoff(vehicle, aTargetAltitude):
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

