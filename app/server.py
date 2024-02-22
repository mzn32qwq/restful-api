from flask import Flask, request, jsonify
import hashlib
import JWT
from datetime import datetime, timedelta

app = Flask(__name__)

users = {}

def hash_password(password):
    """hash password with sha256"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/users', methods=['POST'])
def create_user():
    global users
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'detail': "duplicate"}), 409

    users[username] = hash_password(password)
    return jsonify({'message': 'User created'}), 201

@app.route('/users', methods=['PUT'])
def change_password():
    global users
    data = request.json
    username = data.get('username')
    old_password = data.get('password')
    new_password = data.get('new_password')

    if username not in users or users[username] != hash_password(old_password):
        return jsonify({'detail':"forbidden" }), 403

    users[username] = hash_password(new_password)
    return jsonify({'message': 'Password changed'}), 200

@app.route('/users/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == hash_password(password):
        payload = {
    "sub": password ,
    "name": username,
    "iat":  datetime.utcnow(), # issued at time
    "exp":  datetime.utcnow()+ timedelta(hours=1) # set expiration to 1 hour
}
        token = JWT.create_jwt(payload, "your_secret_key")
        return jsonify({'token': token}), 200

    return jsonify({'detail': "forbidden"}), 403
@app.route('/check', methods=['PUT'])
def check():
    data = request.json
    token = data.get('token')
    if not JWT.verify_jwt(token):
        return jsonify({"status": False, "user": "Unauthorized"})
    checkusername = JWT.return_username(token)
    if checkusername not in users:
        return jsonify({"status": False, "user": "User not found"})
    return jsonify({"status": True, "user": checkusername})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

