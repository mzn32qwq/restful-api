import json
# import os

from flask import Flask, request, jsonify
import hashlib
import JWT
from datetime import datetime, timedelta

app = Flask(__name__)

# USER_SHORT_URL_FILE = os.getenv('USER_SHORT_URL_FILE')
USER_SHORT_URL_FILE = "/auth/file/url_short.json"

def load_users():
    try:
        with open(USER_SHORT_URL_FILE, 'r+') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_SHORT_URL_FILE, 'w') as file:
        json.dump(users, file)

users = load_users()

def hash_password(password):
    """hash password with sha256"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/users', methods=['POST'])
def create_user():
    global users
    users = load_users()
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'detail': "duplicate"}), 409
    users[username] = {'password': hash_password(password)}
    save_users(users)
    return jsonify({'message': 'User created'}), 201

@app.route('/users', methods=['PUT'])
def change_password():
    global users
    users = load_users()
    data = request.json
    username = data.get('username')
    old_password = data.get('password')
    new_password = data.get('new_password')

    if username not in users or users[username]['password'] != hash_password(old_password):
        return jsonify({'detail':"forbidden" }), 403

    users[username]['password'] = hash_password(new_password)
    save_users(users)
    return jsonify({'message': 'Password changed'}), 200

@app.route('/users/login', methods=['POST'])
def login():
    global users
    users = load_users()

    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username]['password'] == hash_password(password):
        payload = {
    "sub": password ,
    "name": username,
    "iat":  datetime.utcnow(), # issued at time
    "exp":  datetime.utcnow()+ timedelta(hours=1) # set expiration to 1 hour
}
        token = JWT.create_jwt(payload, "your_secret_key")
        return jsonify({'token': token}), 200

    return jsonify({'detail': "forbidden"}), 403


if __name__ == '__main__':
    app.run(debug=True, port=5001,host="0.0.0.0")
