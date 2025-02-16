#!/usr/bin/python3
"""
Contains the states' view
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from flask import jsonify, abort, request


# 1 get LIST
@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def retrieve_amenities():
    """Retrieves the list of all amenity objects of a specific State"""
    amenity = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenity.values()])


# 2 GET OBJEct
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """gets the amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


# 3 DELETE
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes the amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# 4 POST
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create a new amenity"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(name=data['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


# 5
@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = {"id", "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
