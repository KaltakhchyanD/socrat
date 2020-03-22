from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class ShortUrl(db.Model):
    __tablename_='shorturls'
    id = db.Column(db.Integer, primary_key=True)
    long_url=db.Column(db.String, nullable=False)
    short_url=db.Column(db.String)