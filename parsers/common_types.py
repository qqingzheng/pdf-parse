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
    def __getitem__(self, __name: str):
        return self.__dict__()[__name]
class Outline():
    def __init__(self, title, page):
        self.title = title
        self.page = page
        self.sub_outline = []
    def add_sub_outline(self, outline):
        self.sub_outline.append(outline)
    def display(self, depth=0):
        output = ""
        output += "\t"*depth
        output += f"{self.title}({self.page})\n"
        for sub in self.sub_outline:
            output += sub.display(depth+1)
        return output
    def search(self, title):
        result = -1
        if(self.title == title):
            result = self.page
        else:
            for sub in self.sub_outline:
                sub_result = sub.search(title)
                result = sub_result if sub_result != -1 else result
        return result
    def get_sub_count(self):
        return len(self.sub_outline)
    def __str__(self):
        return self.display()
    def __repr__(self):
        return self.__str__()