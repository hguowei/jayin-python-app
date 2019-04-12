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

import re

PATTERN_BACKGROUND = r'.(.*?){background:(.*?)px(.*?)px;}'
PATTERN_SPAN_CLASS = r'\[class\^="(.+?)"\]{width:(.+?)px;.+?url\((.+?)\)'
CSS_URL_PREFIX = 'http:'


def parse_shop_css(css):
    cls_dict = {}
    css_dict = {}
    backgrounds = re.findall(PATTERN_BACKGROUND, css)
    spans = re.findall(PATTERN_SPAN_CLASS, css)
    for i in spans:
        cls_dict.update({i[0]: [int(i[1].strip()), CSS_URL_PREFIX + i[2]]})
    for i in backgrounds:
        css_dict[i[0]] = {
            'x': -float(i[1].strip()),
            'y': -float(i[-1].strip()),
        }
    return cls_dict, css_dict


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
    print("css_file1", css_file)
    if pydash.includes(css_file, "_mod_mbox"):
        print("Do not deal with", css_file, "!")
        return {}, {}
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

    encode_dict = parse_data_to_dict(data)

    cls_dict, css_dict = parse_shop_css(data)
    print("cls_dict", cls_dict)
    print("css_dict", css_dict)

    for key_prefix, step_and_url in cls_dict.items():
        step = step_and_url[0]
        url = step_and_url[1]
        svg_file_name = url[pydash.last_index_of(url, "/") + 1:]
        # print("svg_file_name", svg_file_name)
        data_path = "svgs/%s" % svg_file_name
        if not os.path.exists(data_path):
            raise Exception("Need download", url, "to svgs/!")
        path_dict = get_path_dict(data_path)
        href_dict = get_href_dict(data_path)
        # print("path_dict", path_dict, pydash.is_empty(path_dict))
        if pydash.is_empty(path_dict) or pydash.is_empty(href_dict):
            path_dict, href_dict = get_text_dict(data_path)

        cd = ClassDict(path_dict, href_dict)
        for key, value in encode_dict.items():
            if not pydash.starts_with(key, key_prefix):
                pass
            try:
                word = cd.get_by_location(value[0], value[1])
                try:
                    class_to_int[key] = int(word)
                except:
                    class_to_word[key] = word
            except:
                pass

    with open(class_word_file, "w") as f:
        json.dump(class_to_word, f)
    with open(class_int_file, "w") as f:
        json.dump(class_to_int, f)

    return class_to_word, class_to_int


def parse_one_shop_css(html_path):
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
        # if pydash.includes(list(class_to_word.keys()), "jpcgck"):
        #     pass
        # if pydash.includes(list(class_to_word.keys()), "jpcgck"):
        #     pass
    return class_to_word_dict, class_to_int_dict


def parse_a_html(file_path):
    html = read_file(file_path)

    doc = etree.HTML(html)

    # TODO, error
    # shop_url = str(doc.xpath('//*[@id="qrcode"]/@title')[0])
    shop_url = str(doc.xpath("/html/head/link[7]/@href")[0])

    shop_id = shop_url[pydash.last_index_of(shop_url, "/") + 1:]

    class_to_word_dict, class_to_int_dict = parse_one_shop_css(file_path)
    print("class_to_word_dict")
    print(class_to_word_dict)
    print("class_to_int_dict")
    print(class_to_int_dict)

    data_list = []
    for comment_id, li in enumerate(doc.xpath('//*[@class="mod comment"]/ul/li')):
        # print("li", li)
        username = li.xpath('.//a[@class="name"]/text()')[0].strip('\n\r \t')
        user_href = li.xpath('.//a[@class="name"]/@href')[0]
        try:
            huiying_str = pydash.trim("".join(li.xpath('.//div/div/div/a[2]/text()')))
            huiying_num = int(huiying_str[pydash.index_of(huiying_str, "(") + 1: pydash.index_of(huiying_str, ")")])
        except:
            huiying_num = None

        try:
            zan_str = pydash.trim("".join(li.xpath('.//div/div/div/a[1]/text()')))
            zan_num = int(zan_str[pydash.index_of(zan_str, "(") + 1: pydash.index_of(zan_str, ")")])
        except:
            zan_num = None

        try:
            pic_num = len(li.xpath('.//div/div[3]/div[1]/a'))
        except:
            pic_num = None
        try:
            tmp_src = str(li.xpath('.//p/img/@src')[0])
            pre = "squarelv"
            end = ".png"
            pre_idx = pydash.index_of(tmp_src, pre)
            end_idx = pydash.index_of(tmp_src, end)
            user_level = int(tmp_src[pre_idx + len(pre): end_idx])
        except:
            user_level = None
        try:
            star = li.xpath('.//span[contains(./@class, "sml-rank-stars")]/@class')[0]
            # print("star1", star)
            star = re.search(r'sml-str(\d+)', star).group(1)
            print("star", star)
        except IndexError:
            star = 0
        time = li.xpath('.//span[@class="time"]/text()')[0].strip('\n\r \t')
        # test = li.xpath('.//p[@class="desc J-desc"]/text()')
        # comment = pydash.join(test, "")
        # print("comment=")
        # print(comment)
        test = li.xpath('.//p[@class="desc J-desc"]')
        print("test", type(test), test)
        for comment_elem in test:
            # just one comment.
            print("comment_elem", type(comment_elem), comment_elem)
            comment = to_string(comment_elem)

            for class_name in re.findall(r'<b class="([a-zA-Z0-9]{5,6})"/>', comment):
                try:
                    origin_string = '<b class="%s"/>' % class_name
                    word = class_to_word_dict[class_name]
                    print("class_name", class_name, "word", word, origin_string)
                    print("comment", comment)
                    comment = pydash.replace(comment, origin_string, word)
                except Exception as e:
                    # raise e
                    pass

            print("comment=")
            print(comment)

        dr = re.compile(r'<[^>]+>', re.S)
        comment = dr.sub('', comment)
        comment = pydash.trim_end(comment)

        score = ' '.join(map(lambda s: s.strip('\n\r \t'), li.xpath('.//span[@class="score"]//text()')))

        data = {
            'shop_id': shop_id,
            'shop_url': shop_url,
            'comment_id': comment_id,
            'username': username,
            "user_level": user_level,
            "user_href": user_href,
            'comment': comment,
            'star': star,
            'score': score,
            'time': time,
            "pic_num": pic_num,
            "zan_num": zan_num,
            "huiying_num": huiying_num,
        }
        data_list.append(data)
        print("data", data)
        return shop_id, data_list


def parse_all_html():
    files = list_files(file_dir="htmls")

    shop_path = "results/shop_comments.csv"

    all_data_list = []
    for file_path in files:
        print("file_path", file_path)
        shop_id, data_list = parse_a_html(file_path)

        all_data_list.extend(data_list)
        data = pd.DataFrame(data_list)
        print("data", len(data))
        data.to_csv("results/shop_%s.csv" % shop_id, index=False, encoding='utf_8_sig')

    # end for
    shops_comment_df = pd.DataFrame(all_data_list)
    shops_comment_df.to_csv(shop_path, index=False, encoding='utf_8_sig')


# parse_all_html()
parse_a_html(
    file_path="/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/htmls/【蘩楼(华强北店)】电话,地址,价格,营业时间(图) - 深圳美食 - 大众点评网.html")
