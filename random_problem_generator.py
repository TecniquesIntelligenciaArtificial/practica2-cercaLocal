from random import randint


def random_problem_generator(D, U, N=100, M=100):
    users = []
    for idx in range(D + U):
        users.append(generate_user(idx, N, M))
    return users


def generate_user(idx, N, M):
    return tuple((idx, randint(0,N-1), randint(0,M-1), randint(0,N-1), randint(0,M-1)))


def generate_and_save_problem(D, U, file_name, N=100, M=100):
    users = random_problem_generator(D,U)
    file = open(file_name, 'w')
    file.write("%d %d %d %d \n" % (N, M, D, U))
    for u in users:
        for a in u:
            file.write("%d " % a)
        file.write("\n")
    file.close()


generate_and_save_problem(5, 2, 'i_o_files/small_5_2.in')
generate_and_save_problem(5, 7, 'i_o_files/small_5_7.in')
generate_and_save_problem(5, 15, 'i_o_files/small_5_15.in')

generate_and_save_problem(100, 50, 'i_o_files/small_100_50.in')
generate_and_save_problem(100, 150, 'i_o_files/small_100_150.in')
generate_and_save_problem(100, 300, 'i_o_files/small_100_300.in')

generate_and_save_problem(1000, 500, 'i_o_files/small_100_500.in')
generate_and_save_problem(1000, 1500, 'i_o_files/small_100_1500.in')
generate_and_save_problem(1000, 3000, 'i_o_files/small_100_3000.in')

