"""
All functions related to database work.
"""
import sqlite3
from flask import g
from init_db import DATABASE_FILE_PATH


def get_db():
    """
    Returns the database connection for the current request.
    The connection is opened on first use and reused for the rest of the request.
    It is closed automatically by close_db when the request ends.

    :return: The database connection.
    :rtype: sqlite3.Connection
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_FILE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exception=None):
    """
    Closes the request's database connection, if one was opened.
    Registered with app.teardown_appcontext, so it runs even if the request failed.

    :param exception: The unhandled exception, if any (unused).
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()
