from getpass import getpass
import os
import sys

from myapp import create_app
from myapp.models import User, db


app = create_app()

with app.app_context():
    username = os.getenv('ADMIN_USER')
    password = os.getenv('ADMIN_PASSWORD')

    if User.query.filter(User.username == username).count():
        print("Admin already exist")
        sys.exit(0)

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    print(f"Admin added")
