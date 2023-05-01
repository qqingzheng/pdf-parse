from parsers import *
import requests
from lxml import etree
import re
def get_dict(title, buf):
    pymupdf = PyMuPDF(buf)
    result = {}
    print(pymupdf.get_outline())
    result['title'] = title if pymupdf.get_meta()['title'] == '' else pymupdf.get_meta()['title']
    result['author'] = pymupdf.get_meta()['author']
    result['tag'] = pymupdf.get_meta()['keywords']
    
    result['abstract'] = pymupdf.get_block_content("introduction")
    # result['introduction'] = pymupdf.get_block_content("introduction")
    # result['method'] = pymupdf.get_block_content_by_tries(["methods","method","methodology"])
    # result['related_works'] = pymupdf.get_block_content("related work")
    # result['conclusion'] = pymupdf.get_block_content("conclusion")
    # result['references'] = pymupdf.get_block_content("references")
    # result['experiments'] = pymupdf.get_block_content("Experiments")

    # result['content'] = pymupdf.content # All content
    return result
def get_dict_from_url(title, url):
    req = requests.get(url)
    return get_dict(title, req.content)

if __name__ == "__main__":
    print(get_dict_from_url("asd", "https://arxiv.org/pdf/1709.00903v1.pdf"))