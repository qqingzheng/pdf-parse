from .pdf_parser import PDFParser
import fitz
from .common_types import *
from operator import itemgetter
from itertools import groupby
import re
class PyMuPDF(PDFParser):
    def __init__(self, buf):
        super().__init__(buf)
        self.pdf = fitz.open("pdf", buf)
        self.content = ""
        for page in self.pdf:
            self.content += page.get_text("text")
        # with open("test.html", "w") as file:
        #     file.write(self.content)
        self.blocks = {}
        self.__load_blocks()
    def get_block_content(self, name):
        for title, content in self.blocks.items():
            if re.search(f"{name}", title, re.IGNORECASE):
                return content
        return ""
    def __load_blocks(self):
        self.blocks  = {}
        now_block = "Others"
        self.blocks [now_block] = ""
        for page in self.pdf:
            blocks = page.get_text("blocks", sort=False)
            # print(blocks)
            for block in blocks:
                content = block[4]
                if re.match(r"[0-9A-Z][\s\S]*[a-zA-Z]{4}[\s\S]*", content) and len(content) < 30 and len(content) > 2: 
                    now_block = content
                    self.blocks[now_block] = ""
                else:
                    self.blocks[now_block] += " " + content
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
    def get_content_from_title(self, title1, title2):
        """
        return text between title1 and title2
        """
        page_id1 = self.root.search(title1)
        page1 = self.pdf.load_page(page_id1-1)
        search1 = page1.search_for(title1, hit_max=1)
        rect1 = search1[0]
        top = rect1.y1
        page_id2 = self.root.search(title2)
        page2 = self.pdf.load_page(page_id2-1)
        search2 = page2.search_for(title2, hit_max=1)
        rect2 = search2[0]
        bottom = rect2.y0
        if(page_id1 < page_id2):
            return ParseTab(page1, [0, top, 9999, 9999]) + ParseTab(page2, [0, 0, 9999, bottom])
        if(page_id1 == page_id2):
            return ParseTab(page1, [0, top, 9999, bottom])
        else:
            return ""

def ParseTab(page, bbox, columns=None):
    tab_rect = fitz.Rect(bbox).irect
    xmin, ymin, xmax, ymax = tuple(tab_rect)

    if tab_rect.is_empty or tab_rect.is_infinite:
        print("Warning: incorrect rectangle coordinates!")
        return []

    if type(columns) is not list or columns == []:
        coltab = [tab_rect.x0, tab_rect.x1]
    else:
        coltab = sorted(columns)

    if xmin < min(coltab):
        coltab.insert(0, xmin)
    if xmax > coltab[-1]:
        coltab.append(xmax)

    words = page.get_text("words")

    if words == []:
        print("Warning: page contains no text")
        return []

    alltxt = []

    # get words contained in table rectangle and distribute them into columns
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir in tab_rect:
            cnr = 0  # column index
            for i in range(1, len(coltab)):  # loop over column coordinates
                if ir.x0 < coltab[i]:  # word start left of column border
                    cnr = i - 1
                    break
            alltxt.append([ir.x0, ir.y0, ir.x1, cnr, w[4]])

    if alltxt == []:
        print("Warning: no text found in rectangle!")
        return []

    alltxt.sort(key=itemgetter(1))  # sort words vertically

    # create the table / matrix
    spantab = []  # the output matrix

    for y, zeile in groupby(alltxt, itemgetter(1)):
        schema = [""] * (len(coltab) - 1)
        for c, words in groupby(zeile, itemgetter(3)):
            entry = " ".join([w[4] for w in words])
            schema[c] = entry
        spantab.append(schema)

    return spantab