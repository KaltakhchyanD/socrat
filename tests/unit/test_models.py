import pytest
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import NotNullViolation, UniqueViolation

from myapp.models import ShortUrl, Click, User, create_user


def test_short_after_creation(new_shorturl):
    short = new_shorturl

    assert isinstance(short.id, int) and short.id >= 0
    assert short.long_url == "test_long"
    assert short.short_url == "test_short"
    assert short.clicks == None
    assert (
        str(short)
        == f"Short URL db entry {short.id} from long test_long with clicks None"
    )


def test_click_after_creation(new_click):
    click = new_click

    assert click.short_url == "test_short"
    assert click.number_of_clicks == None
    assert click.short_url_id == None


def test_short_click_relationship(new_short_and_click):
    short, click = new_short_and_click

    assert short.clicks == click
    assert click.short_url_id == short.id


def test_short_id_is_primary(create_db):
    db = create_db
    short_1 = ShortUrl(long_url="test_long", short_url="test_short")
    short_2 = ShortUrl(long_url="test_long", short_url="test_short")
    db.session.add(short_1)
    db.session.add(short_2)
    db.session.commit()

    assert short_1.id < short_2.id

    db.session.delete(short_1)
    db.session.delete(short_2)
    db.session.commit()


def test_short_long_url_not_nullable(create_db):
    db = create_db
    short = ShortUrl()
    db.session.add(short)

    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_click_short_url_is_primary(create_db):
    db = create_db
    click_1 = Click(short_url="test_short")
    click_2 = Click(short_url="test_short")
    db.session.add(click_1)
    db.session.add(click_2)
    # db.session.commit()

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


def test_user_after_creation(new_user):
    user = new_user

    assert user.username == "test_user"
    assert user.check_password("test_password")


def test_user_set_salt():
    user = User(username="test_user")
    assert user.salt == None
    user._set_salt()
    assert user.salt != None
    old_salt = user.salt
    user._set_salt()
    new_salt = user.salt
    assert old_salt != new_salt


def test_user_set_password():
    user = User(username="test_user")
    assert user.salt == None
    assert user.password_hash == None
    user.set_password("test_password")
    assert user.salt
    assert user.password_hash and user.password_hash != "test_password"


def test_user_check_password(new_user):
    assert new_user.check_password("test_password")
    assert not new_user.check_password("not")


def test_create_user(create_db):
    db = create_db
    create_user("new_user", "new_password")
    new_user = User.query.filter_by(username="new_user").first()
    assert new_user
    assert new_user.check_password("new_password")

    with pytest.raises(IntegrityError):
        create_user("new_user", "new_password")
