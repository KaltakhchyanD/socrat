import pytest

from myapp.forms import LoginForm


def test_login_form(test_app):
    form = LoginForm()

    assert str(form.hidden_tag()) == ""
    assert (
        str(form.username.label) == '<label for="username">Enter your username</label>'
    )
    assert form.username()
    assert form.password.label
    assert form.password()
    assert form.submit
