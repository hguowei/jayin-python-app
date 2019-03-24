import pydash

from class_utils import ClassDict
from parse_svg_file import get_path_dict, get_href_dict


def class_demo():
    class_dict = {
        "qqfww8": [-276.0, -1441.0]
    }

    data_path = "/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/svgs/0f9f119c6827b4fae4c85ca34c56cbda.svg"
    path_dict = get_path_dict(data_path)
    href_dict = get_href_dict(data_path)
    cd = ClassDict(path_dict, href_dict)

    value = class_dict["qqfww8"]
    word = cd.get_by_location(value[0], value[1])
    print("word", word)


def test_update():
    dict1 = {"a": "a"}
    dict2 = {"b": "b"}
    all_dict = {}
    all_dict.update(dict1)
    print("all", all_dict)
    all_dict.update(dict2)
    print("all", all_dict)


tmp_list = "59677961432346524602"
value = 523 / 12