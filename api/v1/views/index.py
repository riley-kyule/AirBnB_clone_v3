#!/usr/bin/python3
"""
This is our first views file to serve status and stats route
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
import json

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/status', methods=['GET'])
def get_status():
    """Serves the route /status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def get_count():
    """Returns count of items in storage"""
    a = {}

    for k, v in classes.items():
        a[k] = storage.count(v)
    return jsonify(a)
