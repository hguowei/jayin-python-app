import datetime
import json
import os
import re

import pydash
import numpy as np

from class_utils import ClassDict
from parse_svg_file import get_path_dict, get_href_dict, get_text_dict
from utils import find_file, to_shorter_file_name


def get_one_svg_url(line):
    url_str = "url("
    url_index = pydash.index_of(line, url_str)
    if url_index >= 0:
        str_last = line[url_index + len(url_str):]
        right_idx = pydash.index_of(str_last, ")")
        if right_idx > 0:
            return str_last[:right_idx]
    return None


def get_svg_urls(line):
    print("line", line)
    url_str = "url("
    url_index = pydash.index_of(line, url_str)
    if url_index >= 0:
        str_last = line[url_index + len(url_str):]
        right_idx = pydash.index_of(str_last, ")")
        if right_idx > 0:
            last_results = get_svg_urls(str_last[right_idx + 1:])
            last_results.append("http:%s" % str_last[:right_idx])
            return last_results
        else:
            return get_svg_urls(str_last)
    return []


def get_local_css_file(css_file):
    if not os.path.exists(css_file):
        last_idx = pydash.last_index_of(css_file, "/")
        if last_idx >= 0:
            file_name = css_file[last_idx + 1:]
        else:
            file_name = css_file
        files = find_file(".", file_name)
        if files is None or len(files) == 0:
            print("Cannot found: ", css_file)
            return css_file
        else:
            css_file = files[0]
    return css_file


def read_css_file(css_file):
    if not os.path.exists(css_file):
        last_idx = pydash.last_index_of(css_file, "/")
        if last_idx >= 0:
            file_name = css_file[last_idx + 1:]
        else:
            file_name = css_file
        files = find_file(".", file_name)
        if files is None or len(files) == 0:
            print("Cannot found: ", css_file)
            return None, None
        else:
            css_file = files[0]

    f = open(css_file, "r")
    data = f.read()
    f.close()
    return css_file, data


def parse_data_to_dict(data):
    dlen = len(data)
    i = 0
    start = 0
    end = None
    end_brace = None
    tmp_dict = {}
    while i < dlen:
        cur_char = data[i]
        if cur_char == "." and end is None:
            start = i
            end = None
            end_brace = None
        elif cur_char == "{":
            end = i
            end_brace = None
        elif cur_char == "}":
            end_brace = i
            start = None

        if start is not None and end is not None:
            key = data[start + 1:end]
            start = None
        if end is not None and end_brace is not None:
            line = data[end:end_brace + 1]
            url_idx = pydash.index_of(line, "url(")
            if url_idx > 0:
                # tmp_str = line[url_idx:]
                # tmp_str = tmp_str[: pydash.index_of(tmp_str, ".svg") + 4]
                # print("a" * 10, tmp_str)
                # tmp_str = tmp_str[pydash.last_index_of(tmp_str, "/") + 1:]
                # print("a" * 10, tmp_str)
                # raise Exception("Sdxxxxx")
                #
                # print("url_idx > 0", url_idx, line[url_idx:])
                pass
            else:
                tmp = pydash.map_(re.findall(r'-?\d+\.?\d-*e?-?\d*?', line),
                                  lambda x: float(x))
                if key is not None:
                    tmp_dict[key] = tmp
                end = None
                end_brace = None
                key = None
        i += 1
    return tmp_dict


def get_css_class_dict(css_file):
    print("css_file1", css_file)
    css_file = get_local_css_file(css_file)
    print("css_file2", css_file)
    # class_dict_file = "%s.class_dict.json" % css_file
    class_dict_file = to_shorter_file_name(css_file, "class_dict.json")
    if os.path.exists(class_dict_file):
        with open(class_dict_file, 'r') as load_f:
            return json.load(load_f)

    class_to_word = {}

    css_file, data = read_css_file(css_file)
    if data is None:
        print("Cannot found css_file", css_file, "!")
        return {}
    svg_urls = get_svg_urls(data)

    # 保存或解析json文件
    idx = pydash.last_index_of(css_file, "/")
    if idx >= 0:
        file_name = css_file[idx + 1:]
    else:
        file_name = css_file

    print("file_name", file_name)
    new_file_name = pydash.replace(file_name, "_mod_easy-login", "")
    print("new_file_name", new_file_name)
    new_css_file = pydash.replace(css_file, file_name, new_file_name)
    encode_dict_file = "%s.encode_dict.json" % new_css_file
    if os.path.exists(encode_dict_file):
        with open(encode_dict_file, 'r') as load_f:
            encode_dict = json.load(load_f)
    else:
        encode_dict = parse_data_to_dict(data)
        print("len", len(encode_dict_file))
        with open(encode_dict_file, "w") as f:
            json.dump(encode_dict, f)

    # print("encode_dict =", encode_dict)

    # svg_urls, encode_dict = parse_css("css/1eb515893adcc915f7b5cb7d12b8772f.css")
    print("svg_urls", svg_urls)
    done_parse = False
    for url in svg_urls:
        if done_parse:
            break

        svg_file_name = url[pydash.last_index_of(url, "/") + 1:]
        data_path = "svgs/%s" % svg_file_name
        print("data_path", data_path)
        if os.path.exists(data_path) or find_file(".", svg_file_name):
            try:
                path_dict = get_path_dict(data_path)
                href_dict = get_href_dict(data_path)
                if pydash.is_empty(path_dict) or pydash.is_empty(href_dict):
                    path_dict, href_dict = get_text_dict(data_path)
            except Exception as e:
                print("Parse href_dict error!", e)
                continue
            # try:
            cd = ClassDict(path_dict, href_dict)
            for key, value in encode_dict.items():
                # encode_dict = {'pcq0rg': [-224.0, -969.0]}
                try:
                    word = cd.get_by_location(value[0], value[1])
                    print("key", key, ", word", word)
                    class_to_word[key] = word
                except:
                    print("unknown", key)
                    pass

            done_parse = True
            # except Exception as e:
            #     print("Exception", e)
            #     print("key", key)

            keys1 = list(encode_dict.keys())
            keys2 = list(class_to_word.keys())
            print("len(keys1)", len(keys1))
            print("len(keys2)", len(keys2))
            # print("unknown keys", pydash.difference(keys1, keys2))

            continue

    with open(class_dict_file, "w") as f:
        json.dump(class_to_word, f)

    return class_to_word


result = get_css_class_dict("css/1eb515893adcc915f7b5cb7d12b8772f.css")
