from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class ShortUrl(db.Model):
    __tablename__ = "shorturls"
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String)
    clicks = db.relationship(
        "Click", backref="long_url", cascade="delete, delete-orphan"
    )

    def __repr__(self):
        return f"Short URL db entry {self.id} from long {self.long_url}"


class Click(db.Model):
    __tablename__ = "clicks"
    short_url = db.Column(db.String, primary_key=True)
    number_of_clicks = db.Column(db.Integer)
    short_url_id = db.Column(db.ForeignKey("shorturls.id"))

    def __repr__(self):
        return f"This URL {self.short_url} clicked {self.number_of_clicks} times"
