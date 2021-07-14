#TODO comments

class DataObject:
    def __init__(self, content, title, source, date):
        self.content = content
        self.title = title
        self.source = source
        self.date = date

    def __json__(self):
        return {
            "content": self.content,
            "title": self.title,
            "source": self.source
        }

