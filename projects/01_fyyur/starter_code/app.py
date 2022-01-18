#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
#from models import Artist, Show, Venue
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
from models import setup_db, Artist, Venue, Show


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = setup_db(app)

#----------------------------------------------------------------------------#
# Models were moved to the separate file
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
    # CHALLENGE :
    # Show Recent Listed Artists and Recently Listed Venues on the
    # homepage, returning results for Artists and Venues sorting by newly created.
    # Limit to the 10 most recently listed items.

    # query artists and venues by id as it reflects the last added to the db,
    # added-date would change every time when edit of the vebue ahppens

    artists = Artist.query.order_by(Artist.id.desc()).limit(10)
    venues = Venue.query.order_by(Venue.id.desc()).limit(10)

    artists_data = []
    venues_data = []

    for artist in artists:
        shows_list = Show.query.filter(Show.artist_id == artist.id).all() # getting all shows that related to artist id
        shows = [] # empty list for shows related to the artist id
        for e in shows_list:
            venue = Venue.query.filter(Venue.id == e.venue_id).first() # getting venue of the show
            shows.append({
                "venue_id": e.venue_id,
                "venue_name": venue.name,
                "start_time": format_datetime(str(e.start_time))
            })
        genres = artist.genres.replace("{", "").replace("}", "")
        artists_data.append({
            "id": artist.id,
            "image_link": artist.image_link,
            "name": artist.name,
            "genres": genres,
            "website_link": artist.website_link,
            "shows": shows
        })

    return render_template('pages/home.html', artists = artists_data, venues = venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

    areas = []
    unique_places = Venue.query.distinct(Venue.city, Venue.state).all()
    venues = Venue.query.all()

    for unique_place in unique_places:
        # populating each unique place with its only shows
        venues = db.session.query(Venue.id, Venue.name).order_by(Venue.id).filter(Venue.city == unique_place.city).filter(Venue.state == unique_place.state)
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
    venues = Venue.query.filter(Venue.name.ilike(search)).all()
    data = []
    for venue in venues:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(venue.shows)
        })
    results = {
        "count": len(venues),
        "data": data
    }
    return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venues = Venue.query.filter(Venue.id == venue_id).all()
    past_shows = []
    upcoming_shows = []
    for venue in venues:
        shows = venue.shows # join method for venue.shows lazy="joined"
        # explicite version of join with lazy=True
        # session_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).all()
        for show in shows:
            # check if the show is in future or in the past:
            current_date = datetime.now()
            if str(show.start_time) < str(current_date):
                artist = Artist.query.get(show.artist_id)
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": str(show.start_time)
                })

            elif str(show.start_time) > str(current_date) :
                artist = Artist.query.get(show.artist_id)
                upcoming_shows.append(
                    {
                        "artist_id": show.artist_id,
                        "artist_name": artist.name,
                        "artist_image_link": artist.image_link,
                        "start_time": str(show.start_time)
                    }
                )
    genres = venue.genres.replace("{", "").replace("}", "")
    data =  {
        "id": venue.id,
        "name": venue.name,
        "genres": genres,
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

    return redirect(url_for("index"))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: c, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    error = False
    try:
        venue = Venue.query.get(venue_id)
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
                                       # window.location = "/"


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
    return render_template('pages/artists.html', artists=data, count = len(data))

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get("search_term", '')
    search = "%{}%".format(search_term)
    artists = Artist.query.filter(Artist.name.ilike(search)).all()
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
    artist = Artist.query.get(artist_id)
    shows = Show.query.filter_by(artist_id = artist_id).all() # get artist's shows
    # explicite way of querying artist shows session_shows = db.session.query(Show).join(Artist).filter(Show.artist_id == artist_id).all()
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

    genres = artist.genres.replace("{", "").replace("}", "")

    data.update({
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "seeking_venue": artist.seeking_venue,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "seeking_description": artist.seeking_description,
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
            print("Error from except in venue edit", e)
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

@app.route("/artist/<artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
    except ValueError as e:
        error = True
        print(f"Error ==> {e}")
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash(f"An error occured. Artist {artist.name} couldn't be deleted.")
        abourt(400)
    else:
        flash(f"Artist {artist.name} was successfully deleted.")
    return redirect(url_for("artists"))



@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm(request.form, meta={'csrf': False})
    if form.validate():
        try:
            artist = Artist()
            artist.genres = form.genres
            form.populate_obj(artist)
            db.session.add(artist)
            db.session.commit()
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
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
        flash("Errors" +  str(message))

    return redirect(url_for("index"))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows = Show.query.all()
    for show in shows:
        venue = Venue.query.get(show.venue_id)
        artist = Artist.query.get(show.artist_id)
        data.append({
            "venue_id": show.venue_id,
            "venue_name":venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time)
        })
    return render_template('pages/shows.html', shows=data)


@app.route("/shows", methods=["POST"])
def search_shows():
   # Search show by artist id or venue id
   # Todo implement show search frontend  from show.html/changed to search_show.html
    artist_id = request.form.get("artist_id")
    venue_id = request.form.get("venue_id")

    artist = Artist.query.get(artist_id)
    venue = Venue.query.get(venue_id)
    venue_messages = []
    results = []
    messages = []
    errors = []
    venue_results = []
    venue_errors = []
    if artist_id != None: # if the input field is empty
        if not artist: # if there is no astist with inputed id
            errors.append({
                "error": "Sorry... There is no artist with this id."
            })
        else:
            shows = Show.query.filter(Show.artist_id == artist_id).all()
            if not shows:
                genres = artist.genres.replace("{", "").replace("}", "")
                messages.append({
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_genres": genres
                })
            else:
                for show in shows:
                    venue = Venue.query.get(show.venue_id)
                    results.append({
                        "artist_id": artist.id,
                        "venue_id": venue.id,
                        "artist_image_link": artist.image_link,
                        "start_time": str(show.start_time),
                        "artist_name": artist.name,
                        "venue_name": venue.name
                    })

        return render_template("pages/search_show.html", results = results, search_term = request.form.get("artist_id", ""), errors = errors,  messages = messages )

    if venue_id != None: # if searching by venue id
        if not venue: # is id doesn't exist
            venue_errors.append({
                "error": "Sorry... There is no venue with this id."
            })
        else:
            shows = Show.query.filter(Show.venue_id == venue_id).all()
            if not shows:
                genres = venue.genres.replace("{", "").replace("}", "")
                venue_messages.append({
                    "venue_id": venue.id,
                    "venue_genres": genres
                })
            else:
                for show in shows:
                    artist = Artist.query.get(show.artist_id)
                    venue_results.append({
                        "artist_id": artist.id,
                        "venue_id": venue.id,
                        "artist_image_link": artist.image_link,
                        "start_time": str(show.start_time),
                        "artist_name": artist.name,
                        "venue_name": venue.name
                    })
        return render_template("pages/search_show.html", venue_results = venue_results, search_term = request.form.get("venue_id", ""), venue_errors = venue_errors,  venue_messages = venue_messages )
    else:
        return render_template("/forms/500.html")


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
    return redirect(url_for("index"))

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
