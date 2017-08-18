from tinydb import TinyDB, Query


class WritePage:
    def __init__(self, page=None, db=None):
        self.db = TinyDB(db)
        # TODO need to do some check that database is well formed
        # TODO and that the page is a well-formed WebPage object

        self.db.insert({
                'url': page.link,
                'title': page.title,
                'text': page.text,
                'links': page.links})
