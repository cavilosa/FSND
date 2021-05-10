
from dotenv import load_dotenv
load_dotenv()

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

password = os.environ.get("password")

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        self.new_question = {
            "question": "What are we eating?",
            "answer": "What What",
            "difficulty": 1,
            "category": 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_retrieve_categories(self):
        pass
        """Getting all categories"""
        res = self.client().get("/categories")
        data = json.loads(res.data)
        categories = Category.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["categories"]))


    def test_404_categories(self):
        """404 getting questions"""
        res = self.client().get("/categories/?page=3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["messages"], "resource not found")
        self.assertEqual(data["error"], 404)


    def test_retrieving_questions(self):
        """TESTING GETTING QUESTIONS"""
        res = self.client().get("/questions/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertIsNone(data["current_category"])

    def test_retrieving_questions(self):
        """TESTING GETTING QUESTIONS page 2"""
        res = self.client().get("/questions/?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertIsNone(data["current_category"])


    def test_404_retrieve_questions(self):
        """404 getting questions"""
        res = self.client().get("/questions/?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["messages"], "resource not found")
        self.assertEqual(data["error"], 404)


    # def test_delete_question(self):
    #     """DELETING A QUESTION BY ID"""
    #     res = self.client().delete("/questions/5")
    #     questions = Question.query.all()
    #     question = Question.query.get(5)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertIsNone(question)


    def test_404_question(self):
        """DELETING NOT FOUND QUESTION"""
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)
        question = Question.query.get(6)

        self.assertEqual(res.status_code, 422)
        self.assertIsNone(question)
        self.assertFalse(data["success"])
        self.assertEqual(data["messages"], "You are trying to delete a question that does not exists in the database.")
        self.assertEqual(data["error"], 422)



    def test_add_question(self):
        """ADDING A NEW QUESTION"""
        res = self.client().post("/questions/submit", json=self.new_question)
        data = json.loads(res.data)

        questions = [question.format() for question in Question.query.all()]
        list = []
        for question in questions:
            list.append(question["id"])
        question = Question.query.filter(Question.answer == "What What").first().format()["id"]

        self.assertEqual(res.status_code, 200)
        self.assertIn(question, list)

    def test_error_adding_question(self):
        """ERROR ADDING QUESTION"""

        res = self.client().post("/questions/submit", json = {})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"],  "bad request")
        self.assertEqual(data["error"], 400)


    def test_questions_by_category(self):
        """GETTING QUESTIONS FROM A CATEGORY"""
        res = self.client().get("/categories/3/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])


    def test_404_questions_by_category(self):
        """Error getting questions by category"""
        res = self.client().get("/categories/7/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["messages"], "resource not found")
        self.assertEqual(data["error"], 404)

    def test_search_questions(self):
        """TESTONG SEARCH QUESTIONS"""
        res = self.client().post("/questions/search", json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNone(data["current_category"])
        self.assertIsNotNone(data["questions"])
        self.assertIsNotNone(data["total_questions"])

    def test_404_search_questions(self):
        "SEARCH QUESTIONS FAIL"
        res = self.client().post("/questions/search", json={"search": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_quizzes(self):
        """TESTING QUIZZES"""
        res = self.client().post("/quizzes/", json= {'previous_questions': [], 'quiz_category': {'type': 'History', 'id': '4'},
                                'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment',
                                '6': 'Sports'}}
                                )
        data = json.loads(res.data)
        print("DATA categories", data)
        self.assertTrue(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNotNone(data["question"])
        self.assertEqual(data["question"]["id"], 23)

    def test_quizzes(self):
        """FAILING QUIZZES"""
        res = self.client().post("/quizzes/", json={'previous_questions': [], 'quiz_category': {'type': 'History', 'id': '9'},
                                   'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment',
                                   '6': 'Sports'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["messages"], "resource not found")
        self.assertEqual(data["error"], 404)







    def tearDown(self):
        """Executed after each test"""
        # psql -d trivia_test -U postgres -a -f trivia.psql
        pass




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
