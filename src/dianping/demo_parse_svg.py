import pydash
import numpy as np
from lxml import etree

from parse_svg_file import get_text_dict
from utils import read_file, to_string

path_dict = {"2": "M0 72 H600"}
href_dict = {"#1": "你好"}


svg_file = "svgs/ac09bd813a3a57b29cb303da390fd501.svg"
svg_file = "svgs/f8350660159e938ca81d948ca9d0d555.svg"
path_dict, href_dict = get_text_dict(svg_file)

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
    print("line_id", line_id)

    line_string = href_dict[line_id]
    print("line_string", line_string)

    word_index = int(x / 14)
    print("word_index", word_index)

    return line_string[word_index]


result = get_by_location(-22, -141)
print("result", result)

result = get_by_location(-246, -141)
print("result", result)
