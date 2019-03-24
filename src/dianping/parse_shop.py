# encoding: utf-8
import re

from lxml import etree
import pydash
from download_css import get_css_links
from utils import read_file, to_string


def parse_comment_page(doc, css_urls):
    """
        解析评论页并提取数据
    """
    tmp_class_dict = {}

    def get_class_dict(css_url):
        tmp_class_dict_keys = list(tmp_class_dict.keys())
        if pydash.includes(tmp_class_dict_keys, css_url):
            return tmp_class_dict[css_url]
        else:
            class_dict = get_css_class_dict(css_url)
            tmp_class_dict[css_url] = class_dict
            return class_dict

    def get_class_means(class_name):
        for css_url in css_urls:
            print("css_url", css_url)
            class_dict = get_class_dict(css_url)
            if pydash.includes(list(class_dict.keys()), class_name):
                return class_dict[class_name]
        return None

    datas = []
    for li in doc.xpath('//*[@class="mod comment"]/ul/li'):
        print("li", li)
        name = li.xpath('.//a[@class="name"]/text()')[0].strip('\n\r \t')
        try:
            star = li.xpath('.//span[contains(./@class, "sml-rank-stars")]/@class')[0]
            print("star1", star)
            star = re.search(r'sml-str(\d+)', star).group(1)
            print("star2", star)
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

            class_set = set()
            # <b class="([a-zA-Z0-9]{5,6})"/>
            for class_name in re.findall(r'<b class="([a-zA-Z0-9]{5,6})"/>', comment):
                origin_string = '<b class="%s"/>' % class_name
                meaning = get_class_means(class_name)
                print("class_name", class_name, "meaning", meaning, origin_string)
                print("comment", comment)
                comment = pydash.replace(comment, origin_string, get_class_means(class_name))

                class_set.add(class_name)

            print("comment=")
            print(comment)

        score = ' '.join(map(lambda s: s.strip('\n\r \t'), li.xpath('.//span[@class="score"]//text()')))

        data = {
            'name': name,
            'comment': comment,
            'star': star,
            'score': score,
            'time': time,
        }
        datas.append(data)
        print("data", data)
        exit()

    return datas


def parse_one_html(file_path):
    html = read_file(file_path)

    css_urls = get_css_links(html)
    print("css_url", css_urls)

    doc = etree.HTML(html)
    result = parse_comment_page(doc, css_urls)
    print("result", result)


file_path = "htmls/【蔡澜港式点心(海岸城店)】电话,地址,价格,营业时间(图) - 深圳美食 - 大众点评网.html"
parse_one_html(file_path)
