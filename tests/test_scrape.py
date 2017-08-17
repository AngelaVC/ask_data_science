import pytest

"""
This script tests methods a webscraping class called WebPage
"""


@pytest.fixture
def webpage():
    from scrape.web import WebPage
    return WebPage()
