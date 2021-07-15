class DataObject:
    '''
    This class represents the scraped data as a python object.
    '''

    def __init__(self, content, title, source, date):
        '''
        __init__ initializes the data object.
        @param content will be the content of the scraped data.
        @param title will be the title of the scraped data.
        @param source will be the source the scraped data is scraped of.
        @param date will be the date, the data has been published.
        '''
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

