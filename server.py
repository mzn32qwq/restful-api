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
    # get data from request
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # check if username already exists
    if username in users:
        return jsonify({'detail': "duplicate"}), 409

    # create new user
    users[username] = hash_password(password)
    return jsonify({'message': 'User created'}), 201


@app.route('/users', methods=['PUT'])
def change_password():
    # get data from request
    data = request.json
    username = data.get('username')
    old_password = data.get('password')
    new_password = data.get('new_password')

    # check if username exists and old password is correct
    if username not in users or users[username] != hash_password(old_password):
        return jsonify({'detail':"forbidden" }), 403

    # change password
    users[username] = hash_password(new_password)
    return jsonify({'message': 'Password changed'}), 200



@app.route('/users/login', methods=['POST'])
def login():
    # get data from request
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # check if username and password exist in the table
    if username in users and users[username] == hash_password(password):
        payload = {
    "sub": password ,
    "name": username,
    "iat":  datetime.utcnow(), # issued at time
    "exp":  datetime.utcnow()+ timedelta(hours=1) # set expiration to 1 hour
}
        # generate JWT
        token = JWT.create_jwt(payload, "your_secret_key")
        return jsonify({'token': token}), 200

    # return 403 if username and password do not exist in the table
    return jsonify({'detail': "forbidden"}), 403

# check if JWT is valid and user exists
@app.route('/check', methods=['PUT'])
def check(token):
    #if token is not valid then return the error
    if not JWT.verify_jwt(token):
        return jsonify({"Status": False, "User": "Unauthorized"})
    #if token is valid then return the user
    checkusername = JWT.return_username(token)
    if checkusername not in users:
        #if user is not present then return the error
        return jsonify({"Status": False, "User": "User not found"})
    #if user is present then return the user
    return jsonify({"Status": True, "User": checkusername})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

