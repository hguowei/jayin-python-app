import codecs
import re
import os
import pydash
from lxml import etree

from utils import list_files, download, to_string

files = list_files(file_dir="htmls", suffix=".html")
print("files", len(files), files)


def read_html(path):
    f = codecs.open(path, "r", "utf-8")
    s = f.readline()
    f.close()
    return pydash.join(s, "")


def get_css_url(link_str):
    css_prefix = 'href="'
    idx = pydash.index_of(link_str, css_prefix)
    print("idx", idx)
    css_suffix = '.css"'
    css_idx = pydash.index_of(link_str, css_suffix)
    print("idx", css_idx)
    if idx >= 0 and css_idx >= 0:
        tmp_str = link_str[idx + len(css_prefix): css_idx + len(css_suffix) - 1]
        print("tmp_str", tmp_str)
        return "http:%s" % tmp_str
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
        print("link", link_str)
        css_link = get_css_url(link_str)
        if css_link is not None:
            css_links.append(css_link)

    return css_links


for file_path in files[:1]:
    file_path = "htmls/18766328.html"
    print("file_path", file_path)
    html = read_html(path=file_path)
    print("html", html)
    css_urls = get_css_links(html)
    print("css_url", css_urls)

    for css_url in css_urls:
        print("css_url", css_url)
        idx = pydash.last_index_of(css_url, "/")
        css_name = css_url[idx + 1:]
        css_path = "css/%s" % css_name
        print("css_path", css_path)

        if os.path.exists(css_path):
            continue
        css_html = download(css_url)
        # print("css_html", css_html)

        with open(css_path, 'wb') as f:
            f.write(css_html)
        exit()
