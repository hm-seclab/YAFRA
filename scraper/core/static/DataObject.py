'''
This object represents the scraped data as a python object.
'''

class DataObject:
    def __init__(self, content, title, source, date):
        self.content = content
        self.title = title
        self.source = source
        self.date = date

    def __json__(self):
        '''
        __json__ will transform the data object into a json object.
        '''
        return {
            "content": self.content,
            "title": self.title,
            "source": self.source
        }

