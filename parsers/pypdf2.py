from .pdf_parser import PDFParser
from PyPDF2 import PdfReader
from .common_types import *
class PyPDF2(PDFParser):
    def __init__(self, buf):
        super().__init__(buf)
        self.pdf = PdfReader(stream=buf)
        self.content = ""
    def get_meta(self):
        meta_data = MetaData(self.pdf.metadata['/Author'],
                             self.pdf.metadata['/Title'],
                             self.pdf.metadata['/CreationDate'],
                             self.pdf.metadata['/Keywords'],
                             self.pdf.metadata['/Subject'],
                             )
        return meta_data
    def get_catagory(self):
        return self.pdf.outline