from math import hypot


def get_distance(source, dest) -> float:
    return hypot(dest[0] - source[0], dest[1] - source[1])
