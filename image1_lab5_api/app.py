from flask import Flask, request, jsonify
from flask_cors import CORS

# bring in the functions that talk to the database
from database import (
    create_db_table,
    insert_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user,
)

# create the flask app
app = Flask(__name__)

# allow requests from any website so the api can be called from a browser too
CORS(app, resources={r"/*": {"origins": "*"}})


# sends back a list of every user in the database
@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())


# finds one user by their id and sends their info back
@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))


# takes the new user from the request body and adds them to the database
@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    # read the user info that was sent as json
    user = request.get_json()
    return jsonify(insert_user(user))


# updates an existing user with the new info sent in the request
@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    # read the updated user info that was sent as json
    user = request.get_json()
    return jsonify(update_user(user))


# deletes the user that has the given id
@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))


# make sure the users table exists, then start the server on port 5000
if __name__ == "__main__":
    create_db_table()
    app.run(host="0.0.0.0", port=5000)
