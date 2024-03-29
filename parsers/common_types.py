import re
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
    def __init__(self, title, value, parent=None):
        self.title = title
        self.value = value
        self.parent = parent
        self.sub_outline = []
    def add_sub_outline(self, outline):
        self.sub_outline.append(outline)
    def display(self, depth=0):
        output = ""
        output += "\t"*depth
        output += f"{self.title}({self.value})\n"
        for sub in self.sub_outline:
            output += sub.display(depth+1)
        return output
    def search(self, title):
        result = -1
        if(self.title == title):
            result = self.value
        else:
            for sub in self.sub_outline:
                sub_result = sub.search(title)
                result = sub_result if sub_result != -1 else result
        return result
    
    def get_idx_in_sub(self, title):
        for i, sub in enumerate(self.sub_outline):
            if re.search(f"{title}", sub.title, re.IGNORECASE):
                return i
        return None
    def search_title(self, title):
        result = ""
        if re.search(f"{title}", self.title, re.IGNORECASE):
            return self.title
        for sub in self.sub_outline:
            sub_result = sub.search_title(title)
            result = sub_result if sub_result != "" else result
        return result
    def search_sibling_title(self, title):
        result = ""
        if re.search(f"{title}", self.title, re.IGNORECASE):
            ancester = self.parent
            search_title = self.title
            while ancester is not None:
                sibling_idx = ancester.get_idx_in_sub(search_title) + 1
                if sibling_idx >= ancester.get_sub_count():
                    search_title = ancester.title
                    ancester = ancester.parent
                else:
                    return ancester.sub_outline[sibling_idx].title
        for sub in self.sub_outline:
            sub_result = sub.search_sibling_title(title)
            result = sub_result if sub_result != "" else result
        return result
    def get_sub_count(self):
        return len(self.sub_outline)
    def __str__(self):
        return self.display()
    def __repr__(self):
        return self.__str__()