from dronekit import LocationGlobalRelative as Pos
from helper import get_distance_metres, generate_area
import threading
import numpy
import time

AIRSPEED = 1.0
TOLERANCE = 0.7
SEARCH_ALTITUDE = 3.0

class NearSearch(threading.Thread):

    def __init__(self, vehicle, area_coords, signal_queue):
        super(NearSearch, self).__init__()
        self.vehicle = vehicle
        self.signal_queue = signal_queue

        self.vehicle.airspeed = AIRSPEED

        A,_,_,D = generate_area(area_coords, SEARCH_ALTITUDE)
        length = get_distance_metres(A, D)

        self.y_lat_step = (D.lat-A.lat)/length
        self.y_lon_step = (D.lon-A.lon)/length

        # Create signal key point list, add the first point of contact
        self.key_points = [self.vehicle_location()]

    def run(self):

        self.continue_straight()
        self.center_on_line()
    
    def continue_straight(self):
        # Look for next key_point, the point of contact-loss continuing in the same direction
        cont = True
        while cont:
            while cont and not self.signal_queue.empty():
                signal = self.signal_queue.get()

                if not signal[0]:
                # if signal[2] > 6:
                    self.key_points.append(self.vehicle_location())
                    cont = False


    def center_on_line(self):

        print "Center on line"
        point_A = self.key_points[0]
        point_B = self.key_points[1]
        
        lat = (point_A.lat + point_B.lat) / 2.0
        lon = (point_A.lon + point_B.lon) / 2.0
        center = Pos(lat, lon, SEARCH_ALTITUDE)

        self.vehicle.simple_goto(center)

        while get_distance_metres(self.vehicle_location(), center) > TOLERANCE:
            pass

        print ">> Centered on line"
        self.key_points.append(self.vehicle_location())

        self.go_perpendicular(center)

    def go_perpendicular(self, center):

        point_C = self.key_points[2]

        bound = 50
        upper_lat = point_C.lat + self.y_lat_step * bound 
        upper_lon = point_C.lon + self.y_lon_step * bound 
        lower_lat = point_C.lat + self.y_lat_step * (-bound)
        lower_lon = point_C.lon + self.y_lon_step * (-bound) 

        t1, t2 = (Pos(upper_lat, upper_lon, SEARCH_ALTITUDE), Pos(lower_lat, lower_lon, SEARCH_ALTITUDE))

        print("Go to top")
        self.vehicle.simple_goto(t1)
        self.continue_straight()
        print("Reached top")
        
        print("Go back to center")
        self.vehicle.simple_goto(center)
        while get_distance_metres(self.vehicle_location(), center) > TOLERANCE:
            pass
        print("Reached center")

        print("Go to bottom")
        self.vehicle.simple_goto(t2)
        self.continue_straight()

        point_A, point_B = self.key_points[-2:]

        lat = (point_A.lat + point_B.lat) / 2.0
        lon = (point_A.lon + point_B.lon) / 2.0

        print ">>>> PERSON LOCATED:"
        print ">>>>  lat:",lat,"  lon:",lon

        self.vehicle.mode = VehicleMode("LAND")

    def vehicle_location(self):
        return self.vehicle.location.global_relative_frame
