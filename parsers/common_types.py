class MetaData():
    def __init__(self, author, title, creation_date, keywords, subject):
        self.author = author
        self.title = title
        self.creation_date = creation_date
        self.keywords = keywords
        self.subject = subject
    def __dict__(self):
        return {
            "author": self.author,
            "title": self.title,
            "creation_date": self.creation_date,
            "keywords": self.keywords,
            "subject": self.subject
        } 
    def __repr__(self):
        return str(self.__dict__())
    
class Outline():
    def __init__(self, title, page):
        self.title = title
        self.page = page
        self.sub_outline = []
    def add_sub_outline(self, outline):
        self.sub_outline.append(outline)
    def display(self, depth=0):
        print("\t"*depth, end="")
        print(f"{self.title}(self.page)")
        for sub in self.sub_outline:
            sub.display()
    def __repr__(self):
        return self.display()