def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def manhattan_distance(o, d):
    ox, oy = o
    dx, dy = d
    return abs(ox-dx)+abs(oy-dy)

