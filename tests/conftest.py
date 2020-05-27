import os

import pytest
import sqlalchemy_utils

from myapp import create_app, db
from myapp.config import TestConfig
from myapp.models import ShortUrl, Click, User
from myapp.utils import URLShortener

@pytest.fixture(scope="module")
def test_app():
    test_app = create_app(TestConfig)
    app_context = test_app.app_context()
    app_context.push()

    yield test_app

    app_context.pop()
    # db.drop_all(app = test_app) - this is also a valid place


@pytest.fixture(scope="module")
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture(scope="module")
def create_db(test_app):
    try:
        db.create_all(app=test_app)
    except:
        sqlalchemy_utils.create_database(TestConfig.SQLALCHEMY_DATABASE_URI)
        db.create_all(app=test_app)

    yield db
    #db.session.close()
    db.session.remove()
    db.drop_all(app=test_app)


@pytest.fixture()
def new_shorturl(create_db):
    db = create_db
    short = ShortUrl(long_url="test_long", short_url="test_short")
    db.session.add(short)
    db.session.commit()

    yield short

    db.session.delete(short)
    db.session.commit()

@pytest.fixture()
def new_click(create_db):
    db = create_db
    click = Click(short_url="test_short")
    db.session.add(click)
    db.session.commit()

    yield click

    db.session.delete(click)
    db.session.commit()


@pytest.fixture()
def new_short_and_click(new_shorturl, new_click, create_db):
    new_shorturl.clicks = new_click
    db.session.commit()
    yield new_shorturl, new_click


@pytest.fixture()
def new_user(create_db):
    user = User(username='test_user')
    user.set_password('test_password')
    db.session.add(user)
    db.session.commit()

    yield user

    db.session.delete(user)
    db.session.commit()


@pytest.fixture()
def new_users_same_password():
    user_1 = User(username='test_user_1')
    user_2 = User(username='test_user_2')

    user_1.set_password('test_password')
    user_2.set_password('test_password')

    yield user_1, user_2

    db.session.delete(user_1)
    db.session.delete(user_2)
    db.session.commit()


@pytest.fixture()
def new_valid_short(create_db):
    short = ShortUrl(long_url='http://yandex.ru')
    db.session.add(short)
    db.session.commit()

    url_shortener = URLShortener()
    short.short_url = url_shortener.encode(short.id)
    db.session.add(short)
    db.session.commit()

    click_db_entry = Click(
        short_url=short.short_url, number_of_clicks=0
    )
    db.session.add(click_db_entry)
    short.clicks = click_db_entry
    db.session.commit()

    yield short

    db.session.delete(short)
    db.session.commit()


@pytest.fixture()
def create_admin(create_db):
    username = "test"
    password = "test"

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    yield new_user

    db.session.delete(new_user)
    db.session.commit()
