from flask import Flask, request, jsonify
import hashlib
import jwt
import datetime

app = Flask(__name__)

users = {}

def hash_password(password):
    """hash password with sha256"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'detail': "duplicate"}), 409

    users[username] = hash_password(password)
    return jsonify({'message': 'User created'}), 201

@app.route('/users', methods=['PUT'])
def change_password():
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
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, 'your_secret_key', algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'detail': "forbidden"}), 403

if __name__ == '__main__':
    app.run(debug=True, port=5001)

