from flask import Flask, request, jsonify
import pymongo

app = Flask(__name__)

mongo = pymongo.MongoClient('mongodb+srv://aadesh:aadesh@cluster0-8gkj3.mongodb.net/test?retryWrites=true&w=majority')
mongo_db = mongo['placement']
mongo_collection = mongo_db['users']

@app.route('/placements/v1', methods=["GET"])
@app.route('/placements/v1/', methods=["GET"])
def info_view():
    """List of routes for this API."""
    output = {
        'info': 'GET /placements/v1',
        'all users': 'GET /placements/v1/users',
        'login': 'POST /placements/v1/users',
        'register': 'POST /placements/v1/users/register',
        'edit profile': 'PUT /placements/v1/users'
    }
    return jsonify(output)

@app.route('/placement/v1/users/', methods = ["GET"])
@app.route('/placement/v1/users', methods = ["GET"])
def display_users():
    users = mongo_collection.find()
    response = {}
    for user in users:
        user['_id'] = str(user['_id'])
        response[user['_id']] = user
    print(response)
    return response

@app.route('/placement/v1/users/', methods = ["POST"])
@app.route('/placement/v1/users', methods = ["POST"])
def login():
    user_details = request.json

    user = mongo_collection.find_one({'username': user_details['username']})
    print(user)
    if user != None:
        if user['password'] == user_details['password']:
            return "True"
        else:
            return "Password is Wrong"
    else:
        return "User Doesn't Exists"

@app.route('/placement/v1/users/register/', methods = ["POST"])
@app.route('/placement/v1/users/register', methods = ["POST"])
def register():
    user_details = request.json

    doc_id = mongo_collection.insert_one(user_details)
    if doc_id != None:
        return "Resgitered"
    else:
        return "Network Error"

@app.route('/placement/v1/users/', methods = ["PUT"])
@app.route('/placement/v1/users', methods = ["PUT"])
def edit_profile():
    user_details = request.json

    updating_para1 = { 'username': user_details['username'] }
    updating_para2 = { '$set': { 'password': user_details['password'] } }
    mongo_collection.update_one(updating_para1, updating_para2)
    return "Successful"

if __name__ == '__main__':
    app.run(debug = 'true')