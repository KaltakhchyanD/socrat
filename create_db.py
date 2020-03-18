import subprocess

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

#from myapp import create_app, db
import myapp


try:
    myapp.db.create_all(app = myapp.create_app())   
except :#sqlalchemy.exc.OperationalError:
    print("That fucking error again!")
    create_database(myapp.Config.SQLALCHEMY_DATABASE_URI)
    #subprocess.call(['createdb', f'{myapp.Config.db_name}'])   
finally:
    myapp.db.create_all(app = myapp.create_app())   
