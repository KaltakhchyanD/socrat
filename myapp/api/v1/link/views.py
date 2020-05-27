from flask import Blueprint, abort, jsonify, request, make_response
import validators
import urllib3

from myapp.models import db, ShortUrl, Click
from myapp.api.v1.link.models import ShortUrlSchema
from myapp.utils import URLShortener, create_new_short_url_db_entry_with_clicks

blueprint = Blueprint("rest_api", __name__, url_prefix="/api/v1/short")


@blueprint.route("/", methods=["POST"])
def make_short_url():
    schema = ShortUrlSchema()
    json_from_request = request.get_json()

    # Validate that url is valid
    # If not - return json with 400
    if not validators.url(json_from_request["long_url"]):
        if not json_from_request["long_url"].startswith(("http://", "https://")):
            return make_response(
                jsonify(
                    {
                        "errors": [
                            {
                                "code": 3,
                                "message": "URL should start with 'http://' or 'https://'",
                            }
                        ]
                    }
                ),
                400,
            )
        return make_response(
            jsonify({"errors": [{"code": 1, "message": "Bad long url"}]}), 400
        )

    host_of_long_url = urllib3.util.parse_url(json_from_request["long_url"]).host
    if host_of_long_url == "socrat.xyz":
        return make_response(
            jsonify(
                {
                    "errors": [
                        {
                            "code": 2,
                            "message": "I know what u did there! Thats not cool! (Don't try to shortify this site!)",
                        }
                    ]
                }
            ),
            400,
        )

    long_to_short_url_from_json = schema.load(json_from_request)
    updated_long_to_short = create_new_short_url_db_entry_with_clicks(
        long_to_short_url_from_json
    )

    return schema.dump(updated_long_to_short), 200
