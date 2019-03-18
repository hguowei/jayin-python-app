import datetime
import json
import os
import re

import pydash
import numpy as np

from class_utils import ClassDict
from parse_svg_file import get_path_dict, get_href_dict
from utils import find_file


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
    # print("line", line)
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


def read_css_file(css_file):
    f = open(css_file, "r")
    data = f.read()
    f.close()
    return data


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

def parse_css(css_file):
    print("css_file", css_file)
    data = read_css_file(css_file)
    svg_urls = get_svg_urls(data)

    # 保存或解析json文件
    encode_dict_file = "%s.encode_dict.json" % css_file
    if os.path.exists(encode_dict_file):
        with open(encode_dict_file, 'r') as load_f:
            encode_dict = json.load(load_f)
    else:
        encode_dict = parse_data_to_dict(data)
        with open(encode_dict_file, "w") as f:
            json.dump(encode_dict, f)

    # print("encode_dict =", encode_dict)

    # svg_urls, encode_dict = parse_css("css/1eb515893adcc915f7b5cb7d12b8772f.css")
    print("svg_urls", svg_urls)
    class_to_word = {}
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
                    text_path(data_path)
                    print("EEEEMPTY")
                    continue
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
        print('ERROR找不到svg文件，请自己下载到svgs目录！[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=url))
        # data = download("http:%s" % url)
        # xxxx = pydash.starts_with(data, "<html")
        # print("XXXXX", xxxx)
        #
        # with open(data_path, 'wb') as f:
        #     f.write(data)
        # exit()

    # url(//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/552560215a8c8f609b7fb7bd1664070d.svg)

    encode_dict


result = parse_css("css/1eb515893adcc915f7b5cb7d12b8772f.css")
