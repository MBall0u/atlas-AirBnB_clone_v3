#!/usr/bin/python3
"""module for Cities that interacts with the City model in the database"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        return abort(407)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return abort(406)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return abort(405)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        return abort(404)

    if not request.is_json:
        return abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        return abort(400, description="Missing name")

    city = City(**data, state_id=state_id)
    storage.new(city)
    storage.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        return abort(408)

    if not request.is_json:
        return abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict()), 200
