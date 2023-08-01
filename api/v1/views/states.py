#!/usr/bin/python3
""" view for State objects"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.state import State
from models import storage


@app_views.route('/states',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def states(state_id=None):
    """Retrieves a list of state objects"""

    state_objs = storage.all(State)

    states = [obj.to_dict() for obj in state_objs.values()]
    if not state_id:
        if request.method == 'GET':
            return jsonify(states)
        elif request.method == 'POST':
            data = request.get_json()

            if data is None:
                abort(400, 'Not a JSON')
            if data.get("name") is None:
                abort(400, 'Missing name')
            new = State(**data)
            new.save()
            return jsonify(new.to_dict()), 201
    else:
        if request.method == 'GET':
            for state in states:
                if state.get('id') == state_id:
                    return jsonify(state)
            abort(404)
        elif request.method == 'PUT':
            data = request.get_json()

            if data is None:
                abort(400, 'Not a JSON')

            for state in state_objs.values():
                if state.id == state_id:
                    state.name = data.get("name")
                    state.save()
                    return jsonify(state.to_dict()), 200
            abort(404)

        elif request.method == 'DELETE':
            for obj in state_objs.values():
                if obj.id == state_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
