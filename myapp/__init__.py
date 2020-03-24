from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, current_user, login_user
from flask_migrate import Migrate
import validators

from myapp.config import Config
from myapp.models import db, ma, ShortUrl
from myapp.utils import URLShortener
from myapp.api.v1.link.views import blueprint as short_link_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    app.jinja_env.globals.update(__builtins__)
    app.register_blueprint(short_link_blueprint)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/<string:link>")
    def redirect_to_long_url(link):
        url_shortener = URLShortener()
        long_url_id = url_shortener.decode(link)
        long_url_db_entry = ShortUrl.query.filter_by(id=long_url_id).first()
        if not long_url_db_entry:
            abort(404, f"This short link is not valid")
        long_url = long_url_db_entry.long_url

        # Just in case
        # Its good practise to check data on entry and exit
        if not validators.url(long_url):
            abort(404, f"This long url is not a valid URL!")

        print(f"Clicks b4 - {long_url_db_entry.clicks}")
        long_url_db_entry.clicks[0].number_of_clicks += 1
        db.session.commit()
        print(f"Clicks after - {long_url_db_entry.clicks[0]}")

        return redirect(long_url)

    return app
