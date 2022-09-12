"""
database.py -- db interface
=================================
Used in server.py
"""

import sql

def dict_factory(cursor, row):
    """Return DB tuple as dict"""

    res = {}
    for idx, col in enumerate(cursor.description):
        res[col[0]] = row[idx]

    return res


def init(conn):
    """"Initializes DB state"""

    cursor = conn.cursor()
    cursor.execute(sql.CREATE_USERS)
    cursor.execute(sql.CREATE_NOTES)
    conn.commit()
    conn.close()


def get_user(conn, username):
    """get user by username"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_USER, (username,))
    return cursor.fetchone()


def add_user(conn, user):
    """add new user"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_USER, (user['username'], user['password']))


def update_user(conn, user):
    """update existing user"""

    cursor = conn.cursor()
    cursor.execute(sql.UPDATE_USER, (
        user['password'],
        user['username']
    ))

def get_note(conn, uuid):
    """get note by uuid"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_NOTE, (uuid,))
    note = cursor.fetchone()
    if note is None:
        return None

    return note

def get_notes(conn, username, limit, offset):
    """get notes by username"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_NOTES, (username, limit, offset))
    notes = cursor.fetchall()
    if notes is None:
        return None

    return notes

def add_note(conn, note):
    """add new note"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_NOTE, (
        note['uuid'],
        note['user'],
        note['ctime'],
        note['atime'],
        note['title'],
        note['text']
    ))


def update_note(conn, note):
    """update existing note"""

    cursor = conn.cursor()
    cursor.execute(sql.UPDATE_NOTE, (
        note['user'],
        note['ctime'],
        note['atime'],
        note['title'],
        note['text'],
        note['uuid']
    ))


def delete_note(conn, uuid):
    """delete existing note"""

    cursor = conn.cursor()
    cursor.execute(sql.DELETE_NOTE, (uuid,))
