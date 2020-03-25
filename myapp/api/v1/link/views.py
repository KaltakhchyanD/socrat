from flask import Blueprint, abort, jsonify, request, make_response
import validators

from myapp.models import db, ShortUrl, Click
from myapp.api.v1.link.models import ShortUrlSchema
from myapp.utils import URLShortener

blueprint = Blueprint("rest_api", __name__, url_prefix="/api/v1/short")


@blueprint.route("/", methods=["POST"])
def make_short_url():
    schema = ShortUrlSchema()
    json_from_request = request.get_json()

    # Validate that url is valid
    # If not - return json with 400
    if not validators.url(json_from_request["long_url"]):
        return make_response(
            jsonify({"errors": [{"code": 123, "message": "Bad long url"}]}), 400
        )

    short_url_from_json = schema.load(json_from_request)

    # Check that entry is not in db already!
    # Otherwise - many similar entries with same site
    db.session.add(short_url_from_json)
    db.session.commit()

    url_shortener = URLShortener()
    short_url_from_json.short_url = url_shortener.encode(short_url_from_json.id)
    db.session.add(short_url_from_json)

    # click_db_entry = Click(short_url=short_url_from_json.short_url, number_of_clicks=0, short_url_id=short_url_from_json.id)
    click_db_entry = Click(short_url=short_url_from_json.short_url, number_of_clicks=0)
    # This is nessesery to ADD NEW object to SESSION
    db.session.add(click_db_entry)
    short_url_from_json.clicks.append(click_db_entry)
    db.session.commit()

    return schema.dump(short_url_from_json), 200
