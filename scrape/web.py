from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re

def find_top_content(soup):
    '''This script is somewhat inspired by things
        at http://nirmalpatel.com/fcgi/hn.py'''
    neg_class = re.compile("comment|meta|footer|footnote|foot")
    pos_class = re.compile("post|hentry|entry|content|text|body|article")

    paragraphs = soup.findAll("p")

    top_parent = None
    parents = []

    for paragraph in paragraphs:
        parent = paragraph.parent

        if (parent not in parents):
            parents.append(parent)
            parent.score = 0

        # look at presence of positive or negative words in
        # class or id attributes
        if (parent.has_attr("class")):

            if any([bool(
                    neg_class.search(cls)) for cls in parent['class']]):
                parent.score -= 1

            if any([bool(
                    pos_class.search(cls)) for cls in parent['class']]):
                parent.score += 1

        if (parent.has_attr("id")):

            if any([bool(neg_class.search(cls)) for cls in parent['id']]):
                parent.score -= 1

            if any([bool(pos_class.search(cls)) for cls in parent['id']]):
                parent.score += 1

    for parent in parents:
        print(parent.score)
        if parent.score > top_parent.score:
            top_parent = parent
    return top_parent

class WebPage:
    def __init__(self, url=None):
        self.url = url
        self.links = []
        self.soup = None
        self.top = None

    def getSoup(self):

        # XXXX Need to make sure the url exists first!!

        html = urlopen(self.url)
        self.soup = bs(html, "lxml")

        return self.soup

    def getLinks(self):
        '''This gets links starting with 'http' from single page.
        Just the links that are in the top of the page
        '''

        # XXXX what if there are no 'a' tags?

        for link in self.top.findAll('a'):
            if ('href' in link.attrs) & (
                        link.attrs['href'].startswith("http")):
                self.links.append(link.attrs['href'])
        return self.links

    def getTop(self):
        # get the parent that holds the important content
        self.top = find_top_content(self.soup)
        return self.top

    def getText(self):
        # kill all script, style
        for junk in self.soup(["script", "style"]):
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
