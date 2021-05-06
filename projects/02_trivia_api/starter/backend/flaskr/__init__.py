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
    print("PAGE paginate", page)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE


    current_questions = selection[start:end]

    return current_questions

def retrieve_categories():
    categories = [category.format() for category in Category.query.order_by(Category.id).all()]
    dict = {}
    for category in categories:
        dict.update({category.get("id"):category.get("type")})

    return jsonify({
        "success":True,
        "categories": dict
    })


def create_app(test_config=None):
  # create and configure the app
    print("Hello, world!")
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})


  # '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # '''

    @app.route("/")
    def sample():
        return jsonify({
            "success": True
        })

  # '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        return response

    @app.route('/messages')
    @cross_origin()
    def get_messages():
        return jsonify({
            "success": True
        })
  #
  # '''
  # @TODO:
  # Create an endpoint to handle GET requests
  # for all available categories.
  # '''

    @app.route("/categories")
    def retrieve_categories():
        categories = [category.format() for category in Category.query.order_by(Category.id).all()]

        if len(categories) == 0:
            abort(404)

        dict = {}
        for category in categories:
            dict.update({category.get("id"):category.get("type")})

        return jsonify({
            "success":True,
            "categories": dict
        })

  #
  # '''
  # @TODO:
  # Create an endpoint to handle GET requests for questions,
  # including pagination (every 10 questions).
  # This endpoint should return a list of questions,
  # number of total questions, current category, categories.

    @app.route("/questions/", methods=["GET", "DELETE", "POST"])
    def retrieve_questions():
        questions = [question.format() for question in Question.query.order_by(Question.id).all()]
        page = request.args.get("page")
        # print("PAGE questions", page)
        print("retrieve questions")
        current_questions = paginate_questions(request, questions)


        if len(current_questions) == 0:
            abort(404)

        categories = [category.format() for category in Category.query.order_by(Category.id).all()]
        dict = {}
        for category in categories:
            dict.update({category.get("id"):category.get("type")})

        return jsonify({
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": dict,
            "current_category": None
        })

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions.
  # '''
  #
  # '''
  # @TODO:
  # Create an endpoint to DELETE question using a question ID.
  #
  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page.
  # '''

    @app.route("/questions/<id>", methods=["DELETE"])
    def delete_question(id):
        question = Question.query.get(id)
        print("QUESTION", question)

        if question is None:
            abort(422)

        question.delete()

        # return redirect(url_for("retrieve_questions"))
        return jsonify({
            "success":True
        })


  #
  # '''
  # @TODO:
  # Create an endpoint to POST a new question,
  # which will require the question and answer text,
  # category, and difficulty score.

    @app.route("/questions/submit", methods=["POST"])
    def post_new_question():

        body = request.get_json()
        print("BODY", body)

        answer = body.get("answer", None)
        question = body.get("question", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)

        if not answer or not question or not difficulty or not category:
            abort(400)

        question = Question(answer=answer, question=question, category=category, difficulty=difficulty)

        question.insert()

        return jsonify({
            "success":True,
            "answer": answer,
            "question": question.format(),
            "difficulty": difficulty,
            "category": category
        })



  # TEST: When you submit a question on the "Add" tab,
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.
  # '''
  #
  # '''
  # @TODO:
  # Create a POST endpoint to get questions based on a search term.
  # It should return any questions for whom the search term
  # is a substring of the question.
  #
  # TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  # Try using the word "title" to start.
  # '''
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        if body.get("searchTerm") != '':
            search = "%{}%".format(body.get("searchTerm"))
            questions_list = Question.query.filter(Question.question.ilike(search))
            questions = [question.format() for question in questions_list]
        else:
            questions = [question.format() for question in Question.query.order_by(Question.id).all()]

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(questions),
            "current_category": None
        })

  # '''
  # @TODO:
  # Create a GET endpoint to get questions based on category.
  #
  # TEST: In the "List" tab / main screen, clicking on one of the
  # categories in the left column will cause only questions of that
  # category to be shown.
  # '''

    @app.route("/categories/<id>/questions")
    def retrieve_questions_by_category(id):

        category = Category.query.get(id)
        # print("CATEGORY", category.format())
        if category is None:
            abort (404)

        list = Question.query.filter(Question.category == id).order_by(Question.difficulty).all()
        # print("LIST", list)

        questions = []
        for question in list:
            question = question.format()
            questions.append(question)
        # print(questions)
        # print(len(questions), category.format()["id"])

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(questions),
            "current_category": category.format()["id"]
        })


  #
  # '''
  # @TODO:
  # Create a POST endpoint to get questions to play the quiz.
  # This endpoint should take category and previous question parameters
  # and return a random questions within the given category,
  # if provided, and that is not one of the previous questions.

  #
  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not.
  # '''

    @app.route("/quizzes", methods=["POST"])
    def play_quizz():
        body = request.get_json()

        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")
        list_of_questions = []
        print("CAT QUIZZ", quiz_category["id"])

        if quiz_category["id"] != 0:
            data = Question.query.filter_by(category = quiz_category["id"]).all()
            questions = [question.format() for question in data]

            # if questions is None:
            #     abort(404)
            #
            # for question in questions:
            #     if question["id"] not in previous_questions:
            #         new_question = question
            #
            # return jsonify({
            #     "success": True,
            #     "question": new_question
            # })
        else:
            data = Question.query.all()
            questions = [question.format() for question in data]

        if questions is None:
            abort(404)

        for question in questions:
            if question["id"] not in previous_questions:
                new_question = question

        if len(previous_questions)+1 == len(questions):
            last_question = True
        else:
            last_question = False

        return jsonify({
            "success": True,
            "question": new_question,
            "last_question": last_question
        })




  # '''
  # @TODO:
  # Create error handlers for all expected errors
  # including 404 and 422.
  # '''

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
            "message": "You are trying to delete a question that does not exists in the database."
      }), 422

    return app
