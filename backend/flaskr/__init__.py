import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO:[COMPLETED] Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"*": {"origin": "*"}})


    '''
    @TODO:[COMPLETED] Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')

        return response


    '''
    @TODO:[COMPLETED] 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def get_all_categories():

        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
          abort(404)

        return jsonify({
          'success': True,
          'categories': [category.type for category in categories],
          'total_categories': len(categories)
        })


    '''
    @TODO:[COMPLETED] 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def get_questions():

      number_of_questions_per_page = 10
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * number_of_questions_per_page
      end = start + number_of_questions_per_page

      questions = Question.query.order_by(Question.id).all()

      questions_paginated = [question.format() for question in questions][start:end]

      if len(questions_paginated) == 0:
          abort(404)

      categories = [category.type for category in Category.query.order_by(Category.id).all()]
      
      # Current Category Refrence:
      # https://knowledge.udacity.com/questions/82424

      return jsonify({
          'success': True,
          'questions': questions_paginated,
          'total_questions': len(questions),
          'current_category': None,
          'categories': categories
      })


    '''
    @TODO:[COMPLETED]
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_with_id(question_id):
        
        question = Question.query.get(question_id)
        
        # If question with given id is not in db.
        if not question:
            abort(404)

        try:
          question.delete()
        except Exception as e:
          # Print exception for debugging
          print(e)
          abort(422)
        
        return jsonify({
            'success': True
        })
        

    '''
    @TODO: [COMPLETED]
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    # POST REQUEST FOR NEW QUESTION AND SEARCH ACTION
    # WERE DEFINED IN ONE FUNCTION  post_question()
    
    '''
    @TODO: [COMPLETED]
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions', methods=['POST'])
    def post_question():

        post_data = request.get_json()
        
        # Checks weather post request is made for search or not
        if post_data.get('searchTerm', False):
            search_term_filter = Question.question.ilike('%{}%'.format(post_data.get('searchTerm')))
            questions = Question.query.filter(search_term_filter).all()

            return jsonify({
                'success': True,
                'questions': [item.format() for item in questions],
                'total_questions': len(questions),
                'current_category': None
            })

        else:
            # Check weather question and answer text, 
            # category, and difficulty score were available in body
            # Adds only if values of that key is not empty
            required_post_data = {key: post_data[key] for key in post_data if post_data[key]}

            # Refrence: 
            #         https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
            if len(required_post_data.keys()) < 4:
                # 400: The post data is a bad request since it 
                # dose not include required fields. 
                abort(400)

            # Using dictionary Unpacking to assign attribuites
            question = Question(**required_post_data)

            try:
              question.insert()
            except:
              abort(422)

            return jsonify({
                'success': True,
                'question_id': question.id
            }), 201


    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<category_id>/questions')
    def get_questions_by_category(category_id):

        questions = Question.query.filter(Question.category == category_id).all()

        if len(questions) == 0:
          abort(404)

        return jsonify({
            'success': True,
            'questions': [item.format() for item in questions],
            'total_questions': len(questions),
            'current_category': category_id
        })


    '''
    @TODO:[COMPLETED]
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        
        post_data = request.get_json()

        previous_questions = post_data.get('previous_questions', list())
        quiz_category = post_data.get('quiz_category').get('id')
        category_id = int(quiz_category)

        # Category id = 0 refers to all categories
        if category_id == 0:
            query_result = Category.query.all()
            category_id = [item.id for item in query_result]
        else:
            query_result = Category.query.filter(Category.id == category_id).all()
            category_id = [item.id for item in query_result]
        
        # Querys all questions in current category 
        # and questions not in previous questions 
        # Reference: 
        # https://stackoverflow.com/questions/20060485/sqlalchemy-select-using-reverse-inclusive-not-in-list-of-child-column-values
        current_category_questions = Question.category.in_(category_id)
        not_in_previous_questions = ~Question.id.in_(previous_questions)
        print(previous_questions)
        questions = Question.query.filter(current_category_questions, not_in_previous_questions).all()

        # The Game will end if user answered 5 or no more questions available
        if len(previous_questions) == 5 or len(questions) == 0:
            return jsonify({
                'success': True
            })

        # Selects the question randomly
        random_id = random.randint(0, len(questions)-1)

        return jsonify({
            'success': True,
            'question': questions[random_id].format()
        })


    '''
    @TODO:[COMPLETED]
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found_error(error):

        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def request_unprocessable(error):

        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(400)
    def not_acceptable(error):

      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad Request'
      }), 400

    @app.errorhandler(500)
    def server_error(error):

        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Error in API'
        }), 500


    return app

    