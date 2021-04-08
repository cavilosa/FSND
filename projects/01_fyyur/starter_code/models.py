from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate

app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)
#
# migrate = Migrate(app, db)

db = SQLAlchemy(app)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref = 'venues', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    address = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref = 'artists', lazy=True)


class Show(db.Model):
    __tablename__="Show"
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False, primary_key=True)
    start_time = db.Column(db.DateTime)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
