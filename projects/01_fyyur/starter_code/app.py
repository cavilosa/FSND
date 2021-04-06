#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

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
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

    areas = []
    unique_places = Venue.query.distinct(Venue.city, Venue.state).all()
    venues = Venue.query.all()
    # print("unique", unique_places[0].city)
    # print("venue", venues[0].city)
    for unique_place in unique_places:
        venues = db.session.query(Venue.id, Venue.name).order_by(Venue.id).filter(Venue.city == unique_place.city).filter(Venue.state == unique_place.state)
        print("venues", venues)
        print("venues count", venues.count())
        areas.append({
            "city": unique_place.city,
            "state": unique_place.state,
            "venues": venues,
            "num_upcoming_shows": venues.count()
        })

    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get("search_term", '')
    search = "%{}%".format(search_term)
    #print("search", search)
    venues = Venue.query.filter(Venue.name.ilike(search)).all()
    data = []
    for venue in venues:
        print("venue", venue.shows)
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(venue.shows)

        })
    # print("len shows", len(venue.shows))
    results = {
        "count": len(venues),
        "data": data
    }
    # print("results", results)

    return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #print("venue id", venue_id)

    venues = Venue.query.filter(Venue.id == venue_id).all()
    past_shows = []
    upcoming_shows = []
    for venue in venues:
        print("venue id, len", venue.id, len(venues))
        shows = venue.shows
        print("venue.shows", len(shows))
        for show in shows:
            current_date = datetime.now()
            #print(type(str(current_date)), type(str(show.start_time)))
            if str(show.start_time) < str(current_date):
                #print("past shows",str(show.start_time), str(current_date))
                artist = Artist.query.get(show.artist_id)
                print("artist.id", artist.id)
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": str(show.start_time)
                })

                print("past_shows", len(past_shows), past_shows)
            elif str(show.start_time) > str(current_date) :
                print("upcoming_shows", str(show.start_time), str(current_date))
                # print("upcoming_shows", len(upcoming_shows), upcoming_shows)
                artist = Artist.query.get(show.artist_id)
                print("artist.id", artist.id)
                upcoming_shows.append(
                    {
                        "artist_id": show.artist_id,
                        "artist_name": artist.name,
                        "artist_image_link": artist.image_link,
                        "start_time": str(show.start_time)
                    }
                )
                print("upcoming_shows", upcoming_shows)

    data =  {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            venue = Venue()
            form.populate_obj(venue)
            db.session.add(venue)
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
        except ValueError as e:
            print(e)
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        message=[]
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors" +  str(message))

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: c, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    error = False
    try:
        venue = Venue.query.get(venue_id)
        print("DELETE ID", venue.id)
        db.session.delete(venue)
        db.session.commit()
    except Exception as e:
        error = True
        print(f"Error ==> {e}")
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash(f"An error occured. Venue {venue.name} couldn't be deleted.")
        abourt(400)
    else:
        flash(f"Venue {venue.name} was successfully deleted.")

    return redirect(url_for('venues')) # where flash shows up after db deletion,
                                       # but gets redirected to the main page from the js

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # # TODO: replace with real data returned from querying the database
    data =[]
    artists = Artist.query.all()
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
    #print("DATA", data)
    return render_template('pages/artists.html', artists=data, count = len(data))

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get("search_term", '')
    search = "%{}%".format(search_term)
    artists = Artist.query.filter(Artist.name.ilike(search)).all()
    print("ARTISTS lent", len(artists))
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(artist.shows)
        })

    response = {
        "count": len(artists),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

    data = {}
    current_date = datetime.now()
    artist = Artist.query.get(artist_id);
    print("ARTISTS", artist.name)
    shows = Show.query.filter_by(artist_id = artist_id)
    #print("SHOWS", len(shows))
    past_shows = []
    upcoming_shows = []
    for show in shows:
        if str(current_date) > str (show.start_time):
            venue = Venue.query.get(show.venue_id)
            past_shows.append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.start_time)
            })
        else:
            venue = Venue.query.get(show.venue_id)
            upcoming_shows.append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.start_time)
            })
    data.update({
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "seeking_venue": artist.seeking_venue,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    })

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    form = VenueForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            artist = Artist.query.get(artist_id)
            form.populate_obj(artist)
            db.session.commit()
            flash('Artist ' + request.form['name'] + ' was successfully edited!')
        except ValueError as e:
            print(e)
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        message=[]
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors " +  str(message))


    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    print("genres", venue.genres)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            venue = Venue.query.get(venue_id)
            form.populate_obj(venue)
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully edited!')
        except ValueError as e:
            print(e)
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        message=[]
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors" +  str(message))

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            show = Show()
            form.populate_obj(show)
            db.session.add(show)
            db.session.commit()
            # on successful db insert, flash success
            flash('Show was successfully listed!')
        except ValueError as e:
            print(e)
            flash('An error occurred. Show ' + request.form['name'] + ' could not be listed.')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        message=[]
        for field, err in form.errors.items():
            message.append(field + " " + "|".join(err))
        flash("Errors" +  str(message))

            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Show could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
