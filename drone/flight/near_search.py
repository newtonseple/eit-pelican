from dronekit import LocationGlobalRelative as Pos
from helper import get_distance_metres
import threading
import numpy
import time

TOLERANCE = 0.7

class NearSearch(threading.Thread):

    def __init__(self, vehicle, signal_queue):
        super(NearSearch, self).__init__()
        self._stop_event = threading.Event()
        self.vehicle = vehicle
        self.signal_queue = signal_queue


    def run(self):

        while keep_running():
            while keep_running() and not self.signal_queue.empty():

                print q.get()
                time.sleep(1)


    def stop(self):
        self._stop_event.set()

    def keep_running(self):
        return not self._stop_event.is_set()
