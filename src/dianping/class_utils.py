import pydash
import numpy as np
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
            return int(kv[0]), int(pydash.split(kv[1], " ")[1])

        path_list = pydash.map_(path_list, map_func)
        path_list = pydash.sort_by(path_list, lambda kv: kv[0])

        self.path_list = path_list

    def get_line_id(self, y):
        y = np.abs(y)
        for line_id, line_y in self.path_list:
            if y < line_y:
                return line_id
        return self.path_list[-1][0]

    def get_by_location(self, x, y):
        x = np.abs(x)
        line_id = "#%d" % self.get_line_id(y)
        line_string = self.href_dict[line_id]
        word_index = int(x / 14)

        try:
            line_string[word_index]
        except:
            pass
        return line_string[word_index]

    def test(self):
        result = self.get_by_location(-490, -2101)
        print("result", result)


def get_meaning(css_class):
    pass
