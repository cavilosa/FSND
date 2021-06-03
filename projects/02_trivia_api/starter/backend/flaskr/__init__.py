import os
from flask import Flask, request, abort, jsonify
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = selection[start:end]

    return current_questions


def retrieve_categories():
    categories = [category.format()
                  for category in Category.query.order_by(Category.id).all()]
    dict = {}
    for category in categories:
        dict.update({category.get("id"): category.get("type")})

    return jsonify({
        "success": True,
        "categories": dict
    })


def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

# after_request decorator to sets Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        return response

    @app.route('/messages')
    @cross_origin()
    def get_messages():
        return jsonify({
            "success": True
        })


# endpoint to handle GET requests for all available categories


    @app.route("/categories")
    def retrieve_categories():
        categories = [category.format()
                      for category in Category.query.order_by(Category.id).all()]

        if len(categories) == 0:
            abort(404)

        dict = {}
        for category in categories:
            dict.update({category.get("id"): category.get("type")})

        return jsonify({
            "success": True,
            "categories": dict
        })


# Endpoint to handle GET requests for questions, including pagination.


    @app.route("/questions/", methods=["GET"])
    def retrieve_questions():
        questions = [question.format()
                     for question in Question.query.order_by(Question.id).all()]
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = [category.format()
                      for category in Category.query.order_by(Category.id).all()]
        dict = {}
        for category in categories:
            dict.update({category.get("id"): category.get("type")})

        return jsonify({
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": dict,
            "current_category": None
        })


# Endpoint to DELETE question using a question ID.


    @app.route("/questions/<id>", methods=["DELETE"])
    def delete_question(id):
        question = Question.query.get(id)

        if question is None:
            abort(422)

        question.delete()

        return jsonify({
            "success": True
        })


# Endpoint to post a new question with text, category and difficulty score.


    @app.route("/questions/submit", methods=["POST"])
    def post_new_question():
        body = request.get_json()

        answer = body.get("answer", None)
        question = body.get("question", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)

        if not answer or not question or not difficulty or not category:
            abort(400)

        question = Question(
            answer=answer,
            question=question,
            category=category,
            difficulty=difficulty)

        question.insert()

        return jsonify({
            "success": True,
            "answer": answer,
            "question": question.format(),
            "difficulty": difficulty,
            "category": category
        })


# POST endpoint to get questions based on a search term.


    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()

        if body.get("searchTerm"):
            search = "%{}%".format(body.get("searchTerm"))
            questions_list = Question.query.filter(
                Question.question.ilike(search))
            questions = [question.format() for question in questions_list]

            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
                "current_category": None
            })

        else:
            abort(404)


# GET endpoint to get questions based on category.


    @app.route("/categories/<id>/questions")
    def retrieve_questions_by_category(id):

        category = Category.query.get(id)
        if category is None:
            abort(404)

        list = Question.query.filter(
            Question.category == id).order_by(
            Question.difficulty).all()

        questions = []
        for question in list:
            question = question.format()
            questions.append(question)

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(questions),
            "current_category": category.format()["id"]
        })


# POST endpoint to get questions to play the quiz.


    @app.route("/quizzes/", methods=["POST"])
    def play_quizz():
        body = request.get_json()

        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")
        categories = body.get("categories")

        if int(
                quiz_category["id"]) == 0:  # fetch all questions for all the categories
            data = Question.query.all()
            questions = [question.format() for question in data]

        elif int(quiz_category["id"]) > 0 and int(quiz_category["id"]) <= len(categories):
            data = Question.query.filter_by(category=quiz_category["id"]).all()
            questions = [question.format() for question in data]
        else:
            abort(404)

        if len(previous_questions) == len(questions) + 1:
            last_question = True
        else:
            last_question = False

        for question in questions:
            if question["id"] not in previous_questions:
                new_question = question

        #
        if len(questions) == len(previous_questions):
            new_question = ''
            last_question = True

        return jsonify({
            "success": True,
            "question": new_question,
            "last_question": last_question,
            "questions": len(questions)
        })

  # Handlers for all expected errors

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "messages": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "messages": "You are trying to delete a question that does not exists in the database."
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "messages": "Internal server error."
        }), 500

    return app
