import pytest

from myapp.models import ShortUrl, Click
from myapp.utils import URLShortener, create_new_short_url_db_entry_with_clicks


def test_encode():
    shortener = URLShortener()

    assert shortener.encode(-1) == ""
    assert shortener.encode(-100) == ""

    assert shortener.encode(123) == "4s"
    assert shortener.encode(0) == ""
    assert shortener.encode(50) == "_"
    assert shortener.encode(51) == "32"
    assert shortener.encode(2600) == "__"


def test_decode():
    shortener = URLShortener()

    assert shortener.decode("4s") == 123
    assert shortener.decode("") == 0
    assert shortener.decode("_") == 50
    assert shortener.decode("32") == 51
    assert shortener.decode("__") == 2600

def create_new_short(create_db):
    short_with_only_long_url_field = ShortUrl(long_url='test')
    short_full = create_new_short_url_db_entry_with_clicks(short_with_only_long_url_field)
    calculated_short_url = URLShortener.encode(short_full.id)
    assert short_full
    assert short_full.long_url == 'test'
    assert short_full.short_url == calculated_short_url
    assert isinstance(short_full.clicks, Click)
    assert short_full.clicks.number_of_clicks == 0
    assert short_full.clicks.short_url == calculated_short_url

