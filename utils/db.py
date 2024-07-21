"""
All functions related to database work.
"""
import sqlite3

def get_db_connection():
    """
    Connecting to the SQLite database.

    :return: The database connection.
    :rtype: object
    """
    conn = sqlite3.connect("./data/database.db")
    conn.row_factory = sqlite3.Row
    return conn