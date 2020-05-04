from read_answer_file import (parse_answer, legal_answer, driven_distance, get_driver_idx_passengers)
import read_in_file as rif
from utils import manhattan_distance


MAX_DISTANCE = 300


def answer_value(name):
    answer = parse_answer(name + '.out')
    N, M, D, U, drivers, users = rif.parse_in(name + '.in')
    if not legal_answer(answer, D, drivers, users):
        return 0

    value = 0
    for driver in answer:
        passengers = get_driver_passengers_idx(driver)

        # driver only counts if not alone
        if passengers:
            actual_distance = driven_distance(driver)
            min_distance = manhattan_distance(drivers[driver[0][0]][1], drivers[driver[0][0]][2])
            value += MAX_DISTANCE - (actual_distance - min_distance)

        # passengers
        for passenger in passengers:
            if passenger >= D:  # passenger that's not a driver
                value += manhattan_distance(users[passenger - D][1], users[passenger - D][2]) + MAX_DISTANCE
            else:
                value += manhattan_distance(drivers[passenger][1], drivers[passenger][2]) + MAX_DISTANCE
    return value


def get_driver_passengers_idx(driver):
    pass_and_driver = get_driver_idx_passengers(driver)
    return set(pass_and_driver[1:-1])


# print('value: ', answer_value('i_o_files/small_5_2'))
