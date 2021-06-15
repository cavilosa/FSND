import os
from flask import Flask, request, jsonify, abort, flash
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# drops and creates db and a drink object for postman testing
db_drop_and_create_all()

# this route available for all users, down't require permissionsm shows short drinks information
@app.route("/drinks")
def get_drinks():
    drinks_full_list = Drink.query.all()

    drinks = [drink.short() for drink in drinks_full_list]

    return jsonify({
        "success": True,
        "drinks": drinks
    })

# the route shows detailed information about drinks, requires authorization, availabele for barista and manager, not for puclic use
@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    drinks_full_list = Drink.query.all()

    if not drinks_full_list:
        flash("There are no drinks to display")

    drinks = [drink.long() for drink in drinks_full_list]

    return jsonify({
        "success":True,
        "drinks": drinks
    })

# the route to post a new drink, requires permission, role - manager only
@app.route("/drinks", methods = ["POST"])
@requires_auth("post:drinks")
def post_drink(payload):
    body = request.get_json()
    if not body:
        abort(404)

    title = body.get("title")
    recipe = body.get("recipe")

    if not title or not recipe:
        abort(404)

    drink = Drink(
        title = title,
        recipe = json.dumps(recipe)
    )

    drink.insert()

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


# requires manager permission to change detailes in existing drink from the db
@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drink(payload, id):
    # getting drink object from the database
    drink = Drink.query.get(id)
    # check if the drink with the id exists
    if not drink:
        abort(404)

    # getting json information about what to uodate
    body = request.get_json()
    if not body:
        abort(404)

    # checking for the title from update info
    title = body.get("title")
    if title is not None:
        drink.title = title if type(title) == str else json.dumps(title)

    # checking for the recipe from update info
    recipe = body.get("recipe")
    if recipe is not None:
        drink.recipe = recipe if type(recipe) == str else json.dumps(recipe)

    # updating database object with new title or/and recipe
    drink.update()

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })

# a route to delete a drink for the db by its id, requires manager permission
@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payliad, id):
    drink = Drink.query.get(id)
    if not drink:
        # abort(404)
        flash(f"There is no drink with {id} id.")

    drink.delete()

    return jsonify({
        "success": True,
        "delete": id
    })


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.error,
        "code": error.status_code
    }), error.status_code
