from myapp.models import db, ma, ShortUrl
from flask_marshmallow import fields

class ShortUrlSchema(ma.ModelSchema):
    class Meta:
        model = ShortUrl
        sqla_session = db.session
    load_only = ['id', 'long_url']
    number = fields.fields.Method("get_number_of_clicks")

    def get_number_of_clicks(self, obj):
        return obj.clicks.number_of_clicks