from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class ShortUrl(db.Model):
    __tablename__='shorturls'
    id = db.Column(db.Integer, primary_key=True)
    long_url=db.Column(db.String, nullable=False)
    short_url=db.Column(db.String)


class Click(db.Model):
    __tablename__='clicks'
    short_url=db.Column(db.String, primary_key=True)
    number_of_clicks=db.Column(db.Integer)
    short_url_id = db.Column(db.ForeignKey("shorturls.id"))