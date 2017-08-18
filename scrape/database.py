from tinydb import TinyDB, Query


class WritePage:
    def __init__(self, page=None, db=None):
        self.db = TinyDB(db)
        self.page = page
        # TODO need to do some check that database is well formed
        # TODO and that the page is a well-formed WebPage object

        self.db.insert({
                'url': self.page.link,
                'title': self.page.title,
                'text': self.page.text,
                'links': self.page.links})
