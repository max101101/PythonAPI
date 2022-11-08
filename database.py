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
    cursor.execute(sql.CREATE_FAVOURITES)
    cursor.execute(sql.CREATE_NOTIFICATIONS)
    conn.commit()
    conn.close()


def get_favourites_by_userid(conn, userid):
    """get favourites by userid"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_FAVOURITES_BY_USER, (userid,))
    favourites = cursor.fetchall()
    if favourites is None:
        return None

    return favourites

def get_favourites_by_matchid(conn, matchid):
    """get favourites by matchid"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_FAVOURITES_BY_MATCH, (matchid,))
    favourites = cursor.fetchall()
    if favourites is None:
        return None

    return favourites


def add_favourite(conn, userid, matchid):
    """add favourite"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_FAVOURITE, (userid, matchid))

def delete_favourite(conn, id):
    """delete favourite"""

    cursor = conn.cursor()
    cursor.execute(sql.DELETE_FAVOURITE, (id,))


def get_notification(conn, matchid):
    """get notification"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_NOTIFICATION, (matchid,))
    return cursor.fetchone()


def add_notification(conn, matchid):
    """add notification"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_NOTIFICATION, (matchid, 0))
 

def update_notification(conn, matchid, events):
    """update notification"""

    cursor = conn.cursor()
    cursor.execute(sql.UPDATE_NOTIFICATION, (events, matchid))
 
