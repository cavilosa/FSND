import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks")
def get_drinks():
    drinks_full_list = Drink.query.all()

    if not drinks_full_list:
        abort(404)

    drinks = [drink.short() for drink in drinks_full_list]

    return jsonify({
        "success": True,
        "drinks": drinks
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    drinks_full_list = Drink.query.all()
    if not drinks_full_list:
        abort(404)
    drinks = [drink.long() for drink in drinks_full_list]

    return jsonify({
        "success":True,
        "drinks": drinks
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
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
        "drinks": drink.long()
    })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
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
        drink.title = title

    # checking for the recipe from update info
    recipe = body.get("recipe")
    if recipe is not None:
        drink.recipe = json.dumps(recipe)

    # updating database object with new title or/and recipe
    drink.update()

    return jsonify({
        "success": True,
        "drink": drink.long()
    })



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payliad, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)

    drink.delete()

    return jsonify({
        "success": True,
        "delete": id
    })


# Error Handling
'''
Example error handling for unprocessable entity
'''


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
    print("ERROR", type(error))
    return jsonify({
        "success": False,
        "error": error.error,
        "code": error.status_code
    }), 403

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
     ({'code': 'unauthorized', 'description': 'Permission not found.'}, 403)
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
