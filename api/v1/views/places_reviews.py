#!/usr/bin/python3
"""
Contains the states' view
"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from flask import jsonify, abort, request


# 1
@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def retrieve_place_reviews(place_id):
    """Retrieves the list of all place objects of a specific State"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_reviews = [place_review.to_dict() for place_review in place.reviews]
    return jsonify(place_reviews)


# 2
@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_place_review(review_id):
    """gets the place object"""
    place_review = storage.get(Review, review_id)
    if not place_review:
        abort(404)
    return jsonify(place_review.to_dict())


# 3
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place_review(review_id):
    """deletes the place object"""
    place_review = storage.get(Review, review_id)
    if not place_review:
        abort(404)
    storage.delete(place_review)
    storage.save()
    return jsonify({}), 200


# 4/
@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_place_review(place_id):
    """create a new place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'text' not in data:
        abort(400, description="Missing text")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_place_review = Place(
        text=data['text'],
        place_id=place_id,
        user_id=data['user_id'])
    storage.new(new_place_review)
    storage.save()
    return jsonify(new_place_review.to_dict()), 201


# 5
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_place_review(review_id):
    """update a state"""
    place_review = storage.get(Review, review_id)
    if not place_review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = {"id", "user_id", "place_id" "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place_review, key, value)
    storage.save()
    return jsonify(place_review.to_dict()), 200
