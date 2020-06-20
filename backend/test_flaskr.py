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
        self.database_path = "postgres://{}:{}@{}/{}".format('triviatestuser', 'triviatestpass123','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["questions"])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_sent_invalid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_by_category_id(self):
        test_category = "Science"
        category = Category.query.filter(Category.type == test_category).one_or_none()
        category_id = category.id

        res = self.client().get('/categories/' + str(category_id) + '/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'Science')

    def test_get_questions_by_category_id_404_error(self):
        category_id = 1000

        res = self.client().get('/categories/' + str(category_id) + '/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_question(self):
        data = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 1
        }

        res = self.client().post('/questions', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_question_error_422(self):
        data = {
            'question': 'test question',
            'difficulty': 2,
            'category': 1
        }

        res = self.client().post('/questions', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable request")

    def test_delete_question(self):
        data = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 1
        }

        res = self.client().post('/questions', json=data)
        data = json.loads(res.data)

        res = self.client().delete('/questions/{}'.format(data["created"]))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_error_404(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_question(self):
        data = {
            'searchTerm': 'the',
        }
        res = self.client().post('/searchQuestions', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_question_error_404(self):
        data = {
            'searchTerm': 'ndjahskj',
        }
        res = self.client().post('/searchQuestions', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_play_trivia(self):
        data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Sports',
                'id': 6
            }
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_play_trivia_error_422(self):
        data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Sports',
                'id': 16
            }
        }
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()