import json
from flask import Flask, request, jsonify
import hashlib
import time
import re
import JWT

app = Flask(__name__)

# dict_mapping_multi_users = {'username_example':{"id":"url"}}
# auth_check_url = f"{auth_url}{end_point}{check}"

# USER_SHORT_URL_FILE = os.getenv('USER_SHORT_URL_FILE')
USER_SHORT_URL_FILE = "/auth/file/url_short.json"

def load_url_id():
    try:
        with open(USER_SHORT_URL_FILE, 'r+') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_url_id(users):
    with open(USER_SHORT_URL_FILE, 'w') as file:
        json.dump(users, file)

dict_mapping_multi_users = load_url_id()

#function to generate the id for the url
def generate_md5_identifier(url):
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    md5_identifier = md5.hexdigest()
    # limit the length of the identifier to 5
    return md5_identifier[:5]


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

def check(token):
    dict_mapping_multi_users = load_url_id()
    print(dict_mapping_multi_users)
    if not JWT.verify_jwt(token):
        return  False
    checkusername = JWT.return_username(token)
    # print(checkusername)
    if checkusername not in dict_mapping_multi_users:
        return  False
    return checkusername


@app.route('/<id>', methods=['GET'])
#get_url function to get the url from the id
def get_url(id):
    global dict_mapping_multi_users
    dict_mapping_multi_users = load_url_id()
    #if id is present in the dictionary then return the url
    start_time = time.time()
    # get token from request
    token = request.headers.get('Authorization')
    # check validity of the token and get the current username
    check_auth = check(token)
    if check_auth != False:
        user = check_auth
        # base on the username get dic
        if 'short_url' not in dict_mapping_multi_users[user]:
            dict_mapping_multi_users[user]['short_url'] = {}
            save_url_id(dict_mapping_multi_users)
            return "ID not found", 404
        if id in dict_mapping_multi_users[user]['short_url']:
            data = {}
            data["value"] = dict_mapping_multi_users[user]['short_url'][id]
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
            return "ID not found", 404
    else:
        return jsonify({'detail':"forbidden" }), 403


@app.route('/<id>', methods=['PUT'])
#update_url function to update the url from the id
def update_url(id):
    global dict_mapping_multi_users
    dict_mapping_multi_users = load_url_id()
    token = request.headers.get('Authorization')
    check_auth = check(token)
    # if id is present and user is authorized then update the url
    if check_auth!= False:
        user = check_auth
        if 'short_url' not in dict_mapping_multi_users[user]:
            dict_mapping_multi_users[user]['short_url'] = {}
            save_url_id(dict_mapping_multi_users)
            return "ID does not exist", 404
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
        if id not in dict_mapping_multi_users[user]['short_url']:
            return "ID does not exist", 404
        #if url is not valid then return the error
        if not is_valid(new_redirect_url):
            return "error", 400
        #if url is valid then update the url
        dict_mapping_multi_users[user]['short_url'][id] = new_redirect_url
        save_url_id(dict_mapping_multi_users)
        # print(id,dict_mapping)
        return "update success", 200
    else:
        return jsonify({'error': 'Unauthorized'}), 403


@app.route('/<id>', methods=['DELETE'])
#delete_url function to delete the url from the id
def delete_url(id):
    global dict_mapping_multi_users
    dict_mapping_multi_users = load_url_id()
    token = request.headers.get('Authorization')
    check_auth = check(token)
    if check_auth!= False:
        user = check_auth
        if 'short_url' not in dict_mapping_multi_users[user]:
            dict_mapping_multi_users[user]['short_url'] = {}
            save_url_id(dict_mapping_multi_users)
            return "URL deleted successfully", 204
    #if id is present in the dictionary then delete the url
        if id in dict_mapping_multi_users[user]['short_url']:
            # print(dict_mapping)
            dict = dict_mapping_multi_users[user]['short_url']
            del dict[id]
            print(dict)
            dict_mapping_multi_users[user]['short_url'] = dict
            save_url_id(dict_mapping_multi_users)
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
    global dict_mapping_multi_users
    dict_mapping_multi_users = load_url_id()
    token = request.headers.get('Authorization')
    check_auth = check(token)
    # check validity and return urls corresponding username
    if check_auth!= False:
        user = check_auth
        print(user,type(user))
        if 'short_url' not in dict_mapping_multi_users[user]:
            dict_mapping_multi_users[user]['short_url'] = {}
            save_url_id(dict_mapping_multi_users)
        return jsonify(dict_mapping_multi_users[user]['short_url']), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 403


@app.route('/', methods=['POST'])
#function to create the id for the url
def create_id():
    global dict_mapping_multi_users
    dict_mapping_multi_users = load_url_id()
    start_time = time.time()
    data = request.json
    url_to_shorten = data.get('value')
    token = request.headers.get('Authorization')
    check_auth = check(token)
    #if url is valid then create the id
    if check_auth!= False:
        user = check_auth
        # if user is not exist,create a new dic for new user to store urls/ids
        if 'short_url' not in dict_mapping_multi_users[user]:
            dict_mapping_multi_users[user]['short_url'] = {}
            save_url_id(dict_mapping_multi_users)
            dict_mapping_multi_users = load_url_id()
        if is_valid(url_to_shorten):
            id = generate_md5_identifier(url_to_shorten)
            dict_mapping_multi_users[user]['short_url'][id] = url_to_shorten
            save_url_id(dict_mapping_multi_users)
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
    dict_mapping_multi_users = load_url_id()
    token = request.headers.get('Authorization')
    check_auth = check(token)
    # check the validity and get user, only delete current user's dic of urls/ids
    if check_auth!= False:
        user = check_auth
        if 'short_url' not in dict_mapping_multi_users[user]:
            dict_mapping_multi_users[user]['short_url'] = {}
            save_url_id(dict_mapping_multi_users)
            return "All URLs deleted", 404
        else:
            dict_mapping_multi_users[user]['short_url'] = {}
            save_url_id(dict_mapping_multi_users)
            return "All URLs deleted", 404
    else:
        return jsonify({'error': 'Unauthorized'}), 403


if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run(debug=True,port=5000,host="0.0.0.0")