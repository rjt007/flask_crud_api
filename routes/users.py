from flask import Blueprint, jsonify, request
from models.user import user_schema, schema_error
from config.db import connectDB
from bson.objectid import ObjectId

users_blueprint = Blueprint('users', __name__)

#database connection
db = connectDB()
collection = db.users

# Function to convert objectId to string for JSON serialization
def serialize_id(user):
    user['_id'] = str(user['_id'])
    return user

# Home route - for testing purpose
@users_blueprint.route('/', methods=['GET'])
def home():
    return jsonify({'success':'true'})

# Get all users
@users_blueprint.route('/users/', methods=['GET'])
def get_users():
    try:
        users = list(collection.find())
        serialized_users = [serialize_id(user) for user in users]
        return jsonify(serialized_users), 200
    except:
        return jsonify({'message':'Internal server error'}), 500

# Get a user by ID
@users_blueprint.route('/users/<string:id>/', methods=['GET'])
def get_user(id):
    try:
        user = collection.find_one({'_id': ObjectId(id)})
        return jsonify(serialize_id(user)), 200
    except:
        return jsonify({'message': 'User not found'}), 404


# Create a new user
@users_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
        
    try:
        user_data = user_schema.validate(data)
    except schema_error as err:
        return jsonify({'message': 'Invalid data', 'error': str(err)}), 400

    result = collection.insert_one(user_data)
    new_user = collection.find_one({'_id': result.inserted_id})
    return jsonify(serialize_id(new_user)), 201

# Update a user by ID
@users_blueprint.route('/users/<string:id>', methods=['PUT'])
def update_user(id):
    data = request.json
        
    try:
        user_data = user_schema.validate(data)
    except schema_error as err:
        return jsonify({'message': 'Invalid data', 'error': str(err)}), 400

    collection.update_one({'_id': ObjectId(id)}, {'$set': user_data})
    updated_user = collection.find_one({'_id': ObjectId(id)})
    if updated_user:
        return jsonify(serialize_id(updated_user)), 200
    else:
        return jsonify({'message': 'User not found'}), 404


# Delete a user by ID
@users_blueprint.route('/users/<string:id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404