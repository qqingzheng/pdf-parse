from parsers import *

if __name__ == "__main__":
    with open("1706.03762-2.pdf", "rb") as file:
        pymupdf = PyMuPDF(file)
        print(pymupdf.get_meta())
        print(pymupdf.get_catagory())