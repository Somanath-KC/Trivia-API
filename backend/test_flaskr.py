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
        self.database_path = "postgresql:///{}".format(self.database_name)
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


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('categories'))
        self.assertTrue(data.get('total_categories'))


    def test_get_questions_paginated(self):
        res = self.client().get('/questions')
        data = res.get_json()

        self.assertEqual(data.get('success'), True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('total_questions'))
        self.assertTrue(data.get('categories'))


    def test_get_questions_beyond_pagination(self):
        res = self.client().get('/questions?page=4444')
        data = res.get_json()

        self.assertEqual(data.get('success'), False)
        self.assertEqual(res.status_code, 404)


    def test_delete_question_of_id(self):
        # Adding Sample question to db and deleting that same question
        sample_question = {
                            'question': 'Is that true?', 
                            'answer': 'It\'s true', 
                            'difficulty': '2',
                            'category': 1
                          }

        post_response = self.client().post('/questions', json=sample_question)
        post_response_data = post_response.get_json()
        question_id = post_response_data.get('question_id')
        
        res = self.client().delete('/questions/{}'.format(question_id))
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)


    def test_delete_question_of_invalid_id(self):
        res = self.client().delete('/questions/{}'.format(99999))
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)


    def test_post_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'study'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('questions'))
        self.assertFalse(data.get('current_category'))
        self.assertTrue(data.get('total_questions'))


    def test_post_search_non_existing_term(self):
        res = self.client().post('/questions', json={'searchTerm': '943c34r435'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertFalse(data.get('questions'))
        self.assertEqual(data.get('total_questions'), 0)
        self.assertFalse(data.get('current_category'))


    def test_post_new_question(self):
        sample_question = {
                            'question': 'Is that true?', 
                            'answer': 'It\'s true', 
                            'difficulty': '2',
                            'category': 1
                          }

        res = self.client().post('/questions', json=sample_question)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('question_id'))


    def test_post_new_question_with_missing_data(self):
        # Required data 'category' is not being supplied in body
        sample_question = {
                            'question': 'Is that true?', 
                            'answer': 'It\'s true', 
                            'difficulty': '2'
                          }

        res = self.client().post('/questions', json=sample_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'), 400)
        self.assertTrue(data.get('message'))


    def test_post_new_question_with_invalid_data(self):
        # Category 1000 is not valid.
        sample_question = {
                            'question': 'Is that true?', 
                            'answer': 'It\'s true', 
                            'difficulty': '2',
                            'category': 1000
                          }

        res = self.client().post('/questions', json=sample_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error'), 422)
        self.assertTrue(data.get('message'))


    def test_get_questions_by_category(self):
        category = '1'
        res = self.client().get('/categories/{}/questions'.format(category))
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('total_questions'))
        self.assertEqual(data.get('current_category'), category)


    def test_get_questions_by_invalid_category(self):
        category = '99'
        res = self.client().get('/categories/{}/questions'.format(category))
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('error'), 404)
        self.assertTrue(data.get('message'))


    
        
        



        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()