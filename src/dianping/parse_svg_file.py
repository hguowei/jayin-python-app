import json
import os
import xml.sax
import pydash


class PathHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.type = ""
        self.path_dict = {}

    def startElement(self, tag, attributes):
        self.current_data = tag

        if tag == "path":
            print("*" * 10, "path", "*" * 10)
            id = attributes["id"]
            d = attributes["d"]
            self.path_dict[id] = d

    def endElement(self, tag):
        if self.current_data == "path":
            print("Type:", self.type)
        self.current_data = ""

    def characters(self, content):
        if self.current_data == "type":
            self.type = content


class TextPathHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.href = ""
        self.data = ""
        self.href_dict = {}

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "textPath":
            print("*" * 10, "textPath", "*" * 10)
            self.href = attributes["xlink:href"]

    def endElement(self, tag):
        if self.current_data == "textPath":
            print("Type:", self.href)
        self.current_data = ""

    def characters(self, content):
        if self.current_data == "textPath":
            self.data = content
            self.href_dict[self.href] = self.data


class TextHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.x = ""
        self.y = ""
        self.data = ""
        self.path_dict = {}
        self.href_dict = {}

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "text":
            print("*" * 10, "text", "*" * 10)
            self.x = attributes["x"]
            self.y = attributes["y"]

    def endElement(self, tag):
        if self.current_data == "text":
            print("Type:", self.data)
        self.current_data = ""

    def characters(self, content):
        if self.current_data == "text":
            self.data = content
            href_key = "#%s" % self.y
            path_key = "%s" % self.y
            self.href_dict[href_key] = self.data
            tmp_list = pydash.split(self.x, " ")
            self.path_dict[path_key] = "M0 %s %d" % (self.y, int(tmp_list[2]) - int(tmp_list[1]))


def get_path_dict(svg_file):
    print("svg_file", svg_file)
    path_dict_file = "%s.path_dict.json" % svg_file

    if not os.path.exists(path_dict_file):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        handler = PathHandler()
        parser.setContentHandler(handler)

        parser.parse(svg_file)
        print("path_dict", handler.path_dict)
        if not pydash.is_empty(handler.path_dict):
            with open(path_dict_file, "w") as f:
                json.dump(handler.path_dict, f)
        print("加载入文件完成...")

        return handler.path_dict
    else:
        with open(path_dict_file, 'r') as load_f:
            return json.load(load_f)


def get_href_dict(svg_file):
    href_dict_file = "%s.href_dict.json" % svg_file
    if not os.path.exists(href_dict_file):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        handler = TextPathHandler()
        parser.setContentHandler(handler)
        parser.parse(svg_file)
        print("href_dict", handler.href_dict)
        if not pydash.is_empty(handler.href_dict):
            with open(href_dict_file, "w") as f:
                json.dump(handler.href_dict, f)
            print("加载入文件完成...")
        return handler.href_dict
    else:
        with open(href_dict_file, 'r') as load_f:
            return json.load(load_f)


def get_text_dict(svg_file):
    testing = False
    href_dict_file = "%s.href_dict.json" % svg_file
    path_dict_file = "%s.path_dict.json" % svg_file
    href_dict = {}
    path_dict = {}

    if os.path.exists(href_dict_file):
        with open(href_dict_file, 'r') as load_f:
            href_dict = json.load(load_f)
    if os.path.exists(path_dict_file):
        with open(path_dict_file, 'r') as load_f:
            path_dict = json.load(load_f)
    if pydash.is_empty(href_dict) or pydash.is_empty(path_dict):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        handler = TextHandler()
        parser.setContentHandler(handler)
        parser.parse(svg_file)
        href_dict = handler.href_dict
        path_dict = handler.path_dict
        with open(href_dict_file, "w") as f:
            json.dump(href_dict, f)
        with open(path_dict_file, "w") as f:
            json.dump(path_dict, f)
        print("加载入文件完成...")

    return path_dict, href_dict


def parse_text():
    print("TODO parse_text", parse_text)
    pass


if __name__ == "__main__":
    # 注：文件可能需要手动格式化一下，再解析。
    svg_file = "/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/svgs/f79fa764d791dca497ca2e3beb79c517.svg"
    svg_file = "/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/svgs/bf64761f6e0bca109d91f6e31dcd46ce.svg"

    # svg_file = "svgs/2e429b51c0d6dbda8229f44bd237a090.svg"
    # get_href_dict(svg_file)
    # get_path_dict(svg_file)

    svg_file = "svgs/ac09bd813a3a57b29cb303da390fd501.svg"
    svg_file = "svgs/f8350660159e938ca81d948ca9d0d555.svg"
    get_text_dict(svg_file)
