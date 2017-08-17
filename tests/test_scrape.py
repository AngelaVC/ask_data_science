import pytest

"""
This script tests methods in a number theory class called Numbers
"""

@pytest.fixture
def num():
     from swe_barebones.numbers import Numbers
     return Numbers()
