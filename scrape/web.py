from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


class WebPage:
    def __init__(self, url=None):
        self.url = url
        self.links = []
        self.soup = None

    def getSoup(self):

        # XXXX Need to make sure the url exists first!!

        html = urlopen(self.url)
        self.soup = bs(html, "lxml")

        return self.soup

    def getLinks(self):
        '''This gets links starting with 'http' from single page.
        '''

        # XXXX what if there are no 'a' tags?

        for link in self.soup.findAll('a'):
            if ('href' in link.attrs) & (
                        link.attrs['href'].startswith("http")):
                self.links.append(link.attrs['href'])
        return self.links

    def getText(self):
        # kill all script, style, tables
        for junk in self.soup(["script", "style", "table"]):
            junk.decompose()


class DataTauPage(WebPage):
    def __init__(self, url='http://www.datatau.com'):
        WebPage.__init__(self, url)

    def getAllLinks(self, limit=50):
        '''This gets links starting with 'http' from single DataTau page.
        '''
        next_url = self.url
        soup = self.getSoup()
        n = 0

        # go through all the <a> tags, looking for "href" tags,
        # add these as links if they are external links
        # there is a single link "More", record as next_url
        while (next_url != '') & (n <= limit):
            next_url = ''

            for link in soup.findAll('a'):
                if 'href' in link.attrs:
                    if (link.attrs['href'].startswith("http")) & (
                                "datatau" not in link.attrs['href']):
                        self.links.append(link.attrs['href'])
                    elif link.get_text().startswith("More"):
                        next_url = 'http://datatau.com' + link.attrs['href']
            n += 1
        return self.links
