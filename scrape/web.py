from urllib.request import Request, urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup as bs
import re
import scrape.database as database


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class WebPage:
    def __init__(self, url=None):
        self.url = url
        self.html = None
        self.links = []
        self.soup = None
        self.text = None
        self.title = None

        req = Request(self.url, headers={'User-Agent': "Magic Browser"})
        try:
            self.html = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)

            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)

    def getAll(self):
        ''' This gets the beautifulsoup object, title, links, and then cleans
            the text '''
        self.getSoup()
        self.getLinks()
        self.getTitle()
        self.getClean()

    def getSoup(self):
        ''' uses request and urlopen to access url, then calls BeautifulSoup
            to create soup object that can be later extracted for data'''
        req = Request(
                self.url, headers={'User-Agent': "Magic Browser"})
        html = urlopen(req)
        self.soup = bs(html, "lxml")

    def getLinks(self):
        ''' Gets links starting with 'http' from a single page.
            Appends all to self.links
        '''

        # TODO take care of case when there are no 'a' tags

        for link in self.soup.findAll('a'):
            if 'href' in link.attrs:
                if link.attrs['href'].startswith("http"):
                    self.links.append(link.attrs['href'])

    def getTitle(self):
        ''' Looks for h1 tags that contain title in their class and adds
            any text in those to self.title '''
        regex = re.compile('.*title.*')
        title = ''
        for EachPart in self.soup.find_all("h1", {"class": regex}):
            title += EachPart.get_text()
        self.title = title

    def getText(self):
        ''' Kill all script, style, and math elements, then look to just grab
            text that does not contain text in the neg_list '''
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

        # Get rid of any paragraphs whose class has any of the negative
        # language (things like footers etc)
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

    def getClean(self):
        ''' Get rid of elements like hard returns as well as trailing spaces'''
        if self.text is None:
            self.getText()
        self.text = self.text.replace(
                    '\n', ' ').replace('\r', ' ').replace('\\\'', '\'').strip()


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
