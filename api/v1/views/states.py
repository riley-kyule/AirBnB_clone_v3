#!/usr/bin/python3
""" States objects view handles all states related API actions"""
from flask import jsonify
from flask import abort
from flask import request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def states():
    """Returns all states obj in json format """
    try:
        all_states = storage.all(State)
        states_list = []
        for state in all_states:
            states_list.append(all_states[state].to_dict())
        return jsonify(states_list)
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves individual states obj based on id"""
    try:
        state = storage.get(State, state_id)
        dictionary = state.to_dict()
        return jsonify(dictionary)
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def del_state(state_id):
    """ Deletes a state obj"""
    try:
        storage.delete(State, state_id)
        storage.save()
        return {}, 200
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state obj"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    return jsonify(state.save().to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ modifies state obj"""
    state = 'State.' + str(state_id)
    all_obj = storage.all()
    if state not in all_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if i not in ['created_at', 'id', 'updated_at']:
            setattr(storage.all()[i], k, v)
    storage.all()[i].save()
    a = storage.get(State, state_id)
    return jsonify(a.to_dict(), 200)
