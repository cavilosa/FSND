import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database  db = SQLAlchemy()


SQLALCHEMY_TRACK_MODIFICATIONS = False

# TODO IMPLEMENT DATABASE URL
username = os.environ.get("username")
password = os.environ.get("password")

SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(username, password, 'localhost:5432', 'fyyur')