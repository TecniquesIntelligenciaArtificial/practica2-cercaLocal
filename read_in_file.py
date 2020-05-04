def parse_in(in_file):
    with open(in_file, 'r') as file:
        N, M, D, U = [int(x) for x in file.readline().split()]
        drivers = []
        for n in range(D):
            drivers.append(parse_user(file.readline()))
        users = []
        for n in range(U):
            users.append(parse_user(file.readline()))
    return N, M, D, U, drivers, users


def parse_user(line):
    idx, ox, oy, dx, dy = [int(x) for x in line.split()]
    return tuple((idx, (ox, oy), (dx, dy)))

