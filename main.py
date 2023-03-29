from parsers import *
import requests
import re
def get_dict(title, url):
    req = requests.get(url)
    pymupdf = PyMuPDF(req.content)
    result = {}
    result['title'] = title if pymupdf.get_meta()['title'] == '' else pymupdf.get_meta()['title']
    result['author'] = pymupdf.get_meta()['author']
    result['tag'] = pymupdf.get_meta()['keywords']
    result['abstract'] = pymupdf.get_block_content("abstract")
    result['introduction'] = pymupdf.get_block_content("introduction")
    result['background'] = pymupdf.get_block_content("background")
    result['content'] = pymupdf.content
    return result
    

if __name__ == "__main__":
    print(get_dict("title", "https://arxiv.org/pdf/1706.03762.pdf"))