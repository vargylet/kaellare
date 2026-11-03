"""
All functions related to locations.
"""
import sqlite3
from flask import flash
from utils.db import get_db

def get_all_locations():
    """
    Fetching and returning all locations.

    :return: A list of the locations.
    :rtype: list
    """
    return get_db().execute(
        "SELECT locationId, locationName "
        "FROM locations "
        "ORDER BY locationName ASC"
    ).fetchall()

def get_location(location_id):
    """
    Fetching and returning one location.

    :param location_id: The location's database ID.
    :type location_id: int
    :return: The location's name.
    :rtype: tuple
    """
    return get_db().execute(
        "SELECT locationName "
        "FROM locations "
        "WHERE locationId = ?",
        (location_id,)
    ).fetchone()

def create_location(name):
    """
    Creates a new location in the database.

    :param name: The location's name.
    :type name: str
    :return: A flash message with the outcome.
    :rtype: str
    """
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO locations (locationName) "
            "VALUES (?)",
            (name,)
        )
        conn.commit()
    except sqlite3.IntegrityError as integrity_error:
        flash(
            f"An error occurred. Location wasn't saved due to a database integrity error: "
            f"{str(integrity_error)}",
            "error"
        )
    except sqlite3.DatabaseError as db_error:
        flash(f"A database error occured. Location wasn't saved. {str(db_error)}", "error")
    else:
        flash(f"{name} has been added.", "info")

def update_location(location_id, new_name):
    """
    Updates the name of a location in the database.

    :param location_id: The location's database ID.
    :type location_id: int
    :param new_name: The new name we want to give the location.
    :type new_name: string
    :return: A flash message with the outcome.
    :rtype: str
    """
    try:
        conn = get_db()
        conn.execute(
            "UPDATE locations "
            "SET locationName = ? "
            "WHERE locationId = ?",
            (new_name, location_id)
        )
        conn.commit()
    except sqlite3.IntegrityError as integrity_error:
        flash(
            f"An error occurred. Location wasn't saved due to a database integrity error: "
            f"{str(integrity_error)}",
            "error"
        )
    except sqlite3.DatabaseError as db_error:
        flash(f"A database error occured. Location wasn't saved. {str(db_error)}", "error")
    else:
        flash(f"{new_name} has been updated.", "info")
