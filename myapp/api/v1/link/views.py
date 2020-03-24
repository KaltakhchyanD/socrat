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
    # If not - abort
    if not validators.url(json_from_request["long_url"]):
        abort(404, f"This is not a valid URL!")

    short_url_from_json = schema.load(json_from_request)

    # Check that entry is not in db already!
    # Otherwise - many similar entries with same site
    db.session.add(short_url_from_json)
    db.session.commit()

    url_shortener = URLShortener()
    short_url_from_json.short_url = url_shortener.encode(short_url_from_json.id)
    db.session.add(short_url_from_json)

    click_db_entry = Click(short_url=short_url_from_json.short_url, number_of_clicks=0, short_url_id=short_url_from_json.id)
    print(f"At api click - {click_db_entry}")

    #click_db_entry = Click(short_url=short_url_from_json.short_url, number_of_clicks=0)
    db.session.add(click_db_entry)
    #short_url_from_json.clicks.append(click_db_entry)

    print(f"At api short_url_from_json - {short_url_from_json}")
    #db.session.add(short_url_from_json)


    db.session.commit()


    return schema.dump(short_url_from_json), 200
