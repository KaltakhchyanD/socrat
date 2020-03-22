from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, current_user, login_user
from flask_migrate import Migrate

from myapp.config import Config
from myapp.models import db, ma
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
    def ya_page(link):
        if link == "ya":
            return redirect("https://yandex.ru")

    return app
