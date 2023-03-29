from .pdf_parser import PDFParser
import fitz
from .common_types import *
from operator import itemgetter
from itertools import groupby
from lxml import etree
import re
class PyMuPDF(PDFParser):
    def __init__(self, buf, depth=5):
        super().__init__(buf)
        self.pdf = fitz.open("pdf", buf)
        self.content = ""
        html_content = ""
        for page in self.pdf:
            html_content += page.get_text("html")
            self.content += page.get_text("text")
        self.html_tree = etree.HTML(html_content)
        self.font_size_to_title = {}
        self.root = Outline("Root", -1)
        self.depth = depth
        self.__load_titles()
        self.__get_outline(self.root)
    def get_block_content_by_tries(self, titles):
        for title in titles:
            result = self.get_block_content(title)
            if result != "":
                return result
        return ""
    def get_block_content(self, title):
        title1 = title
        title2 = self.root.search_sibling_title(self.root, title)
        _span = self.html_tree.xpath('//span')
        content = ""
        start = False
        for span in _span:
            if re.match(f"{title1}", span.text, re.IGNORECASE):
                start = True
            elif re.match(f"{title2}", span.text, re.IGNORECASE):
                break
            elif start:
                content += span.text
        return content
    def __load_titles(self):
        i = 0
        _span = self.html_tree.xpath('//b/span')
        for span in _span:
            font_size = float(re.search(r"([\d\.]+?)pt", span.get("style")).group(1))
            if font_size not in self.font_size_to_title:
                self.font_size_to_title[font_size] = []
            self.font_size_to_title[font_size].append((i, span.text))
            i = i + 1
    def __get_outline(self, root: Outline, sibling_value=99, depth=0):
        if len(self.font_size_to_title.keys()) <= depth or self.depth == depth:
            return
        title_size = list(self.font_size_to_title.keys())[depth]
        c = 0
        for i, title in self.font_size_to_title[title_size]:
            next_sibling_value = self.font_size_to_title[title_size][c+1][0] if c+1 < len(self.font_size_to_title[title_size]) else 99
            if i > root.value and i < sibling_value:
                sub_node = Outline(title, i)
                self.__get_outline(sub_node, next_sibling_value, depth+1)
                root.add_sub_outline(sub_node)
            c = c + 1
    def get_meta(self):
        """
        Keys: ['format', 'title', 'author', 'subject', 
               'keywords', 'creator', 'producer', 'creationDate',
               'modDate', 'trapped', 'encryption']
        """
        meta_data = MetaData(self.pdf.metadata['author'],
                             self.pdf.metadata['title'],
                             self.pdf.metadata['creationDate'],
                             self.pdf.metadata['keywords'],
                             self.pdf.metadata['subject'],
                             )
        return meta_data
    def get_catagory(self):
        self.root = Outline("Root", 0)
        toc = self.pdf.get_toc()
        depth_ptr = dict()
        depth_ptr[0] = self.root
        for outline in toc:
            o = Outline(outline[1], outline[2])
            depth_ptr[outline[0]] = o
            depth_ptr[outline[0]-1].add_sub_outline(o)
        return self.root
