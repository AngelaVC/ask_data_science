import pytest
from tinydb import TinyDB

test_db = TinyDB('test_db.json')
test_db.insert({
        'url': 'http://google.com',
        'title': 'A Title',
        'text': "The best text. Even best stuff.",
        'links': ['http://link1.html', 'http://link2.html']})


@pytest.fixture
def gen():
    from ..tweet.generate import Generated
    generated = Generated('test_db.json')
    generated.getAll()
    return generated


test_data = [((test_db, 'The'), ('The', 'best')), ((test_db, 'XX124'), (None, None))]
@pytest.mark.parametrize('x,expected',test_data)
def test_firstWords(x, expected, gen):
    # Test initialization, not sure how
    # assert isinstance(gen(input1[0]), Generated)

    tweet, next_word = gen.firstWords()
    assert str(tweet == expected[0])
    assert str(next_word == expected[1])


test2_data = [((test_db, 'In the dark', 'text'), ('In the dark text', '.')),
              ((test_db, 'One or two', 'The'), ('One or two The', 'best'))]
@pytest.mark.parametrize('x,expected', test2_data)
def test_nextWords(x, expected, gen):

    tweet, next_word = gen.nextWords(x[1])

    assert str(tweet == expected[0])
    assert str(next_word == expected[1])

#test_generated_class(input1, expected1)
