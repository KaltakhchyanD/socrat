from flask import Flask, render_template, request, url_for, redirect, abort, flash
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    login_required,
    logout_user,
)
from flask_migrate import Migrate
import validators

from myapp.config import Config
from myapp.models import db, ma, ShortUrl, User, Click
from myapp.utils import URLShortener, admin_required
from myapp.api.v1.link.views import blueprint as short_link_blueprint
from myapp.forms import LoginForm


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    app.jinja_env.globals.update(__builtins__)
    app.register_blueprint(short_link_blueprint)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/<string:link>")
    def redirect_to_long_url(link):
        url_shortener = URLShortener()
        # In case that link contains unsupported by url_shortener chars
        try:
            long_url_id = url_shortener.decode(link)
        except ValueError:
            abort(404, f"This short link is not valid")

        long_url_db_entry = ShortUrl.query.filter_by(id=long_url_id).first()
        if not long_url_db_entry:
            abort(404, f"This short link is not valid")
        long_url = long_url_db_entry.long_url

        # Just in case
        # Its good practise to check data on entry and exit
        if not validators.url(long_url):
            abort(404, f"This long url is not a valid URL!")

        # On click increase number of Clicks
        long_url_db_entry.clicks.number_of_clicks += 1
        db.session.commit()

        return redirect(long_url)

    @app.route("/admin_login", methods=["GET", "POST"])
    def login_for_admin():
        print(f"Referer - {request.referrer}")
        if current_user.is_authenticated:
            flash("You are already logged in!")
            # NO redirect to referer, coz there is no referer
            return redirect(url_for("index"))

        login_form = LoginForm()
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if user and user.check_password(password=login_form.password.data):
                login_user(user, remember=True)
                flash("You are now logged in!")
                # NO redirect to referer, coz there is no referer
                return redirect(url_for("index"))
            else:
                flash("Invalid username or password")
                return redirect(url_for("login_for_admin"))
        return render_template("login.html", form=login_form)

    @app.route("/admin")
    @login_required
    def admin_view():
        links = (
            ShortUrl.query.join(ShortUrl.clicks)
            .order_by(db.desc(Click.number_of_clicks))
            .limit(10)
            .all()
        )
        return render_template("admin.html", links=links)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app
