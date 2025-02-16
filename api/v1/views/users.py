#!/usr/bin/python3
"""
Contains the states' view
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.amenity import Amenity
from flask import jsonify, abort, request


# 1 get LIST
@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def retrieve_users():
    """Retrieves the list of all vusers objects of a specific State"""
    user = storage.all(User)
    return jsonify([user.to_dict() for user in user.values()])


# 2 GET OBJEct
@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """gets the users' object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


# 3 DELETE
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes the user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# 4 POST
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """create a new user"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    new_user = User(name=data['name'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


# 5
@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(user_id):
    """update a amenity"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = {"id", "email" "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
