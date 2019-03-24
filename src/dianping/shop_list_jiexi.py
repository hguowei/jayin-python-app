import json
import os
import re

import numpy as np
import pandas as pd
import pydash
from lxml import etree

# 目前餐馆列表是手动将页面ctrl+s保存的。
from class_utils import ClassDict
from parse_svg_file import get_path_dict, get_href_dict, get_text_dict


def list_files(file_dir, suffix=".html"):
    result_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == suffix:
                result_list.append(os.path.join(root, file))
    return result_list


def read_file(path):
    f = open(path)
    s = f.read()
    f.close()
    return s


def to_string(element):
    return etree.tostring(element, encoding="utf-8", pretty_print=True)[:-1].decode("utf-8")


def to_shorter_file_name(css_file, surfix):
    idx = pydash.last_index_of(css_file, "/")
    if idx >= 0:
        file_name = css_file[idx + 1:]
    else:
        file_name = css_file

    # print("file_name", len(file_name))
    # print("file_name = '%s'" % file_name)
    new_file_name = pydash.replace(file_name, "_mod_easy-login", "")
    # print("new_file_name", new_file_name)
    new_css_file = pydash.replace(css_file, file_name, new_file_name)
    return "%s.%s" % (new_css_file, surfix)


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


def get_svg_urls(line):
    # print("line", line)
    url_str = "url("
    url_index = pydash.index_of(line, url_str)
    if url_index >= 0:
        str_last = line[url_index + len(url_str):]
        right_idx = pydash.index_of(str_last, ")")
        if right_idx > 0:
            last_results = get_svg_urls(str_last[right_idx + 1:])
            new_svg_url = "http:%s" % str_last[:right_idx]
            if pydash.ends_with(new_svg_url, ".svg"):
                last_results.append(new_svg_url)
            return last_results
        else:
            return get_svg_urls(str_last)
    return []


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
                # print(re.findall(r'-?\d+\.?\d-*e?-?\d*?', line))
                tmp = pydash.map_(re.findall(r'-?\d+\.?\d-*e?-?\d*?', line),
                                  lambda x: float(x))
                if key is not None:
                    tmp_dict[key] = tmp
                end = None
                end_brace = None
                key = None
        i += 1
    return tmp_dict


testing = True


def parse_a_css(css_file):
    # css_file = "shop_lists/深圳聚餐相关搜索结果推荐-大众点评网2_files/47463da64cdc885b913e5f736f27f2c0.css"
    print("css_file1", css_file)
    class_word_file = to_shorter_file_name(css_file, "word_dict.json")
    class_int_file = to_shorter_file_name(css_file, "int_dict.json")
    if os.path.exists(class_word_file) and os.path.exists(class_int_file):
        with open(class_word_file, 'r') as load_f:
            class_to_word = json.load(load_f)
        with open(class_int_file, 'r') as load_f:
            class_to_int = json.load(load_f)
            return class_to_word, class_to_int

    class_to_word = {}
    class_to_int = {}

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

    if len(file_name) == 255:
        return class_to_word, class_to_int

    # new_file_name = pydash.replace(file_name, "_mod_easy-login", "")
    # print("new_file_name", new_file_name)

    encode_dict = parse_data_to_dict(data)
    print("len(encode_dict)", len(encode_dict))

    print("svg_urls", svg_urls)
    done_parse = False
    for url in svg_urls:
        if done_parse:
            break

        svg_file_name = url[pydash.last_index_of(url, "/") + 1:]
        # print("svg_file_name", svg_file_name)
        data_path = "svgs/%s" % svg_file_name

        path_dict = get_path_dict(data_path)
        href_dict = get_href_dict(data_path)
        # print("path_dict", path_dict, pydash.is_empty(path_dict))
        if pydash.is_empty(path_dict) or pydash.is_empty(href_dict):
            path_dict, href_dict = get_text_dict(data_path)

        cd = ClassDict(path_dict, href_dict)
        for key, value in encode_dict.items():
            # encode_dict = {'pcq0rg': [-224.0, -969.0]}
            try:
                word = cd.get_by_location(value[0], value[1])
                # print("key", key, ", word", word, pydash.includes(list(class_to_int.keys()), key))
                if pydash.includes(list(class_to_int.keys()), key) and \
                        not pydash.is_equal(key, str(class_to_int[key])):
                    raise Exception("key", key, "word", word, "class", class_to_int[key])
                if pydash.includes(list(class_to_word.keys()), key) and \
                        not pydash.is_equal(key, str(class_to_word[key])):
                    raise Exception("key", key, "word", word, "class", class_to_word[key])
                try:
                    class_to_int[key] = int(word)
                except:
                    class_to_word[key] = word
            except:
                # print("unknown", key)
                pass

        keys1 = list(encode_dict.keys())
        keys2 = list(class_to_word.keys())
        keys3 = list(class_to_int.keys())
        diff = pydash.difference(keys1, keys2)
        diff2 = pydash.difference(diff, keys3)
        print("len(keys1)", len(keys1))
        print("len(keys2)", len(keys2))
        print("unknown keys", len(diff))
        print("unknown keys", len(diff2))
        if len(diff2) == 0:
            done_parse = True

        continue

    with open(class_word_file, "w") as f:
        json.dump(class_to_word, f)
    with open(class_int_file, "w") as f:
        json.dump(class_to_int, f)

    return class_to_word, class_to_int


def parse_shop_list_css(html_path):
    html_dir = "%s_files" % html_path[:-5]
    print("html_dir", html_dir)
    css_files = list_files(html_dir, ".css")
    print("css_files", len(css_files), css_files)
    class_to_word_dict = {}
    class_to_int_dict = {}
    for css_file in css_files:
        class_to_word, class_to_int = parse_a_css(css_file)
        class_to_word_dict.update(class_to_word)
        class_to_int_dict.update(class_to_int)
    return class_to_word_dict, class_to_int_dict


def parse_all_html():
    files = list_files(file_dir="shop_lists")

    shop_list_path = "results/shop_list.csv"
    shop_df = None
    shop_ids = []
    if os.path.exists(shop_list_path):
        shop_df = pd.read_csv(shop_list_path)
        shop_ids = shop_df["shop_id"].tolist()

    for file_path in files:
        print("file_path", file_path)
        class_to_word_dict, class_to_int_dict = parse_shop_list_css(file_path)

        html = read_file(file_path)

        doc = etree.HTML(html)

        # pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        pattern = re.compile(
            r'http://www.dianping.com/shop/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式

        urls = []
        stars_dict = []

        for ul in doc.xpath('//*[@id="shop-all-list"]/ul/li'):
            # print("ul", to_string(ul))
            for kouwei_elem in ul.xpath('//li[4]/div[2]/span/span[1]'):
                kouwei = to_string(kouwei_elem)
                # print("kouwei", kouwei)
                for class_name in re.findall(r'<span class="([a-zA-Z0-9]{5,6})"/>', kouwei):
                    origin_string = '<span class="%s"/>' % class_name
                    meaning = class_to_int_dict[class_name]
                    # print("class_name", class_name, "meaning", meaning, origin_string)
                    kouwei = pydash.replace(kouwei, origin_string, meaning)
                kouwei = float(".".join(re.findall("\d+", kouwei)))

            for huanjing_elem in ul.xpath('//li[4]/div[2]/span/span[2]'):
                huanjing = to_string(huanjing_elem)
                # print("huanjing", huanjing)
                for class_name in re.findall(r'<span class="([a-zA-Z0-9]{5,6})"/>', huanjing):
                    origin_string = '<span class="%s"/>' % class_name
                    meaning = class_to_int_dict[class_name]
                    # print("class_name", class_name, "meaning", meaning, origin_string)
                    huanjing = pydash.replace(huanjing, origin_string, meaning)
                huanjing = float(".".join(re.findall("\d+", huanjing)))
            for fuwu_elem in ul.xpath('//li[4]/div[2]/span/span[3]'):
                fuwu = to_string(fuwu_elem)
                # print("fuwu", fuwu)
                for class_name in re.findall(r'<span class="([a-zA-Z0-9]{5,6})"/>', fuwu):
                    origin_string = '<span class="%s"/>' % class_name
                    meaning = class_to_int_dict[class_name]
                    # print("class_name", class_name, "meaning", meaning, origin_string)
                    fuwu = pydash.replace(fuwu, origin_string, meaning)
                fuwu = float(".".join(re.findall("\d+", fuwu)))

            for span in ul.xpath('//li[*]/div[2]/div[2]/span'):
                star = re.search(r'sml-str(\d+)', to_string(span)).group(1)

            stars_dict.append({
                "kouwei": kouwei,
                "huanjing": huanjing,
                "fuwu": fuwu,
                "star": star
            })

            # for li in doc.xpath('//*[@id="shop-all-list"]/ul/li[*]/div[2]/div[1]/a'):
            for li in ul.xpath('//li[*]/div[2]/div[1]/a'):
                tmp_string = to_string(li)
                # print("tmp_string", tmp_string)
                tmp_urls = re.findall(pattern, tmp_string)
                # print("tmp_urls", tmp_urls)
                urls.extend(tmp_urls)

        print("urls", len(stars_dict), stars_dict)
        print("urls", len(urls), urls)

        is_pass_exists = False

        def parse_url(kv):
            url = kv[0]
            star_dict = kv[1]
            idx = pydash.last_index_of(url, "/")
            shop_id = url[idx + 1:]
            try:
                shop_id = int(shop_id)
                if is_pass_exists and pydash.includes(shop_ids, shop_id):
                    return []
                else:
                    shop_ids.append(shop_id)
                print("shop_id", shop_id)

                star_dict.update({
                    "shop_id": shop_id,
                    "shop_url": "http://www.dianping.com/shop/%s" % shop_id})
                return [star_dict]
            except:
                return []

        tmp_dict = pydash.chain(urls).zip(stars_dict).map(parse_url).flatten().value()
        print("tmp_dict", tmp_dict)

        data = pd.DataFrame(tmp_dict)
        print("data", len(data))

        if data.empty:
            pass
        elif shop_df is None:
            shop_df = data
        else:
            shop_df = shop_df.append(data)

    print("size", shop_df.size)
    if shop_df is not None:
        shop_df.to_csv(shop_list_path, index=False)


parse_all_html()
