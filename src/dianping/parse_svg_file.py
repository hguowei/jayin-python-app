import json
import xml.sax


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


if __name__ == "__main__":
    # 注：文件可能需要手动格式化一下，再解析。
    svg_file = "/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/svgs/f79fa764d791dca497ca2e3beb79c517.svg"
    svg_file = "/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/svgs/bf64761f6e0bca109d91f6e31dcd46ce.svg"
    path_dict_file = "%s.path_dict.json" % svg_file
    href_dict_file = "%s.href_dict.json" % svg_file
    import os

    if not os.path.exists(path_dict_file):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        handler = PathHandler()
        parser.setContentHandler(handler)

        parser.parse(svg_file)
        print("path_dict", handler.path_dict)
        with open(path_dict_file, "w") as f:
            json.dump(handler.path_dict, f)
        print("加载入文件完成...")

    if not os.path.exists(href_dict_file):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        handler2 = TextPathHandler()
        parser.setContentHandler(handler2)
        parser.parse(svg_file)
        print("href_dict", handler2.href_dict)
        with open(href_dict_file, "w") as f:
            json.dump(handler2.href_dict, f)
        print("加载入文件完成...")
