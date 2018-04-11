import logging
import threading
import time

class FlightLogger(threading.Thread):

    def __init__(self, vehicle):
        super(FlightLogger, self).__init__()
        logging.basicConfig(filename='flight.log',level=logging.DEBUG)
        self.vehicle = vehicle

    def run(self):
        while True:
            pos = self.vehicle.location.global_relative_frame
            logging.info('{ "lat": %f, "lon": %f}', pos.lat, pos.lon)
            time.sleep(1)
