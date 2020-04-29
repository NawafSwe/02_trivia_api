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
        self.database_path = "postgresql://{}/{}".format('postgres:@5466771$#@localhost:5432', self.database_name)
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


    
    def test_404_sent_requesting_questions_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_with_result(self):
        response = self.client.get('/categories')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']),6)

    def test_delete_question(self):
         deleted_question = Question(question='do you love udacity?'
         , answer='yes I do so much',category=2,difficulty=1)
          ## i want to test it in case of successfully deleted
         deleted_question.insert()
         
         response = self.client().delete(f'/questions/{ deleted_question.id}')
         data = json.loads(response.data)
         selection = Question.query.filter(
             Question.id == deleted_question.id
         ).one_or_none()

         self.ssertEqual(response.status_code,200)
         self.assertEqual(data['success'],True)
         self.assertEqual(data['delete'],str(deleted_question))
         self.assertEqual(selection,None) ## does not exist any more ;; 


    def test_get_categories_with_no_result(self):
        response = self.client.get('/categories')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']),0)

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'],True)
        self.assertTrue(len(data['questions']))
    def test_422_delete_non_exist_question(self):
        response = self.client().delete('/questions/100')
        data = json.loads(response.data)

        self.assertEqual(response.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'processable')
    
    def test_create_question(self):
       ## question = Question(question='do you love udacity?',answer='yes of course',category=1,difficulty=2)
        response = self.client().post('/questions',json={'question': 'do you love udacity','answer' : 'yes of course','category' : 1, 
        'difficulty': 2})
        data = self.json(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
    def test_searching_for_question(self):
        response = self.client.post('/search',json={'search':'love python'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'],0)
        self.assertEqual(len(data['questions']),0)
        ### testing that the search do not match ;;
        
        

    


# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()