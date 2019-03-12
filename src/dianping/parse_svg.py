import pydash
import numpy as np
from lxml import etree

from utils import read_file, to_string

path_dict = {"2": "M0 72 H600"}
href_dict = {"#1": "你好"}

path_list = list(path_dict.items())


def map_func(kv):
    return int(kv[0]), int(pydash.split(kv[1], " ")[1])


path_list = pydash.map_(path_list, map_func)
path_list = pydash.sort_by(path_list, lambda kv: kv[0])


def get_line_id(y):
    y = np.abs(y)
    for line_id, line_y in path_list:
        if y < line_y:
            return line_id
    return path_list[-1][0]


def get_by_location(x, y):
    x = np.abs(x)
    line_id = "#%d" % get_line_id(y)
    line_string = href_dict[line_id]
    word_index = int(x / 14)
    return line_string[word_index]


result = get_by_location(-490, -2101)
print("result", result)
