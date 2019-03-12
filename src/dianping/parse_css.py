import datetime
import os
import re

import pydash


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
    data = read_css_file(css_file)
    svg_url = get_svg_urls(data)
    encode_dict = parse_data_to_dict(data)
    return svg_url, encode_dict


svg_urls, encode_dict = parse_css("css/1eb515893adcc915f7b5cb7d12b8772f.css")
print("xxx", encode_dict)
print("svg_urls", svg_urls)
for url in svg_urls:
    data_path = "svgs%s" % url[pydash.last_index_of(url, "/"):]
    # print("data_path", data_path)
    if os.path.exists(data_path):
        continue

    print('请自己下载到svgs目录！[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=url))

    # data = download("http:%s" % url)
    # xxxx = pydash.starts_with(data, "<html")
    # print("XXXXX", xxxx)
    #
    # with open(data_path, 'wb') as f:
    #     f.write(data)
    # exit()

# url(//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/552560215a8c8f609b7fb7bd1664070d.svg)