#!/usr/bin/python3
"""module for Amenities that interacts with the Amenity model in the database"""
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Gets the list of all Amenity objects"""
    all_amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in all_amenities]

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Gets an Amenity object with the given ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object with the given ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    request_data = request.get_json()
    if 'name' not in request_data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**request_data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an existing Amenity object with the given ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    request_data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    storage.save()

    return jsonify(amenity.to_dict()), 200
