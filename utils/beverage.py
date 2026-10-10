"""
All functions related to beverages.
"""
import sqlite3
from flask import flash, abort
from utils.db import get_db_connection


def get_beverage(beverage_id):
    """
    Fetches data from the database about a beverage based on the provided database ID.

    :param id: The beverage's database ID.
    :type id: id
    :return: Returns the beverage's data that's relevant for the user.
    :rtype: tuple
    """
    conn = get_db_connection()
    beverage = conn.execute(
        "SELECT beverageId, beverageName, beverageYear, beveragePurchaseDate, beverageDrinkBefore, "
        "beverageNotes, locationId, locationName "
        "FROM beverages "
        "FULL JOIN locations ON beverageLocationId=locationId "
        "WHERE beverageId = ?",
        (beverage_id,)
    ).fetchone()
    conn.close()
    if beverage is None:
        abort(404)
    return beverage

def get_beverages(finished=None):
    """
    Fetches the beverages to list on the dashboard, sorted by name.

    :param finished: True for finished beverages, False for stored beverages
                     and None (default) for all beverages.
    :type finished: bool or None
    :return: The beverages' id, name, year, location id and location name.
             An empty list if the database couldn't be read.
    :rtype: list
    """
    # Only fixed SQL fragments are used, never input from the caller
    if finished is None:
        sql_where = ""
    elif finished:
        sql_where = "WHERE beverageLocationId = 0 "
    else:
        sql_where = "WHERE beverageLocationId != 0 "

    sql_query = (
        "SELECT beverageId, beverageName, beverageYear, locationId, locationName "
        "FROM beverages "
        "LEFT JOIN locations ON beverageLocationId=locationId "
        f"{sql_where}"
        "ORDER BY beverageName ASC"
    )

    try:
        conn = get_db_connection()
        try:
            return conn.execute(sql_query).fetchall()
        finally:
            conn.close()
    except sqlite3.Error as db_error:
        flash(f"A database error occurred. Beverages couldn't be loaded. {str(db_error)}", "error")
        return []