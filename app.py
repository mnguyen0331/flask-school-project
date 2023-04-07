# Student's name: Phu Nguyen
# Course: CPSC 449-01 13991
# Assignment: Midterm Project
# Date: April 07, 2023

from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
import pymysql
import jwt
import os


app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = '5ff71db551be42be945fc0d3a5af46aa'

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password="",
    db='',
    cursorclass=pymysql.cursors.DictCursor
)
cur = conn.cursor()

# Uploaded file config
# Path to the uploads folder
app.config['UPLOAD_PATH'] = os.getcwd() + '/uploads'
# Limit the file size to 1 megabyte
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# Only accept images that has these extentions
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']


# Check for JWT token
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # Check for token in headers
        if 'token' in request.headers:
            token = request.headers['token']
            try:
                # decode the token
                payload = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms="HS256")
                # get username from payload
                username = payload['username']
                # find user that has that username in db
                cur.execute(
                    'SELECT * FROM users WHERE username = % s', (username))
                user = cur.fetchone()
                return func(user, *args, **kwargs)
            except:
                return unauthorized("Invalid token")
        # Not found
        else:
            return unauthorized("Missing token")
    return decorated

# login endpoint
@app.route('/login', methods=['POST'])
def login():
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Query to get users that has username and password provided in submit form
        cur.execute(
            'SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        user = cur.fetchone()
        # If user is found
        if user:
            # Generates a JWT token
            token = jwt.encode({
                'username': username,
                'exp': datetime.utcnow() + timedelta(minutes=5)
            }, app.config['SECRET_KEY'])
            # Return a token
            return make_response(jsonify({'token': token}), 201)
        # User is not found
        else:
            return unauthorized("Username or password is incorrect")
    # Username or password is empty
    return bad_request("Username and password cannot be empty")

# upload endpoint
@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    # Sanitize file name
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        # Get file's extension
        file_ext = os.path.splitext(filename)[1]
        # Check the extension
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return bad_request(f"{filename} is not an image")
        # If everything is good, then save the file to uploads folder
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return 'Upload file succeeded'
    return bad_request('Please attach a file before submit')


# public endpoint
# does not required authentication
@app.route('/public')
def public():
    public_items = ['item1', 'item2', 'item3']
    return public_items

# admin endpoint
# required authentication
@app.route('/admin')
@token_required
def admin(user):
    return 'Hello ' + user['username']

# Error handler functions
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(401)
def unauthorized(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"), debug=True)
