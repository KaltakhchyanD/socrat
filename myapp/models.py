from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin
from flask_scrypt import (
    generate_random_salt,
    generate_password_hash,
    check_password_hash,
)

db = SQLAlchemy()
ma = Marshmallow()


class ShortUrl(db.Model):
    __tablename__ = "shorturls"
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String)
    clicks = db.relationship(
        "Click", uselist=False, backref="long_url", cascade="delete, delete-orphan"
    )

    def __repr__(self):
        return f"Short URL db entry {self.id} from long {self.long_url} with clicks {self.clicks}"


class Click(db.Model):
    __tablename__ = "clicks"
    short_url = db.Column(db.String, primary_key=True)
    number_of_clicks = db.Column(db.Integer)
    short_url_id = db.Column(db.ForeignKey("shorturls.id"))

    def __repr__(self):
        return f"This URL {self.short_url} clicked {self.number_of_clicks} times"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=True, unique=True)
    salt = db.Column(db.String(256), nullable=True, unique=True)

    def _set_salt(self):
        self.salt = generate_random_salt().decode()

    def set_password(self, password):
        self._set_salt()
        self.password_hash = generate_password_hash(
            password, self.salt.encode()
        ).decode()

    def check_password(self, password):
        return check_password_hash(
            password, self.password_hash.encode(), self.salt.encode()
        )

    def __repr__(self):
        return f"<User {self.username}, id - {self.id}>"


def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
