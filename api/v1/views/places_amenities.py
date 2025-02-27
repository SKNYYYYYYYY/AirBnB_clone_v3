#!/usr/bin/python3
"""API endpoints for handling Place - Amenity relationships"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv

STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieve all Amenity objects linked to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if STORAGE_TYPE == "db":
        amenities = place.amenities
    else:
        amenities = [storage.get(Amenity, amenity_id) for amenity_id in place.amenity_ids]

    return jsonify([amenity.to_dict() for amenity in amenities if amenity])


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete an Amenity from a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if STORAGE_TYPE == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Link an Amenity to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if STORAGE_TYPE == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
