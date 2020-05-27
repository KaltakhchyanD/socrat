import os
from datetime import timedelta


class Config:
    """Config object for Flask"""

    PRODUCTION = os.getenv("PRODUCTION") == "1"
    # session cookie and remember_Me only sent by browser over https
    if PRODUCTION:
        SESSION_COOKIE_SECURE = True
        REMEMBER_COOKIE_SECURE = True
        SERVER_NAME = "socrat.xyz"
        PREFERRED_URL_SCHEME = "https"

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    in_docker = os.getenv("IN_DOCKER")
    db_host = os.getenv("DB_HOST") if in_docker == "1" else "localhost"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    REMEMBER_COOKIE_DURATION = timedelta(days=5)


class TestConfig():
    """Config for testing"""

    PRODUCTION = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://test_user:test_password@localhost:5432/test_db"
    SECRET_KEY = 'some_secret_key'
    TESTING=True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_TRACK_MODIFICATIONS = False



