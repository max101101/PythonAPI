#!/usr/bin/env python3
"""
server.py -- http api server
========================
Http api server
"""


import sqlite3
from time import time
from flask import Flask, jsonify, abort, request, make_response, g

import database
import properties

APP = Flask(__name__)

def conn_get():
    """Return DB connection, creates connection if needed"""

    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(properties.db_name)
        conn.row_factory = database.dict_factory

    return conn


@APP.teardown_appcontext
def conn_close(_):
    """Close DB connection"""

    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()


@APP.errorhandler(400)
def bad_request(_):
    """400 status wrapper"""

    return make_response(jsonify({'error': 'Bad Request'}), 400)


@APP.errorhandler(409)
def conflict(_):
    """409 status wrapper"""

    return make_response(jsonify({'error': 'Conflict'}), 409)


@APP.errorhandler(406)
def not_acceptable(_):
    """406 status wrapper"""

    return make_response(jsonify({'error': 'Not Acceptable'}), 406)


@APP.errorhandler(404)
def not_found(_):
    """404 status wrapper"""

    return make_response(jsonify({'error': 'Not Found'}), 404)


@APP.errorhandler(500)
def internal(_):
    """500 status wrapper"""
    return make_response(jsonify({'error': 'Internal Error'}), 500)


@APP.route('/api/v1/add_favourite', methods=['POST'])
def add_favourite():
    """
    Api.add_favourite method
    arguments: [userid, matchid]
    returns: []
    201 -- note created
    400 -- wrong arguments
    500 -- internal error
    """

    if not request.json or not 'userid' in request.json or not 'matchid' in request.json:
        abort(400)

    conn = conn_get()
    database.add_favourite(conn, request.json["userid"], request.json["matchid"])
    conn.commit()

    return jsonify({}), 200


@APP.route('/api/v1/get_favourite', methods=['POST'])
def get_favourite():
    """
    Api.get_favourite method
    arguments: [userid]
    returns: [[id, userid, matchid]]
    200 -- ok
    400 -- wrong arguments
    500 -- internal error
    """
    if not request.json or not 'userid' in request.json:
        abort(400)

    conn = conn_get()
    favourites = database.get_favourites_by_userid(conn, request.json['userid'])
    conn.commit()

    return jsonify(favourites)


@APP.route('/api/v1/delete_favourite', methods=['POST'])
def delete_favourite():
    """
    Api.delete_favourite method
    arguments: [id]
    returns: []
    200 -- ok
    400 -- wrong arguments
    500 -- internal error
    """
    if not request.json or not 'id' in request.json:
        abort(400)

    conn = conn_get()
    database.delete_favourite(conn, request.json['id'])
    conn.commit()

    return jsonify({})


if __name__ == '__main__':
    database.init(sqlite3.connect(properties.db_name))
    APP.run(debug=False)
