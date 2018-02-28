from dronekit import connect
import sys

#simualtor imports
import dronekit_sitl

# Connect to UDP endpoint (and wait for default attributes to accumulate)
# Device
target = 'udpin:0.0.0.0:14550' #Drone

# SIMULATOR ACTIVATION
# sitl = dronekit_sitl.start_default()
# target = sitl.connection_string()
# END SIMULATOR ACTIVATION

print 'Connecting to ' + target + '...'
vehicle = connect(target, wait_ready=True)

# Get all vehicle attributes (state)
print "Vehicle state:"
print " Global Location: %s" % vehicle.location.global_frame
print " Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print " Local Location: %s" % vehicle.location.local_frame
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Heading: %s" % vehicle.heading
print " Groundspeed: %s" % vehicle.groundspeed
print " Airspeed: %s" % vehicle.airspeed
print " Mode: %s" % vehicle.mode.name
print " Is Armable?: %s" % vehicle.is_armable
print " Armed: %s" % vehicle.armed

vehicle.close()
print "Done."
