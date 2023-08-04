from flask import Blueprint, jsonify, request, make_response
from flask_restful import Resource, Api
from models.user import user_schema, schema_error
from config.db import connectDB
from bson.objectid import ObjectId

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

#database connection
db = connectDB()
collection = db.users

# Function to convert objectId to string for JSON serialization
def serialize_id(user):
    user['_id'] = str(user['_id'])
    return user

# UsersResource for GET all users and POST new user
class UsersResource(Resource):

    def get(self):
        try:
            users = list(collection.find())
            serialized_users = [serialize_id(user) for user in users]
            return make_response(jsonify(serialized_users), 200)
        except:
            return make_response(jsonify({'message':'Internal server error'}), 500)
    
    def post(self):
        data = request.json
        print(data)
            
        try:
            user_data = user_schema.validate(data)
        except schema_error as err:
            return make_response(jsonify({'message': 'Invalid data', 'error': str(err)}), 400)

        result = collection.insert_one(user_data)
        new_user = collection.find_one({'_id': result.inserted_id})
        return make_response(jsonify(serialize_id(new_user)), 201)

# UserResource for GET, PUT and DELETE a user
class UserResource(Resource):

    def get(self, id):
        try:
            user = collection.find_one({'_id': ObjectId(id)})
            return make_response(jsonify(serialize_id(user)), 200)
        except:
            return make_response(jsonify({'message': 'User not found'}), 404)
    
    def put(self, id):
        data = request.json
            
        try:
            user_data = user_schema.validate(data)
        except schema_error as err:
            return make_response(jsonify({'message': 'Invalid data', 'error': str(err)}), 400)

        collection.update_one({'_id': ObjectId(id)}, {'$set': user_data})
        updated_user = collection.find_one({'_id': ObjectId(id)})
        if updated_user:
            return make_response(jsonify(serialize_id(updated_user)), 200)
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)

    def delete(self, id):
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return make_response(jsonify({'message': 'User deleted successfully'}), 200)
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)


# Adding Resources to api
api.add_resource(UsersResource, '/')
api.add_resource(UserResource, '/<string:id>/')