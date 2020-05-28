import os
import sys
from math import hypot


def get_distance(source, dest) -> float:
    return hypot(dest[0] - source[0], dest[1] - source[1])


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(".."), relative_path).replace("\\", '/')
