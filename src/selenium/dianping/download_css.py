import codecs
import os

import pydash
from lxml import etree


def read_file(path):
    f = open(path)
    s = f.read()
    f.close()
    return s


def to_string(element):
    return etree.tostring(element, encoding="utf-8", pretty_print=True)[:-1].decode("utf-8")


def get_css_url(link_str):
    css_prefix = 'href="'
    idx = pydash.index_of(link_str, css_prefix)
    # print("idx", idx)
    css_suffix = '.css"'
    css_idx = pydash.index_of(link_str, css_suffix)
    # print("idx", css_idx)
    if idx >= 0 and css_idx >= 0:
        tmp_str = link_str[idx + len(css_prefix): css_idx + len(css_suffix) - 1]
        return tmp_str
    return None


# link_str = '<link rel="stylesheet" type="text/css" href="//www.dpfile.com/app/pc-common/index.min.30301999a81455aaf8a16973b3b13888.css"/> '
# link = link_str
# print(get_css_url(link))
# exit()


def get_css_links(html):
    # xpath
    doc = etree.HTML(html)
    print("doc", doc)
    css_links = []
    for link in doc.xpath('//link'):
        link_str = to_string(link)
        # print("link", link_str)
        css_link = get_css_url(link_str)
        if css_link is not None:
            css_links.append(css_link)

    return css_links


def split_file_path(file_path, sep="."):
    idx = pydash.last_index_of(file_path, sep)
    if idx > 0:
        return file_path[:idx], file_path[idx + 1:]
    return "", file_path


def split_css_path(file_path):
    idx = pydash.index_of(file_path, "/")
    if idx > 0:
        return file_path[:idx], file_path[idx + 1:]
    return "", file_path


def parse_a_html(file_path):
    # file_path = "htmls/18766328.html"
    print("file_path", file_path)
    # html = read_html(path=file_path)
    dir, _ = split_file_path(file_path)
    dir = "%s_files/" % dir
    print("dir", dir)
    html = read_file(file_path)
    # print("html", html)
    css_urls = get_css_links(html)
    print("css_urls", len(css_urls))

    for css_url in css_urls:
        print("css_url", css_url)
        pp = "/Users/huang/Downloads/%s" % css_url
        print("pp", pp, os.path.exists(pp))
        _, filename = split_file_path(css_url, "/")
        print("filename", filename)

        full_path = "%s%s" % (dir, filename)
        print("full_path", full_path)

        if os.path.exists(full_path):
            continue
        print("Not exists!")


if __name__ == '__main__':
    file_path = "/Users/huang/Downloads/深圳聚餐相关搜索结果推荐-大众点评网.html"
    parse_a_html(file_path)
