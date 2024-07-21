"""
All functions related to locations.
"""
import sqlite3
from flask import flash
from utils.db import get_db_connection

def get_all_locations():
    """
    Fetching and returning all locations.

    :return: A list of the locations.
    :rtype: list 
    """
    conn = get_db_connection()
    all_locations = conn.execute(
        "SELECT locationId, locationName "
        "FROM locations "
        "ORDER BY locationName ASC"
    ).fetchall()
    conn.close()
    return all_locations

def get_location(location_id):
    """
    Fetching and returning one location.

    :param location_id: The location's database ID.
    :type location_id: int
    :return: The location's name.
    :rtype: tuple
    """
    conn = get_db_connection()
    location = conn.execute(
        "SELECT locationName "
        "FROM locations "
        "WHERE locationId = ?",
        (location_id,)
    ).fetchone()
    conn.close()
    return location

def create_location(name):
    """
    Creates a new location in the database.

    :param name: The location's name.
    :type name: str
    :return: A flash message with the outcome.
    :rtype: str
    """
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO locations (locationName) "
            "VALUES (?)",
            (name,)
        )
        conn.commit()
        conn.close()
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
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE locations "
            "SET locationName = ? "
            "WHERE locationId = ?",
            (new_name, location_id)
        )
        conn.commit()
        conn.close()
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
