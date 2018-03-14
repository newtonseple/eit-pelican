from ..helper import get_distance_metres, generate_area
from dronekit import LocationGlobalRelative as Pos, VehicleMode
import threading
import numpy
import math
import time
from itertools import cycle

GRANULARITY = 2
TOLERANCE = 0.7

class CoarseSearch(threading.Thread):

    def __init__(self, vehicle, area_coords, search_altitude):
        super(CoarseSearch, self).__init__()
        self._stop_event = threading.Event()
        self.vehicle = vehicle

        dt = GRANULARITY

        #Generate search pattern
        A,B,C,D = generate_area(area_coords, search_altitude)
        length = get_distance_metres(A, D)

        num_steps = math.ceil(length/dt + 1)
        steps = numpy.linspace(0, length, num=num_steps)

        left_lat_step = (D.lat-A.lat)/length
        left_lon_step = (D.lon-A.lon)/length
        left = [Pos(A.lat + t*left_lat_step, A.lon + t*left_lon_step, search_altitude) for t in steps]

        right_lat_step = (C.lat-B.lat)/length
        right_lon_step = (C.lon-B.lon)/length
        right = [Pos(B.lat + t*right_lat_step, B.lon + t*right_lon_step, search_altitude) for t in steps]

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

        self.vehicle.simple_goto(target)

        while not self.stopped():
            print "Flying to specified location. Current altitude: ", self.vehicle.location.global_relative_frame.alt, "m",\
            "  Lateral distance to target: ", "%.2f" % get_distance_metres(self.vehicle.location.global_relative_frame, target), "m"

            if get_distance_metres(self.vehicle.location.global_relative_frame, target) <= TOLERANCE:
                print ">>> Target reached!"
                target = next(targets)
                self.vehicle.simple_goto(target)

            time.sleep(1)


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
