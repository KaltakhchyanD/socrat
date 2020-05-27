from flask import current_app, g, session
from flask_login import current_user
import pprint
import pytest

from myapp.models import User

def test_index(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_valid_existing_short(test_client, new_valid_short):
    short_url = new_valid_short.short_url

    response = test_client.get(short_url)
    assert response.status_code == 302
    assert response.headers["Location"] == "http://yandex.ru"


def test_invalid_short(test_client):
    short_url = "10"
    response = test_client.get(short_url)
    assert response.status_code == 404
    assert b":(" in response.data


def test_non_existing_short(test_client):
    short_url = "bcdf"
    response = test_client.get(short_url)
    assert response.status_code == 404
    assert b":(" in response.data


def test_admin_login_get(test_client):
    response = test_client.get("/admin_login")
    assert response.status_code == 200
    assert b"Enter your username" in response.data


def test_admin_login_post_valid(test_client, create_admin, test_app):
    login_data = dict(
        username="test", password="test", submit="Submit", follow_redirects=True
    )

    response = test_client.post("/admin_login", data=login_data)

    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/"
    assert (
        b"Invalid username or password"
        not in test_client.get(response.headers["Location"]).data
    )
    with test_client:
        test_client.get('/')
        assert current_user.is_authenticated


def test_admin_login_post_invalid_password(test_client, create_admin):
    login_data = dict(
        username="test", password="wrong", submit="Submit", follow_redirects=True
    )

    response = test_client.post("/admin_login", data=login_data)
    import pprint

    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/admin_login"

    response_data = test_client.get(response.headers["Location"]).data
    assert b"Invalid username or password" in response_data


def test_admin_login_post_invalid_username(test_client, create_admin):
    login_data = dict(
        username="wrong", password="test", submit="Submit", follow_redirects=True
    )

    response = test_client.post("/admin_login", data=login_data)

    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/admin_login"

    response_data = test_client.get(response.headers["Location"]).data
    assert b"Invalid username or password" in response_data


def test_admin_login_post_valid_twice(test_client, create_admin):
    login_data = dict(
        username="test", password="test", submit="Submit", follow_redirects=True
    )

    first_response = test_client.post("/admin_login", data=login_data)

    second_response = test_client.post("/admin_login", data=login_data)

    assert second_response.status_code == 302
    assert second_response.headers["Location"] == "http://localhost/"

    assert (
        b"You are already logged in!"
        in test_client.get(second_response.headers["Location"]).data
    )


def test_logout_after_login(test_client, create_admin):

    response = test_client.get("/")


    login_data = dict(
        username="test", password="test", submit="Submit", follow_redirects=True
    )

    response=test_client.post("/admin_login", data=login_data)
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/"
    
    assert (
        b"You are now logged in!"
        in test_client.get(response.headers["Location"]).data
    )

    with test_client:
        test_client.get('/')
        assert current_user.is_authenticated


    response = test_client.get("/logout")

    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/"
    
    assert (
        b"You are now logged out!"
        in test_client.get(response.headers["Location"]).data
    )

    with test_client:
        test_client.get('/')
        assert not current_user.is_authenticated


def test_logout_without_login(test_client, create_admin):
    response = test_client.get('/logout')
    assert response.status_code == 401

def test_admin_after_login(test_client, create_admin):
    login_data = dict(
        username="test", password="test", submit="Submit", follow_redirects=True
    )

    response = test_client.post("/admin_login", data=login_data)
    
    response = test_client.get('/admin')
    assert response.status_code == 200
    assert b'Long URL' in response.data


def test_admin_without_login(test_client, create_admin):
    response = test_client.get('/admin')
    assert response.status_code == 401
