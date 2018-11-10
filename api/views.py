from flask import Flask, request, jsonify
import json
import uuid
import re
from db import DatabaseConnection
from api.models import User, Answer, Questions
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
#something
app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'KenG0W@Da4!'

db = DatabaseConnection()


@app.route('/api/v1/questions', methods=['POST'])
@jwt_required
def post_question():
    username = get_jwt_identity()
    info = request.get_json()

    question = info.get('question')

    if not question or question.isspace():
        return jsonify({'message': 'Enter a question.'}), 400

    question_db = db.check_question(username)

    for Question in question_db:
        if Question[0] == question:
            return jsonify({'message': 'Please be creative. You can not ask the same question twice.'})

    db.insert_question(question, username)

    return jsonify({
        'Question': question
    }), 201


@app.route('/api/v1/questions', methods=['GET'])
@jwt_required
def get_all_questions():
    db = DatabaseConnection()
    question_db = db.get_all_questions()

    if question_db == None:
        return jsonify({
            'message': 'There are no questions yet.'
        }), 400
    else:
        return jsonify({
            'Question': [question for question in question_db]
        }), 201


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
@jwt_required
def post_answer(questionId):
    try:
        info = request.get_json()
        username = get_jwt_identity()

        answer = info.get('answer')

        if not answer and answer.isspace():
            return jsonify({'message': 'Please enter an answer.'}), 400

        db = DatabaseConnection()
        db.insert_answer(answer, username, questionId)

        return jsonify({
            'message': 'Answer added succesfully.'
        }), 201
    except IndexError:
        return jsonify({'message': 'The question does not exist'}), 400


@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
@jwt_required
def get_one_qn(questionId):
    try:
        db = DatabaseConnection()
        question = db.get_one_question(questionId)
        answers = db.get_answers(questionId)

        print(type(answers))

        if question == None:
            return jsonify({'message': 'Question doesn\'t exist'}), 400

        return jsonify({
            'Question': question,
            'Answer': [answer for answer in answers],
            'message': 'Question fetched succesfully.',
        }), 200
    except TypeError:
        return jsonify({'message': 'Question Id must be a number.'}), 400


@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId):
    try:
        username = get_jwt_identity()

        db = DatabaseConnection()
        question = db.get_one_question(questionId)

        if question[2] == username:
            db.delete_question(questionId, username)
            return jsonify({'message': 'Question deleted succesfully.'}), 200
        else:
            return jsonify({'message': 'You don\'t have permission to delete this question.'}), 400
    except TypeError:
        return jsonify({'message': 'Question does not exist.'}), 400


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    info = request.get_json()

    username = info.get('username')
    password = info.get('password')

    if not username or username.isspace():
        return jsonify({
            'message': 'Enter a valid username.'
        }), 400
    if not password or password.isspace():
        return jsonify({
            'message': 'Enter a valid password.'
        }), 400

    db = DatabaseConnection()
    user = db.login(username)

    if check_password_hash(user[3], password) and user[1] == username:
        access_token = create_access_token(identity=username)
        return jsonify({
            'token': access_token,
            'message': '{} has logged in.'.format(username)
        }), 200
    else:
        return jsonify({'message': 'Wrong login credentials.'}), 400


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    info = request.get_json()

    username = info.get('username')
    email = info.get('email')
    password = info.get('password')
    userId = uuid.uuid4()
    password_hash = generate_password_hash(password, method='sha256')

    if not username or username.isspace():
        return jsonify({'message': 'Username field can not be empty.'}), 400

    if not email or email.isspace():
        return jsonify({'message': 'Email field can not be empty.'}), 400
    elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
        return jsonify({'message': 'Enter a valid email address.'}), 400

    if not password or password.isspace():
        return jsonify({'message': 'Password field can not be left empty.'}), 400
    elif len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters.'}), 400

    db = DatabaseConnection()
    email_db = db.check_email(email)
    username_db = db.check_username(username)

    if username_db != None:
        return jsonify({'message': 'This username already has an account.'}), 400
    if email_db != None:
        return jsonify({'message': 'This email is already taken.'}), 400
    db.insert_users(userId, username, email, password_hash)
    access_token = create_access_token(username)

    return jsonify({
        'access_token': access_token,
        'message': '{} has been registered succesfully.'.format(username)
    })


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['PUT'])
@jwt_required
def preferred_answer(questionId, answerId):
    username = get_jwt_identity()
    db = DatabaseConnection()
    question_username = db.asked(questionId)
    answer_username = db.answered(answerId, questionId)

    if username == question_username[0]:
        db.preferred(username)
    elif username == answer_username[0]:
        info = request.get_json()
        new_answer = info.get('new_answer')

        db.edit_answer(new_answer, username, questionId)
    else:
        return jsonify({'message': 'You don\'t have permission to be here.'}), 400

@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['GET'])
@jwt_required
def get_an_answer(questionId, answerId):
    db = DatabaseConnection()
    answer = db.get_an_answer(questionId)
    question = db.get_a_question(questionId)

    if question == None:
        return jsonify({'message': 'Question does not exist.'})
    if answer == None:
        return jsonify({'message': 'Answer does not exist'})

    return jsonify({
        'Question': question,
        'Answer': answer
    })


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'The URL entered does not exist.'})
