import argparse  
from flight import setup, helper
from flight.search import coarse_search

DRONE_CON_STRING = "0.0.0.0:14550"
AIRSPEED = 4
SEARCH_ALTITUDE = 10

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Simulator/drone and search-area')
    parser.add_argument('--device', help="simulator or drone, default is simulator")
    parser.add_argument('--area', nargs='+',
                        default=[63.41155685054248, 10.408640161710764,
                                 63.41155685054248, 10.408996895509745,
                                 63.41186057535474, 10.408996895509745,
                                 63.41186057535474, 10.408640161710764
                            ],
                        type=float, help="list of coords, A,B,C,D")
    args = parser.parse_args()

    con_string = DRONE_CON_STRING if args.device == "drone" else None
    area = helper.coords_to_area(args.area)

    # Setup and start drone
    vehicle = start_drone(con_string)

    start_search(vehicle, area)


def start_drone(con_string):
    vehicle = setup.connect_to_drone(con_string) #given "None" the simulator is used.

    vehicle.airspeed = AIRSPEED
    setup.arm_and_takeoff(vehicle, SEARCH_ALTITUDE)
    return vehicle

def start_search(vehicle, area):
    coarse_search.start(vehicle, area, SEARCH_ALTITUDE)
    return 1



if __name__ == "__main__":
    main()