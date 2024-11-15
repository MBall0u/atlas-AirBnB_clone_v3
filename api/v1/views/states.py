#!/usr/bin/python3
"""module for States that interacts with the State model in the database"""
from flask import jsonify, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Gets a list of all State objects"""
    all_states = storage.all(State).values()
    states_list = [state.to_dict() for state in all_states]

    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Gets a single State object with the given ID"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False
    )
def delete_state(state_id):
    """Deletes a single State object with the given ID"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, description="Not a JSON")

    if 'name' not in request_data:
        abort(400, description="Missing name")

    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object with the given ID"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    request_data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
