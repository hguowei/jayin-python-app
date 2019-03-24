import pydash
import numpy as np

from parse_svg_file import get_path_dict, get_href_dict, get_text_dict
from utils import list_files, find_file

all_css_files = list_files(file_dir="css", suffix=".css")
print("files", len(all_css_files), all_css_files)

all_css_files = find_file(file_dir=".", suffix=".css")
print("files", len(all_css_files), all_css_files)


class ClassDict(object):

    def __init__(self, path_dict, href_dict):
        self.path_dict = path_dict
        self.href_dict = href_dict

        # path_dict = {"2": "M0 72 H600"}
        # href_dict = {"#1": "你好"}

        path_list = list(path_dict.items())

        def map_func(kv):
            tmp_list = pydash.split(kv[1], " ")
            try:
                step = int(tmp_list[2])
            except:
                step = 14
            return int(kv[0]), (int(tmp_list[1]), step)

        path_list = pydash.map_(path_list, map_func)
        path_list = pydash.sort_by(path_list, lambda kv: kv[0])

        self.path_list = path_list

    def get_line_id(self, y):
        y = np.abs(y)
        step = 14
        for line_id, kv in self.path_list:
            line_y, step = kv
            step = np.abs(step)
            if y < line_y:
                return line_id, step
        return self.path_list[-1][0], step

    def get_by_location(self, x, y):
        x = np.abs(x)
        kv = self.get_line_id(y)
        line_id = "#%d" % kv[0]
        line_string = self.href_dict[line_id]
        word_index = int(x / kv[1])

        try:
            line_string[word_index]
        except:
            pass
        return line_string[word_index]

    def get_by_location_str(self, tmp_str):
        tmp_str = pydash.replace(tmp_str, "px", "")
        tmp_list = pydash.split(tmp_str, " ")
        return self.get_by_location(float(tmp_list[0]), float(tmp_list[1]))

    def test(self):
        result = self.get_by_location(-490, -2101)
        print("result", result)


def get_svg_ClassDict(
        data_path="/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/svgs/0f9f119c6827b4fae4c85ca34c56cbda.svg"):
    path_dict = get_path_dict(data_path)
    href_dict = get_href_dict(data_path)
    print("path_dict", path_dict, pydash.is_empty(path_dict))
    if pydash.is_empty(path_dict) or pydash.is_empty(href_dict):
        path_dict, href_dict = get_text_dict(data_path)
    return ClassDict(path_dict, href_dict)


if __name__ == '__main__':
    cd = get_svg_ClassDict()
    # result = cd.get_by_location_str("-523.0px -42.0px")
    result = cd.get_by_location_str("-55.0px -81.0px")
    print("result", result)
