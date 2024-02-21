import json

import requests
from flask import Flask, request, jsonify
import hashlib
import time
import re
import JWT

app = Flask(__name__)

dict_mapping_multi_users = {'username':{"id":"url"}}
users = {'user1': 'password1', 'user2': 'password2'}
auth_url = "http://127.0.0.1:5001"
end_point = "/"
check = "check"
auth_check_url = f"{auth_url}{end_point}{check}"

# def verify_jwt_in_request():
#     """verify JWT in request header"""
#     token = request.headers.get('Authorization', None)
#     if not token:
#         return False, "Missing token"
#     try:
#         payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
#         # add more verification here if needed
#         return True, payload
#     except jwt.ExpiredSignatureError:
#         return False, "Token expired"
#     except jwt.InvalidTokenError:
#         return False, "Invalid token"

# @app.route('/your-protected-route', methods=['GET', 'POST'])
# def protected_route():
#     """protected route"""
#     is_valid, payload_or_error = verify_jwt_in_request()
#     if not is_valid:
#         return jsonify({"error": payload_or_error}), 401

#     return jsonify({"message": "Success"})


#function to generate the id for the url
def generate_md5_identifier(url):
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    md5_identifier = md5.hexdigest()
    # limit the length of the identifier to 5
    return md5_identifier[:5]

# def generate_unique_md5_identifier(url):
#     while True:
        # dict_mapping[identifier] = url
        # return identifier
        # identifier = generate_md5_identifier(url)
        # # check if identifier is unique
        # if identifier not in dict_mapping:
        #     dict_mapping[identifier] = url
        #     return identifier
        # else:
        #     # if collision detected, regenerate identifier
        #     print("Collision detected for identifier:", identifier)
        #     print("Regenerating identifier...")
        #     continue



def is_valid(url):
    regex = re.compile(
        r'^(https?:\/\/)'  # Protocol (must be http or https)
        r'([\w\.-]+)'      # Subdomain and domain name (letters, digits, underscores, dots, and hyphens)
        r'(\.[a-zA-Z]{2,10})'  # Top-level domain (letters, length from 2 to 10)
        r'(\/[\w\.-]*)*'   # Path (optional, letters, digits, underscores, dots, and hyphens)
        r'(\/[\w\.-]*\([\w\.-]*\))*'  # Path with parentheses (optional, used for matching URLs like Wikipedia)
        r'(\/[\w\.-]*)*'   # Path (optional, letters, digits, underscores, dots, and hyphens)
        r'(\?[&\w\.-=]*)?' # Query parameters (optional)
)
    return re.match(regex, url) is not None


@app.route('/<id>', methods=['GET'])
#get_url function to get the url from the id
def get_url(id):
    #if id is present in the dictionary then return the url
    start_time = time.time()
    token = request.headers.get('Authorization')
    print("!!!!!!!!!!!!!!!!!",token)
    response = requests.put(auth_check_url, json={"token": token})
    response_json = response.json()
    check_auth = response_json['status']
    if check_auth == True:
        user = response_json['user']
        if user in dict_mapping_multi_users:
            dict_mapping = dict_mapping_multi_users[user]
        else:
            dict_mapping_multi_users[user] = {}
        if id in dict_mapping:
            data = {}
            data["value"] = dict_mapping[id]
            json_data = jsonify(data)
            # print(json_data)
            end_time = time.time()
            # Calculate elapsed time
            elapsed_time = end_time - start_time
            print("Elapsed get time: ", elapsed_time)
            return json_data, 301
        #if id is not present in the dictionary then return the error
        else:
            end_time = time.time()
            # Calculate elapsed time
            elapsed_time = end_time - start_time
            print("Elapsed get time: ", elapsed_time)
            return "URL not found", 404
    else:
        return jsonify({'detail':"forbidden" }), 403



@app.route('/<id>', methods=['PUT'])
#update_url function to update the url from the id
def update_url(id):
    global dict_mapping_multi_users
    token = request.headers.get('Authorization')
    # print("!!!!!!!!!!!!!!!!!",token)
    response = requests.put(auth_check_url, json={"token": token})
    response_json = response.json()
    check_auth = response_json['status']
    if check_auth == True:
        user = response_json['user']
        if user not in dict_mapping_multi_users:
            dict_mapping_multi_users[user] = {}

        #if id is present and user is authorized then update the url
        try:
            values = request.data
            values = values.decode('utf-8')
            values = json.loads(values)
            # values = request.get_json()
            new_redirect_url = values["url"]
        #if url is not provided then return the error
        except KeyError:
            # print("No url provided")
            return "error", 400
        if id not in dict_mapping_multi_users[user]:
            return "ID does not exist", 404
        #if url is not valid then return the error
        if not is_valid(new_redirect_url):
            return "error", 400
        #if url is valid then update the url
        dict_mapping_multi_users[user][id] = new_redirect_url
        # print(id,dict_mapping)
        return "update success", 200
    else:
        return jsonify({'error': 'Unauthorized'}), 403


@app.route('/<id>', methods=['DELETE'])
#delete_url function to delete the url from the id
def delete_url(id):
    global dict_mapping_multi_users
    token = request.headers.get('Authorization')
    response = requests.put(auth_check_url, json={"token": token})
    response_json = response.json()
    check_auth = response_json['status']
    if check_auth == True:
        user = response_json['user']
        if user not in dict_mapping_multi_users:
            dict_mapping_multi_users[user] = {}
    #if id is present in the dictionary then delete the url
        if id in dict_mapping_multi_users[user]:
            # print(dict_mapping)
            dict_mapping_multi_users[user] = {}
            # print(dict_mapping)
            return "URL deleted successfully", 204
        #if id is not present in the dictionary then return the error
        else:
            return "ID doesn't found", 404
    else:
        return jsonify({'error': 'Unauthorized'}), 403


@app.route('/', methods=['GET'])
#function to get all the urls
def get_all_urls():
    token = request.headers.get('Authorization')
    response = requests.put(auth_check_url, json={"token": token})
    response_json = response.json()
    check_auth = response_json['status']
    if check_auth == True:
        user = response_json['user']
        if user in dict_mapping_multi_users:
            dict_mapping = dict_mapping_multi_users[user]
        else:
            dict_mapping_multi_users[user] = {}
        return jsonify(dict_mapping), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 403


@app.route('/', methods=['POST'])
#function to create the id for the url
def create_id():
    start_time = time.time()
    data = request.json
    url_to_shorten = data.get('value')
    #if url is valid then create the id
    token = request.headers.get('Authorization')
    print("!!!!!!!!!!!!!!!!!",token)
    response = requests.put(auth_check_url, json={"token": token})
    response_json = response.json()
    print(response_json)

    check_auth = response_json['status']
    if check_auth == True:
        user = response_json['user']
        if user not in dict_mapping_multi_users:
            dict_mapping_multi_users[user] = {}
        if is_valid(url_to_shorten):
            id = generate_md5_identifier(url_to_shorten)
            dict_mapping_multi_users[user][id] = url_to_shorten
            end_time = time.time()
            # Calculate elapsed time
            elapsed_time = end_time - start_time
            print("Elapsed create id time: ", elapsed_time)
            return jsonify({"id": id}), 201

        #if url is not valid then return the error
        else:
            end_time = time.time()
            # Calculate elapsed time
            elapsed_time = end_time - start_time
            print("Elapsed create id time: ", elapsed_time)
            return "error", 400
    else:
        return jsonify({'error': 'Unauthorized'}), 403


@app.route('/', methods=['DELETE'])
#function to delete all the urls
def delete_all_urls():
    global dict_mapping_multi_users
    token = request.headers.get('Authorization')
    response = requests.put(auth_check_url, json={"token": token})
    response_json = response.json()
    check_auth = response_json['status']
    if check_auth == True:
        user = response_json['user']
        if user in dict_mapping_multi_users:
            dict_mapping_multi_users[user] = {}
            return "All URLs deleted", 404
        else:
            dict_mapping_multi_users[user] = {}
            return "All URLs deleted", 404
    # print(dict_mapping)
    else:
        return jsonify({'error': 'Unauthorized'}), 403


if __name__ == '__main__':
    app.run(debug=True,port=5001)