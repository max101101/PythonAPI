#!/usr/bin/env python3
"""
server.py -- http api server
========================
Http api server for smg client
Provides auth and notebook api
Validates game state
"""


import sqlite3
#from multiprocessing import Process
from time import time
from uuid import uuid1

from flask import Flask, jsonify, abort, request, make_response, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import database
import properties

APP = Flask(__name__)
AUTH = HTTPBasicAuth()


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


@AUTH.error_handler
def forbidden():
    """403 status wrapper"""

    return make_response(jsonify({'error': 'Forbidden'}), 403)


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


@AUTH.verify_password
def verify_password(username, password):
    """Validate password"""

    conn = conn_get()
    user = database.get_user(conn, username)
    if user is None:
        return False

    return check_password_hash(user['password'], password)


@APP.route('/api/v1/health_check', methods=['GET'])
def health_check():
    """
    Api.health_check method
    returns status "ok" or fails
    """

    return jsonify({"status": "ok"})


@APP.route('/api/v1/auth', methods=['GET'])
@AUTH.login_required
def authenticate():
    """
    Api.auth method
    arguments: []
    returns: empty body
    200 -- auth success
    403 -- wrong authorization
    500 -- internal error
    """

    return ""


@APP.route('/api/v1/auth', methods=['PUT'])
def register():
    """
    Api.register method
    arguments: [username, password]
    returns: empty body
    201 -- registration success
    400 -- wrong arguments
    409 -- username exists
    500 -- internal error
    """

    if not request.json \
            or not 'username' in request.json or len(request.json['username']) == 0 \
            or not 'password' in request.json or len(request.json['password']) == 0:
        abort(400)

    if not request.json['username'].isalnum() or not request.json['password'].isalnum():
        abort(400)

    print(request.json['password'])

    conn = conn_get()
    user = database.get_user(conn, request.json['username'])
    if user is not None:
        abort(409)

    user = {
        'username': request.json['username'],
        'password': generate_password_hash(request.json['password']),
    }
    database.add_user(conn, user)
    conn.commit()

    return "", 201


@APP.route('/api/v1/auth', methods=['POST'])
@AUTH.login_required
def change_password():
    """
    Api.change_password method
    arguments: [password]
    returns: empty body
    200 -- password changed
    400 -- wrong arguments
    403 -- wrong authorization
    500 -- internal error
    """

    if not request.json or not 'password' in request.json or len(request.json['password']) == 0:
        abort(400)

    if not request.json['password'].isalnum():
        abort(400)

    conn = conn_get()
    user = database.get_user(conn, AUTH.username())
    user['password'] = generate_password_hash(request.json['password'])
    database.update_user(conn, user)
    conn.commit()

    return ""


@APP.route('/api/v1/note', methods=['PUT'])
@AUTH.login_required
def create_note():
    """
    Api.create_note method
    arguments: [title, text]
    returns: [uuid, user, ctime, atime, title, text]
    201 -- note created
    400 -- wrong arguments
    403 -- wrong authorization
    500 -- internal error
    """

    if not request.json or not 'text' in request.json or not 'title' in request.json:
        abort(400)

    conn = conn_get()
    note = {
        'uuid':  str(uuid1()),
        'user':  AUTH.username(),
        'ctime': int(time()),
        'atime': int(time()),
        'title': request.json["title"],
        'text':  request.json["text"]
    }
    database.add_note(conn, note)
    conn.commit()

    return jsonify(note), 201


@APP.route('/api/v1/note', methods=['GET'])
@AUTH.login_required
def get_notes():
    """
    Api.get_notes method
    arguments: [limit, offset]
    returns: [[uuid, user, ctime, atime, title, text]]
    200 -- ok
    400 -- wrong arguments
    403 -- wrong authorization
    500 -- internal error
    """

    limit = int(request.args.get('limit'))
    if limit is None or limit < 0 or limit > 100:
        limit = 20

    offset = int(request.args.get('offset'))
    if offset is None or offset < 0:
        offset = 0

    conn = conn_get()
    notes = database.get_notes(conn, AUTH.username(), limit, offset)
    conn.commit()

    return jsonify(notes)


@APP.route('/api/v1/note/<string:uuid>', methods=['GET'])
@AUTH.login_required
def get_note(uuid):
    """
    Api.get_note method
    returns: [uuid, user, ctime, atime, title, text]
    200 -- ok
    403 -- wrong authorization
    404 -- note not found
    500 -- internal error
    """

    conn = conn_get()
    note = database.get_note(conn, uuid)
    if note is None:
        abort(404)

    if AUTH.username() != note["user"]:
        abort(403)

    return jsonify(note)


@APP.route('/api/v1/note/<string:uuid>', methods=['POST'])
@AUTH.login_required
def update_note(uuid):
    """
    Api.update_note method
    arguments: [title, text]
    returns: [uuid, user, ctime, atime, title, text]
    200 -- note updated
    400 -- wrong arguments
    403 -- wrong authorization
    404 -- note not found
    500 -- internal error
    """

    conn = conn_get()
    note = database.get_note(conn, uuid)
    if note is None:
        abort(404)

    if AUTH.username() != note["user"]:
        abort(403)

    if not request.json or not 'text' in request.json or not 'title' in request.json:
        abort(400)

    note["atime"] = int(time())
    note["title"] = request.json["title"]
    note["text"] = request.json["text"]
    database.update_note(conn, note)
    conn.commit()

    return jsonify(note)


@APP.route('/api/v1/note/<string:uuid>', methods=['DELETE'])
@AUTH.login_required
def delete_note(uuid):
    """
    Api.update_note method
    returns: empty body
    204 -- note deleted
    403 -- wrong authorization
    404 -- note not found
    500 -- internal error
    """

    conn = conn_get()
    note = database.get_note(conn, uuid)
    if note is None:
        abort(404)

    if AUTH.username() != note["user"]:
        abort(403)

    database.delete_note(conn, note["uuid"])
    conn.commit()

    return "", 204


if __name__ == '__main__':
    database.init(sqlite3.connect(properties.db_name))
    APP.run(debug=False)
