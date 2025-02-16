#!/usr/bin/python3
"""
Contains the states' view
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import jsonify, abort, request#!/usr/bin/python3
"""
Contains the states' view
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import jsonify, abort, request


# 1
@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def retrieve_places(city_id):
    """Retrieves the list of all place objects of a specific State"""
    place = storage.get(City, city_id)
    if not place:
        abort(404)
    places = [place.to_dict() for place in place.cities]
    return jsonify(places)


# 2
@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """gets the place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


# 3
@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes the place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


# 4
@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place():
    """create a new place"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing name")
    if 'user_id' not in data:
        abort(400, description="Missing name")

    new_city = City(name=data['name'])
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


# 5
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a state"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = {"id", "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200



# 1 get LIST
@app_views.route('/place',
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
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'email' not in data:
        abort(400, description="Missing password")

    new_user = User(name=data['name'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


# 5
@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
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
