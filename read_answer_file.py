from collections import defaultdict
import read_in_file as rif
import utils

MAX_DISTANCE = 300


def parse_answer(answer_file):
    drivers=[]
    f = open(answer_file, 'r')
    for line in f:
        if line.strip():
            driver = parse_driver(line)
            drivers.append(driver)
    f.close()
    return drivers


def parse_driver(line):
    driver = [int(x) for x in line.split()]
    if len(driver) % 6 != 0:
        raise Exception('All users should have origin ox oy and destination dx dy')
    idxs, points = get_indexes_and_points_separated_lists(driver)
    point_tuples = tuple([(x, y) for x, y in utils.pairwise(points)])
    idxs_and_points = [(idx, point) for idx, point in zip(idxs, point_tuples)]
    return idxs_and_points


def get_indexes_and_points_separated_lists(driver):
    return [driver[idx] for idx in range(len(driver)) if idx % 3 == 0], [driver[idx] for idx in range(len(driver)) if idx % 3 != 0]


def legal_answer(answer, D, drivers, users):
    if not actual_drivers(answer, D, drivers):
        print('A driver is not an actual driver')
        return False
    if not actual_users(answer, D, drivers + users):
        print('A user (driver or passenger) is not an actual user')
        return False

    if not users_appear_once_at_most(answer):
        print('A user appears more than once')
        return False

    if not drivers_with_legal_passengers(answer):
        print('Driver with illegal passenger')
        return False

    if not drivers_within_distance(answer):
        print('Driver drives beyond maxim distance')
        return False

    return True


def drivers_with_legal_passengers(drivers):
    """checks max 2 passengers and gets/drops all of them
    A passenger can only be driven once by the same driver"""
    passenger_counts = defaultdict(int)
    for driver in drivers:
        passengers = get_driver_idx_passengers(driver)
        passenger_in_car = 0
        for passenger in passengers:
            passenger_counts[passenger] += 1
            if passenger_counts[passenger] == 1:
                passenger_in_car += 1
            if passenger_counts[passenger] == 2:
                passenger_in_car -=1
            if passenger_in_car > 3 or passenger_counts[passenger] > 2:
                return False
        if passenger_in_car > 0:
            return False
    return True


def drivers_within_distance(drivers):
    """Checks drivers drive within distance limit"""
    return all([driven_distance(driver) <= MAX_DISTANCE for driver in drivers])


def driven_distance(driver):
    points = get_driver_destinations(driver)
    return sum([utils.manhattan_distance(o, d) for o, d in zip(points[:-1], points[1:])])


def get_driver_destinations(driver):
    return [point for idx, point in driver]


def get_driver_idx_passengers(driver):
    return [idx for idx, point in driver]


def get_driver_passengers(driver):
    passengers = defaultdict(list)
    for passenger in driver[1:-1]:
        idx, point = passenger
        passengers[idx].append([idx, point])

    result = []
    for passenger in passengers.values():
        result.append(tuple((passenger[0][0], passenger[0][1], passenger[1][1])))
    return result


def actual_drivers(answer, D, drivers):
    """ Drivers have same origin/destination as in the input file.
    if driver idx >= D means it's a user that can not drive"""
    return all([equal_driver(ad, drivers[ad[0][0]]) if ad[0][0] < D else False for ad in answer])


def actual_users(answer, D, all_users):
    """All passengers have same origin/destination than the ones defined in the input file
    Recall that a passenger can be either a non driving user or a driver"""
    for driver in answer:
        passengers = get_driver_passengers(driver)
        if not all([all_users[passenger[0]] == passenger for passenger in passengers]):
            return False
    return True


def equal_driver(answer_driver, driver):
    idx, ad_origin = answer_driver[0]
    idx, ad_dest = answer_driver[-1]
    return tuple((idx, ad_origin, ad_dest)) == driver


def users_appear_once_at_most(answer):
    """A driver can only drive once and a passenger can be driven only once"""
    user_counts = defaultdict(int)
    for driver in answer:
        driver_and_passenger_idx = set([driver[idx] for idx in range(len(driver)) if idx % 3 == 0])
        for user_idx in driver_and_passenger_idx:
            user_counts[user_idx] += 1
            if user_counts[user_idx] > 1:
                return False
    return True


answer = parse_answer('i_o_files/small_5_2' + '.out')
N, M, D, U, drivers, users = rif.parse_in('i_o_files/small_5_2' + '.in')
print('legal: ', legal_answer(answer, D, drivers, users))