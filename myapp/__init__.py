from flask import Flask, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user
from flask_migrate import Migrate 

from myapp.config import Config
from myapp.database import db, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    #login_manager = LoginManager()
    #login_manager.init_app(app)
    migrate = Migrate(app, db)

    app.jinja_env.globals.update(__builtins__)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5500, debug=True)
