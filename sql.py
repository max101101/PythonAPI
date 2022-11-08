"""
sql.py -- sql commands
======================
Used is database.py
"""

CREATE_FAVOURITES = """CREATE TABLE IF NOT EXISTS favourites(
                       id INTEGER PRIMARY KEY,
                       userid VARCHAR NOT NULL,
                       matchid VARCHAR NOT NULL)"""

SELECT_FAVOURITES_BY_USER  = "SELECT * FROM favourites WHERE userid=?"
SELECT_FAVOURITES_BY_MATCH = "SELECT * FROM favourites WHERE matchid=?"

INSERT_FAVOURITE = "INSERT INTO favourites VALUES (NULL, ?, ?)"
DELETE_FAVOURITE = "DELETE FROM favourites WHERE id=?"


CREATE_NOTIFICATIONS = """CREATE TABLE IF NOT EXISTS notifications(
                          matchid VARCHAR PRIMARY KEY,
                          events INTEGER NOT NULL)"""

SELECT_NOTIFICATION = "SELECT * FROM notifications WHERE matchid=?"

INSERT_NOTIFICATION = "INSERT INTO notifications VALUES (?, ?)"

UPDATE_NOTIFICATION = """UPDATE notifications SET
                         events=?
                         WHERE matchid=?"""
