import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:cavilosa1@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
        self.assertTrue(data["totalQuestions"])
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


    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
