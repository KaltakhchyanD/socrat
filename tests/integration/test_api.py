import json
import pytest
from pprint import pprint

from myapp.models import ShortUrl


def test_api_post_no_http_https(test_client):
    # data = json.dumps(dict(long_url="yandex.ru"))
    response = test_client.post("/api/v1/short/", json=dict(long_url="yandex.ru"))
    # response=test_client.post("/api/v1/short/", headers={'Content-Type': 'application/json'},data=data)

    assert response.status_code == 400
    assert response.json["errors"][0]["code"] == 3
    assert len(response.json["errors"]) == 1


def test_api_post_invalid_url(test_client, create_db):
    response = test_client.post("/api/v1/short/", json=dict(long_url="http://yandex"))
    assert response.status_code == 400
    assert response.json["errors"][0]["code"] == 1
    assert len(response.json["errors"]) == 1
    #
    response = test_client.post("/api/v1/short/", json=dict(long_url="https://yandex."))
    assert response.status_code == 400
    assert response.json["errors"][0]["code"] == 1
    assert len(response.json["errors"]) == 1


def test_api_post_url_socrat(test_client):
    response = test_client.post(
        "/api/v1/short/", json=dict(long_url="http://socrat.xyz")
    )

    assert response.status_code == 400
    assert response.json["errors"][0]["code"] == 2
    assert len(response.json["errors"]) == 1

    response = test_client.post(
        "/api/v1/short/", json=dict(long_url="https://socrat.xyz")
    )

    assert response.status_code == 400
    assert response.json["errors"][0]["code"] == 2
    assert len(response.json["errors"]) == 1


def test_api_post_valid_url_and_check_click_after_get_short(test_client, create_db):
    response = test_client.post(
        "/api/v1/short/", json=dict(long_url="https://yandex.ru")
    )

    assert response.status_code == 200
    assert response.json["long_url"] == "https://yandex.ru"
    assert response.json["short_url"]

    short = ShortUrl.query.filter_by(short_url=response.json["short_url"]).first()

    assert short.clicks.number_of_clicks == 0

    response = test_client.get(short.short_url)
    assert short.clicks.number_of_clicks == 1
