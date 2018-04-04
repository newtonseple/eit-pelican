import argparse
import threading
import time
from Queue import Queue
from flight import setup
from flight.coarse_search import CoarseSearch
from flight.near_search import NearSearch
from barryvox import BarryvoxThread

DRONE_CON_STRING = "0.0.0.0:14550"
TAKEOFF_ALTITUDE = 10.0

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Simulator/drone and search-area')
    parser.add_argument('--device', help="simulator or drone, default is simulator")
    parser.add_argument('--area', nargs='+',
                        default=[63.41155685054248, 10.408640161710764, 63.41155685054248, 10.408996895509745,
                                 63.41186057535474, 10.408996895509745, 63.41186057535474, 10.408640161710764],
                        type=float, help="list of coords, A,B,C,D")
    args = parser.parse_args()

    con_string = DRONE_CON_STRING if args.device == "drone" else None

    # Setup and start drone
    vehicle = setup.connect_to_drone(con_string) #given "None" the simulator is used.

    setup.arm_and_takeoff(vehicle, TAKEOFF_ALTITUDE)

    start_search(vehicle, args.area)


def start_search(vehicle, area):

    signal_queue = Queue()

    barryvox = BarryvoxThread(signal_queue)
    barryvox.daemon = True
    barryvox.start()

    coarse_mode(vehicle, area, signal_queue)


def coarse_mode(vehicle, area, signal_queue):

    print "Start coarse search"
    cs = CoarseSearch(vehicle, area)
    cs.daemon = True
    cs.start()

    # Coarse search until we get a signal
    # while not signal_queue.get(block=True)[0]:
    while signal_queue.get(block=True)[2] > 6:
        pass

    cs.stop()
    near_mode(vehicle, area, signal_queue)


def near_mode(vehicle, area, signal_queue):

    print "Start near search"
    ns = NearSearch(vehicle, area, signal_queue)
    ns.start()

    ns.join()

if __name__ == "__main__":
    main()
