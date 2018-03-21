import argparse
import threading
from flight import setup
from flight.coarse_search import CoarseSearch
from flight.near_search import NearSearch
import time
from Queue import Queue

DRONE_CON_STRING = "0.0.0.0:14550"
AIRSPEED = 4
SEARCH_ALTITUDE = 10

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

    vehicle.airspeed = AIRSPEED
    setup.arm_and_takeoff(vehicle, SEARCH_ALTITUDE)

    start_search(vehicle, args.area)


def start_search(vehicle, area):

    #TODO: Pass this to signal-processor, and to the instances wanting to consume it as well (one at a time!)
    signal_queue = Queue()

    cs = CoarseSearch(vehicle, area, SEARCH_ALTITUDE)
    cs.start()

    time.sleep(20)
    cs.stop()



if __name__ == "__main__":
    main()
