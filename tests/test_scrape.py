import pytest

"""
This script tests a webscraping class called WebPage
"""

# TODO still need to fix this first test
@pytest.fixture
def webpage(url):
    from scrape.web import WebPage, database
    return WebPage(url)


test_site_data = [
                    ('http://google.com', True),
                    ('htt:google.com', 'Error')]


@pytest.mark.parametrize('x, expected', test_site_data)
def test_webpage(x, expected, webpage):
    assert webpage.html == expected
