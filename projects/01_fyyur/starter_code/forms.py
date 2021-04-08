from datetime import datetime
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, validators
from wtforms.validators import InputRequired, AnyOf, URL
from enums import Genre, State
#import enum
# from wtforms import ValidationError
# from flask import flash

# def is_integer(form, field):
#     for each in field.data:
#         print (each)
#         if type(each) != int:
#             raise ValidationError("Phone number can only have numbers in it")

# def validate(self):
#     rv = FlaskForm.validate(self)
#     if not rv:
#         return False
#     if not all(elements in self.genres.data for elements in Genre.choices()):
#         self.genres.errors.append("Choose genres from the list")
#         return False
#     if not all(elements in self.state.data for elements in State.choices()):
#         self.genres.errors.append("Chooise states from the list")
#         return False
#     else:
#         return True


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id', [validators.InputRequired(), validators.NumberRange()]
    )
    venue_id = StringField(
        'venue_id', [validators.InputRequired(), validators.NumberRange()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[InputRequired()],
        default= datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[InputRequired()]
    )
    city = StringField(
        'city', validators=[InputRequired()]
    )
    state = SelectField(
        'state', validators=[InputRequired()],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[InputRequired()]
    )
    phone = StringField(
        'phone', [validators.Optional()]
    )
    image_link = StringField(
        'image_link', [validators.Optional()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres',
        validators=[InputRequired()],
        choices=Genre.choices()

    )

    facebook_link = StringField(
        'facebook_link', [validators.Optional()]
    )

    website_link = StringField(
        'website_link', [validators.Optional()]
    )

    seeking_talent = BooleanField( 'seeking_talent', [validators.Optional()] )

    seeking_description = StringField(
        'seeking_description', [validators.Optional()]
    )

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not all(self.genres.data for choice in Genre):
            self.genres.errors.append("Choose genres from the list")
            return False
        if not all(self.state.data for choice in State):
            self.genres.errors.append("Chooise states from the list")
            return False
        else:
            return True




class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[InputRequired()]
    )
    city = StringField(
        'city', validators=[InputRequired()]
    )
    state = SelectField(
        'state',
        validators=[InputRequired()],
        choices=State.choices()
    )

    address = StringField(
        'address', validators=[InputRequired()]
    )

    phone = StringField(
        # TODO implement validation logic for state
        'phone', [validators.Optional()]
    )
    image_link = StringField(
        'image_link', [validators.Optional(), validators.URL()]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[InputRequired()],
        choices=Genre.choices()
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', [validators.Optional(), validators.URL()]
     )

    website_link = StringField(
        'website_link', [validators.Optional(), validators.URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue', [validators.Optional()] )

    seeking_description = StringField(
            'seeking_description', [validators.Optional()]
     )

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not all(self.genres.data for choice in Genre):
            self.genres.errors.append("Choose genres from the list")
            return False
        if not all(self.state.data for choice in State):
            self.genres.errors.append("Chooise states from the list")
            return False
        else:
            return True
