"""
sql.py -- sql commands
======================
Used is database.py
"""

CREATE_FAVOURITES = """CREATE TABLE IF NOT EXISTS favourites(
                      id INTEGER PRIMARY KEY,
                      userid VARCHAR NOT NULL,
                      matchid VARCHAR NOT NULL)"""

SELECT_BY_USER  = "SELECT * FROM favourites WHERE userid=?"
SELECT_BY_MATCH = "SELECT * FROM favourites WHERE matchid=?"

INSERT_FAVOURITE = "INSERT INTO favourites VALUES (NULL, ?, ?)"
DELETE_FAVOURITE = "DELETE FROM favourites WHERE id=?"
