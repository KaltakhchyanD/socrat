from myapp.models import db, ma, ShortUrl


class ShortUrlSchema(ma.ModelSchema):
    class Meta:
        model = ShortUrl
        sqla_session = db.session
    load_only = ['id', 'long_url']