import codecs
import re

import pydash


def read_html(path="test.html"):
    f = codecs.open(path, "r", "utf-8")
    s = f.readline()
    f.close()
    return pydash.join(s, "")


def get_css_link(html):
    search_result = re.search(r'<link re.*?css.*?href="(.*?svgtextcss.*?)">', html)
    css_link = search_result[1]
    return "http:%s" % css_link[0: pydash.index_of(css_link, '"')]


# html = read_html()
# print(get_css_link(html))
