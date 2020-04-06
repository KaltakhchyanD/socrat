from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "Enter your username",
        validators=[DataRequired()],
        render_kw={"class": "form_control"},
    )
    password = PasswordField(
        "Enter your password",
        validators=[DataRequired()],
        render_kw={"class": "form_control"},
    )
    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary"})
