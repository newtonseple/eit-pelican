import argparse
import threading
import time
from Queue import Queue
from flight_logger import FlightLogger
from flight import setup
from flight.coarse_search import CoarseSearch
from flight.near_search import NearSearch
from barryvox import BarryvoxThread

DRONE_CON_STRING = "0.0.0.0:14550"
TAKEOFF_ALTITUDE = 3.0

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

    flight_logger = FlightLogger(vehicle)
    flight_logger.daemon = True
    flight_logger.start()

    signal_queue = Queue()

    # t = threading.Thread(target=test_signal_feeder, args=(signal_queue, ))
    # t.start()

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
    #while not signal_queue.get(block=True)[0]:
    while signal_queue.get(block=True)[2] > 6:
        pass

    cs.stop()
    last_target = cs.target
    print("Last target: ")
    print(last_target)
    near_mode(vehicle, area, signal_queue, last_target)


def near_mode(vehicle, area, signal_queue, last_target):

    print "Start near search"
    ns = NearSearch(vehicle, area, signal_queue, last_target)
    ns.start()

    ns.join()


# # Just a test
# def test_signal_feeder(signal_queue):

#     time.sleep(5)
#     signal_queue.put((True, "normal", 5))
#     time.sleep(7)
#     signal_queue.put((False, "no_signal", 7))
#     time.sleep(3)
#     signal_queue.put((True, "normal", 5))
#     time.sleep(7)
#     signal_queue.put((False, "no_signal", 7))
#     time.sleep(3)
#     signal_queue.put((True, "normal", 5))
#     time.sleep(7)
#     signal_queue.put((False, "no_signal", 7))


if __name__ == "__main__":
    main()
