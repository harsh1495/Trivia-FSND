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

  # cors = CORS(app)
  cors = CORS(app, resources={r"/categories*": {"origins": "*"}, r"/questions*": {"origins": "*"}, r"/quizzes": {"origins": "*"}, \
    r"/searchQuestions": {"origins": "*"}})


  @app.after_request
  def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [c.format() for c in categories]

    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "categories": {category.id: category.type for category in categories}
    })


  def pagination(request, data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_data = [d.format() for d in data]

    return formatted_data[start: end]


  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.all()

    formatted_questions = pagination(request, questions)

    if len(formatted_questions) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(questions),
      "categories": {category.id: category.type for category in categories},
      "current_category": None
    })


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      ques = Question.query.filter(Question.id == question_id).one_or_none()

      if ques is None:
        abort(404)

      ques.delete()

      questions = Question.query.order_by(Question.id).all()
      formatted_questions = pagination(request, questions)

      categories = Category.query.all()

      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(questions),
        "categories": {category.id: category.type for category in categories},
        "current_category": None
      })

    except:
      abort(404)


  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      question, answer, difficulty, category = request.get_json().get("question"), request.get_json().get("answer"), \
                                                request.get_json().get("difficulty"), request.get_json().get("category")

      # Abort if either of these fields is empty
      if not question or not answer or not difficulty or not category:
        abort(422)

      new_question = Question(question, answer, category, difficulty)
      new_question.insert()

      return jsonify({
        "success": True,
        "created": new_question.id
      })

    except:
      abort(422)


  @app.route('/searchQuestions', methods=['POST'])
  def search_question():
    try:
      search = "%{}%".format(request.get_json().get("searchTerm"))

      search_result = Question.query.filter(Question.question.ilike(search)).all()

      if not search_result:
        abort(404)

      formatted_questions = pagination(request, search_result)

      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(search_result),
        "current_category": None
      })

    except:
      abort(404)


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category_id(category_id):
    try:
      questions = Question.query.filter_by(category=category_id).order_by(Question.id).all()
      formatted_questions = pagination(request, questions)

      category = Category.query.filter(Category.id == category_id).one_or_none()

      if len(formatted_questions) == 0:
        abort(404)

      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(questions),
        "current_category": category.type
      })

    except:
      abort(404)


  def generate_question(questions, previous_questions):
    '''
    Returns a randomly selected question from the list of questions if it has not been asked before
    @param questions: List of questions queried from the database
    @param previous_questions: List of previous question ids sent from the frontend
    '''
    idx = random.randint(0, len(questions)-1)

    q_id = questions[idx].id

    if len(previous_questions) >= len(questions):
      return None

    while q_id in previous_questions:
      idx = random.randint(0, len(questions)-1)
      q_id = questions[idx].id

    q = questions[idx].format()

    return q

  @app.route('/quizzes', methods=['POST'])
  def play_trivia():
    try:
      category, previous_questions = request.get_json().get('quiz_category'), request.get_json().get('previous_questions')

      if category.get("id") == 0:
        questions = Question.query.order_by(Question.id).all()
        q = generate_question(questions, previous_questions)

      else:
        questions = Question.query.filter_by(category=category.get("id")).order_by(Question.id).all()
        q = generate_question(questions, previous_questions)

      return jsonify({
          "success": True,
          "question": q,
        })

    except:
      abort(422)


  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable request"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400

  return app

