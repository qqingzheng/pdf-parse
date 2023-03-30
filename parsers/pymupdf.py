from .pdf_parser import PDFParser
import fitz
from .common_types import *
from operator import itemgetter
from itertools import groupby
from lxml import etree
import re
class PyMuPDF(PDFParser):
    def __init__(self, buf, depth=3):
        super().__init__(buf)
        self.pdf = fitz.open("pdf", buf)
        
        raw_content = ""
        for page in self.pdf:
            raw_content += page.get_text("html")
        with open("test.html", "w") as file:
            file.write(raw_content)
        self.__html_tree = etree.HTML(raw_content)
        self.__font_size_to_title = {}
        self.__root = Outline("Root", -1)
        self.__depth = depth
        self.__load_titles()
        self.__load_outline(self.__root)
        
        self.content = self.__get_content()
        # print(self.__root)
    def get_block_content_by_tries(self, titles):
        for title in titles:
            result = self.get_block_content(title)
            if result != "":
                return result
        return ""
    def __get_content(self):
        span_list = self.__html_tree.xpath('//span')
        content = ""
        for span in span_list:
            content +=span.text + " "
        return content
    def get_block_content(self, title):
        title1 = self.__root.search_title(title)
        title2 = self.__root.search_sibling_title(title1)
        span_list = self.__html_tree.xpath('//span')
        content = ""
        start = False
        for span in span_list:
            if re.match(f"{title1}", span.text, re.IGNORECASE):
                start = True
            elif title2 != "" and re.match(f"{title2}", span.text, re.IGNORECASE):
                break
            elif start:
                content +=span.text + " "
        return content
    def __load_titles(self):
        i = 0
        _span = self.__html_tree.xpath('//b/span')
        for span in _span:
            font_size = int(float(re.search(r"([\d\.]+?)pt", span.get("style")).group(1)))
            if font_size not in self.__font_size_to_title:
                self.__font_size_to_title[font_size] = []
            self.__font_size_to_title[font_size].append((i, span.text))
            i = i + 1
    def __load_outline(self, root: Outline, depth=0):
        if len(self.__font_size_to_title.keys()) <= depth or self.__depth == depth:
            return
        title_size = list(self.__font_size_to_title.keys())[depth]
        c = 0
        
        for i, title in self.__font_size_to_title[title_size]:
            next_sibling_value = self.__font_size_to_title[title_size][c+1][0] if c+1 < len(self.__font_size_to_title[title_size]) else 99
            if i > root.value and i < next_sibling_value:
                sub_node = Outline(title, i, root)
                self.__load_outline(sub_node, depth+1)
                root.add_sub_outline(sub_node)
            c = c + 1
    def get_meta(self):
        meta_data = MetaData(self.pdf.metadata['author'],
                             self.pdf.metadata['title'],
                             self.pdf.metadata['creationDate'],
                             self.pdf.metadata['keywords'],
                             self.pdf.metadata['subject'],
                             )
        return meta_data
    def get_outline(self):
        return self.__root
