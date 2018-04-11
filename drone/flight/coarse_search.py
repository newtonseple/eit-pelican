from dronekit import LocationGlobalRelative as Pos
from helper import get_distance_metres, generate_area
import threading
import numpy
import time
from itertools import cycle

GRANULARITY = 3.0
TOLERANCE = 0.7
AIRSPEED = 2.0
GROUNDSPEED = 2.0
SEARCH_ALTITUDE = 3.0

class CoarseSearch(threading.Thread):

    def __init__(self, vehicle, area_coords):
        super(CoarseSearch, self).__init__()
        self._stop_event = threading.Event()
        self.vehicle = vehicle

        self.vehicle.airspeed = AIRSPEED

        dt = GRANULARITY

        #Generate search pattern
        A,B,C,D = generate_area(area_coords, SEARCH_ALTITUDE)
        length = get_distance_metres(A, D)

        num_steps = int(numpy.ceil(length/dt + 1))
        steps = numpy.linspace(0, length, num=num_steps)

        y_lat_step = (D.lat-A.lat)/length
        y_lon_step = (D.lon-A.lon)/length

        left = [Pos(A.lat + t*y_lat_step, A.lon + t*y_lon_step, SEARCH_ALTITUDE) for t in steps]
        right = [Pos(B.lat + t*y_lat_step, B.lon + t*y_lon_step, SEARCH_ALTITUDE) for t in steps]

        self.search_pattern = []
        # Re-arrange to right-angle zig-zag pattern
        is_left = True
        for l,r in zip(left, right):
            if is_left:
                self.search_pattern.extend([l,r])
            else:
               self.search_pattern.extend([r,l])
            is_left = not is_left


    def run(self):

        targets = cycle(self.search_pattern)
        target = next(targets)

        self.vehicle.simple_goto(target, groundspeed=GROUNDSPEED)

        while self.keep_running():
            print "Lateral distance to target: ", "%.2f" % get_distance_metres(self.vehicle.location.global_relative_frame, target), "m"

            if get_distance_metres(self.vehicle.location.global_relative_frame, target) <= TOLERANCE:
                print ">>> Target reached!"
                target = next(targets)
                self.vehicle.simple_goto(target, groundspeed=GROUNDSPEED)

            #TODO: remove this, not needed.. if you do, also remember to comment out printouts, as they will spam you down
            time.sleep(1)


    def stop(self):
        self._stop_event.set()

    def keep_running(self):
        return not self._stop_event.is_set()
