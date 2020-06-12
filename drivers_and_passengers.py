import search
from utils import manhattan_distance
from collections import defaultdict
import copy
import itertools
import random
import heapq


MAX_DISTANCE = 300


class DriversAndPassengers(search.Problem):
    """
    Solves the Som Mobilitat challenge
    """
    def __init__(self, initial):
        search.Problem.__init__(self, initial)

    def actions(self, state):
        """
        Given a state returns all legal actions (no collisions)
        """
        #return state.get_all_possible_driver_passenger_pairs()
        #return state.get_drivers_only_next_passenger_pairs()
        return state.get_closest_drivers_only_next_passenger_pairs()

    def legal(self, state, action):
        return False

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        new_state.add_passenger_driver_best_position(action[0], action[1])
        return new_state

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        return state.goodness()


class DriversAndPassengersState:
    initial_users = []
    number_of_drivers = 0
    drivers = []
    distance_to_drivers = []
    closest_drivers = 10

    def __init__(self, drivers = None, passengers = None):
        self.remaining_passengers = []
        self.allocated_passengers = []
        self.run_out_of_passengers = False
        if drivers and passengers:
            self.initial_users = [(id, origin, destination) for id, origin, destination in drivers] + \
                                 [(id, origin, destination) for id, origin, destination in passengers]
            self.number_of_drivers = len(drivers)
            self.drivers = [Driver(id, origin, destination) for id, origin, destination in drivers]
            self.remaining_passengers = [i for i, o, d in passengers]
            random.shuffle(self.remaining_passengers)
        if not self.distance_to_drivers:
            self.distance_to_drivers = [301]*len(self.initial_users)
            self.calculate_driver_passenger_distance()



    def add_passenger_driver(self, passenger_id, driver_id, pick_pos=1, drop_pos=2):
        if self.drivers[driver_id].add_passenger(self.initial_users[passenger_id], pick_pos, drop_pos):
            self.update_passenger_driver_lists(passenger_id, driver_id)
            return True
        return False

    def add_passenger_driver_best_position(self, passenger_id, driver_id):
        positions = self.generate_pick_drop_positions(driver_id)
        min_dist = MAX_DISTANCE + 1
        min_pos = tuple((-1,-1))
        for pick_pos, drop_pos in positions:
            if self.drivers[driver_id].add_passenger(self.initial_users[passenger_id], pick_pos, drop_pos):
                if min_dist > self.drivers[driver_id].distance:
                    min_dist = self.drivers[driver_id].distance
                    min_pos = tuple((pick_pos, drop_pos))
                self.drivers[driver_id].remove_passenger(self.initial_users[passenger_id], pick_pos, drop_pos)
        if min_dist < MAX_DISTANCE + 1:
            self.drivers[driver_id].add_passenger(self.initial_users[passenger_id], min_pos[0], min_pos[1])
            self.update_passenger_driver_lists(passenger_id, driver_id)

    def update_passenger_driver_lists(self, passenger_id, driver_id):
        self.remaining_passengers.remove(passenger_id)
        self.allocated_passengers.append(passenger_id)
        if self.run_out_of_passengers: # driver is not a passenger candidate anymore
            if driver_id in self.remaining_passengers:
                self.remaining_passengers.remove(driver_id)

    def generate_pick_drop_positions(self, driver_id):
        length = len(self.drivers[driver_id].get_destinations())
        return itertools.combinations(range(1,length+1),2)

    def user_origin(self, user):
        return self.initial_users[user][1]

    def user_destination(self, user):
        return self.initial_users[user][2]

    def get_drivers_only_next_passenger_pairs(self):
        if not self.run_out_of_passengers and not self.remaining_passengers:
            self.remaining_passengers = self.get_empty_drivers()
            self.run_out_of_passengers = True
        if not self.remaining_passengers:
            return []
        return [(self.remaining_passengers[0], d) for d in range(len(self.drivers)) #if self.drivers[d].distance < MAX_DISTANCE * 0.9
                if self.remaining_passengers[0] != d and d not in self.allocated_passengers]

    def get_closest_drivers_only_next_passenger_pairs(self):
        if not self.run_out_of_passengers and not self.remaining_passengers:
            self.remaining_passengers = self.get_empty_drivers()
            self.run_out_of_passengers = True
        if not self.remaining_passengers:
            return []
        return [(self.remaining_passengers[0], d) for (dist,d) in heapq.nsmallest(self.closest_drivers, self.distance_to_drivers[self.remaining_passengers[0]]) #if self.drivers[d].distance < MAX_DISTANCE * 0.9
                if self.remaining_passengers[0] != d and d not in self.allocated_passengers]

    def get_all_possible_driver_passenger_pairs(self):
        if not self.run_out_of_passengers and not self.remaining_passengers:
            self.remaining_passengers = self.get_empty_drivers()
            self.run_out_of_passengers = True
        return [(p, d) for d in range(len(self.drivers)) if self.drivers[d].distance < MAX_DISTANCE * 0.9
                for p in self.remaining_passengers if p != d and d not in self.allocated_passengers]

    def number_of_drivers(self):
        return self.number_of_drivers

    def drivers_id(self):
        return [d.id for d in self.drivers]

    def get_empty_drivers(self):
        return [d.id for d in self.drivers if len(d.passengers) == 2]

    def remaining_passengers_id(self):
        return self.remaining_passengers

    def goodness(self, debug=False):
        value = 0
        for driver in self.drivers:
            passengers = driver.get_passengers_id()

            min_distance = manhattan_distance(driver.origin(), driver.destination())
            if passengers:
                value += MAX_DISTANCE - (driver.distance - min_distance)
                if debug:
                    print('driver with p: ', driver.id, ' val: ', MAX_DISTANCE - (driver.distance - min_distance))
            else: # empty driver
                value += min_distance
                if debug:
                    print('driver with no p: ', driver.id, ' val: ', min_distance)

            # passengers
            for passenger in set(passengers):
                value += manhattan_distance(self.user_origin(passenger), self.user_destination(passenger)) + MAX_DISTANCE
                if debug:
                    print('passenger: ', passenger, ' val: ', manhattan_distance(self.user_origin(passenger), self.user_destination(passenger)) + MAX_DISTANCE)
        return value

    def calculate_driver_passenger_distance(self):
        for u in range(len(self.initial_users)):
            self.distance_to_drivers[u] = self.distance_user_driver(u)

    def distance_user_driver(self, user):
        distances = []
        for d in self.drivers:
            if user != d.id:
                if d.add_passenger(self.initial_users[user]):
                    distance = d.driven_distance()
                    d.remove_passenger(self.initial_users[user])
                else:
                    distance = 301
                distances.append((distance, d.id))
        return distances

    def __str__(self):
        result = ''
        for driver in self.drivers:
            #if driver.id not in self.allocated_passengers:
            result += driver.__str__() + '\n'
        return result

    def write_out_file (self, name):
        file = open(name, 'w')
        for driver in self.drivers:
            if driver.id not in self.allocated_passengers:
                driver.write_out_file(file)
                file.write("\n")


class Driver:
    def __init__(self, id, origin = (0,0), destination = (0,0)):
        self.id = id
        self.passengers = [(id, origin), (id, destination)]
        self.distance = manhattan_distance(origin, destination)

    def add_passenger(self, passenger, pick_pos=1, drop_pos=2):
        if pick_pos >= drop_pos or pick_pos < 1 or drop_pos < 2 or pick_pos > len(self.passengers) or drop_pos > len(self.passengers)+1:
            raise Exception('Adding Passenger in illegal position')
        self.passengers.insert(pick_pos, (passenger[0], passenger[1]))
        self.passengers.insert(drop_pos, (passenger[0], passenger[2]))
        if self.too_many_passengers() or self.driven_distance() >= MAX_DISTANCE:
            self.passengers.pop(drop_pos)
            self.passengers.pop(pick_pos)
            return False
        self.distance = self.driven_distance()
        return True

    def remove_passenger(self, passenger, pick_pos=1, drop_pos=2):
        if self.passengers[pick_pos][0] != passenger[0] or self.passengers[drop_pos][0] != passenger[0]:
            raise Exception('Removing incorrect passenger')
        self.passengers.pop(drop_pos)
        self.passengers.pop(pick_pos)

    def too_many_passengers(self):
        passengers_in_driver = 0
        seen_passenger = defaultdict(int)
        for p in self.get_passengers_id():
            if seen_passenger[p] > 0:
                passengers_in_driver -= 1
            else:
                passengers_in_driver += 1
                seen_passenger[p] += 1
            if passengers_in_driver > 2 or passengers_in_driver < 0:
                return True
        return passengers_in_driver != 0

    def driven_distance(self):
        points = self.get_destinations()
        return sum([manhattan_distance(o, d) for o, d in zip(points[:-1], points[1:])])

    def get_destinations(self):
        return [point for idx, point in self.passengers]

    def get_passengers_id(self):
        passenger_plus_driver = [id for id, point in self.passengers]
        return passenger_plus_driver[1:-1]

    def origin(self):
        return self.passengers[0][1]

    def destination(self):
        return self.passengers[-1][1]

    def __str__(self):
        return self.passengers.__str__() + ' direct dist: ' + str(manhattan_distance(self.origin(), self.destination())) + ' dist: ' + str(self.distance)

    def write_out_file(self, file):
        for n in self.passengers:
            file.write ("%d %d %d " % (n[0],  n[1][0], n[1][1]))


