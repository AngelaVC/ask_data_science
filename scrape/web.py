from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
import database


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class WebPage:
    def __init__(self, url=None):
        self.url = url
        self.links = []
        self.soup = None
        self.text = None
        self.title = None

        if not self.url.startswith('http://'):
            raise Error("Must pass in URL, starting with http://")

    def __getAll(self):
        self.getSoup()
        self.getLinks()
        self.getTitle()
        self.getClean()

    def getSoup(self):

        req = Request(
                self.url, headers={'User-Agent': "Magic Browser"})
        html = urlopen(req)
        self.soup = bs(html, "lxml")

    def getLinks(self):
        '''This gets links starting with 'http' from single page.
        '''

        # XXXX what if there are no 'a' tags?

        for link in self.soup.findAll('a'):
            if 'href' in link.attrs:
                if link.attrs['href'].startswith("http"):
                    self.links.append(link.attrs['href'])
        return self.links

    def getTitle(self):
        regex = re.compile('.*title.*')
        title = ''
        for EachPart in self.soup.find_all("h1", {"class": regex}):
            title += EachPart.get_text()
        self.title = title
        return self.title

    def getText(self):
        # kill all script, style
        for junk in self.soup(["script", "style"]):
            junk.decompose()

        # kill all the math in the paragraph
        for math in self.soup.findAll("div", {"class": "math"}):
            math.decompose()

        neg_list = "comment|meta|footer|footnote|foot|script|style|bottom|margin|bottom"
        neg_class = re.compile(neg_list, re.IGNORECASE)

        paragraphs = self.soup.findAll("p")

        if paragraphs is None:
            self.text = ''
            return self.text

        for paragraph in paragraphs:
            if (paragraph.has_attr("class")):
                if any([bool(neg_class.search(
                                cls)) for cls in paragraph['class']]):
                    paragraph.decompose()

            elif (paragraph.has_attr("id")):
                if any([bool(
                           neg_class.search(cls)) for cls in paragraph['id']]):
                    paragraph.decompose()
        self.text = ' '.join(
                            [paragraph.get_text() for paragraph in paragraphs])

        return self.text

    def getClean(self):
        if self.text is None:
            self.getText()
        self.text = self.text.replace(
                    '\n', ' ').replace('\r', ' ').replace('\\\'', '\'').strip()
        return self.text


class DataTauPage(WebPage):
    def __init__(self, url='http://www.datatau.com'):
        WebPage.__init__(self, url)

    def getAllLinks(self, limit=50):
        '''This gets links starting with 'http' from single DataTau page.
        '''
        next_url = self.url
        self.soup = self.getSoup()
        n = 0

        # go through all the <a> tags, looking for "href" tags,
        # add these as links if they are external links
        # there is a single link "More", record as next_url
        while (next_url != '') & (n <= limit):
            next_url = ''

            for link in self.soup.findAll('a'):
                if 'href' in link.attrs:

                    if (link.attrs['href'].startswith("http")) & (
                                "datatau" not in link.attrs['href']):
                        self.links.append(link.attrs['href'])

                    elif link.get_text().startswith("More"):
                        next_url = 'http://datatau.com' + link.attrs['href']
            n += 1

    def scrapeStoreLinks(self, db=None):
        ''' This will write to existing or new TinyDB database db
            input is a WebPage object'''
        print("Scraping links: ")
        if not self.links:
            self.getAllLinks()
        else:
            for link in self.links:
                page = WebPage(link)
                page.getAll()
                if db is None:
                    db = input("Enter database name for storage, or hit enter to \
                          return the data.")
                    # XX Do some checking that input is reasonable
                    if db is None:
                        return page
                    else:
                        database.WritePage(page, db)
                print('.')
