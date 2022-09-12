"""
sql.py -- sql commands
======================
Used is database.py
"""

CREATE_USERS = """CREATE TABLE IF NOT EXISTS users(
                      username VARCHAR PRIMARY KEY,
                      password VARCHAR NOT NULL)"""

CREATE_NOTES = """CREATE TABLE IF NOT EXISTS notes(
                      uuid VARCHAR PRIMARY KEY,
                      user VARCHAR NOT NULL,
                      ctime INT NOT NULL,
                      atime INT NOT NULL,
                      title VARCHAR NOT NULL,
                      text VARCHAR NOT NULL)"""

SELECT_USER = "SELECT * FROM users WHERE username=?"
INSERT_USER = "INSERT INTO users VALUES (?, ?)"
UPDATE_USER = """UPDATE users SET
                     password=?
                     WHERE username=?"""

SELECT_NOTE  = "SELECT * FROM notes WHERE uuid=?"
SELECT_NOTES = "SELECT * FROM notes WHERE user=? LIMIT ? OFFSET ?"
INSERT_NOTE  = "INSERT INTO notes VALUES (?,?,?,?,?,?)"
DELETE_NOTE  = "DELETE FROM notes WHERE uuid=?"
UPDATE_NOTE  = """UPDATE notes SET
                      user=?,
                      ctime=?,
                      atime=?,
                      title=?,
                      text=?
                      WHERE uuid=?"""
