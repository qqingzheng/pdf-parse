from .pdf_parser import PDFParser
import fitz
from .common_types import *
class PyMuPDF(PDFParser):
    def __init__(self, buf):
        super().__init__(buf)
        self.pdf = fitz.open("pdf", buf.read())
        self.content = ""
        for page in self.pdf:
            self.content += page.get_text()
            page.search_for("Introduction")
            
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
        return self.pdf.get_toc()