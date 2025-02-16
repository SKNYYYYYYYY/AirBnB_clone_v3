#!/usr/bin/python3
"""
Contains the states' view
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


# 1
@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_cities(state_id):
    """Retrieves the list of all City objects of a specific State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# 2
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """gets the state object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


# 3
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes the state object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


# 4
@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city():
    """create a new state"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
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
