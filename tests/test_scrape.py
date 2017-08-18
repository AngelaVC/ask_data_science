import pytest

"""
This script tests methods a webscraping class called WebPage
"""


@pytest.fixture
def webpage():
    from scrape.web import WebPage
    return WebPage()


test_site_data = [
                    ('http://google.com', True),
                    ('htt:google.com', True)]


@pytest.mark.parametrize('x, expected', test_site_data)
def test_perfect_number(x, expected, webpage):
    assert webpage.html == expected
