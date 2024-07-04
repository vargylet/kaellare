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

def get_beverages(rows=("beverageId","beverageName"), join="LEFT JOIN", where=""):
    """
    Fetches data from the database about beverages based on the provided query.

    :param rows: The rows to fetch from the database.
                 Defaults to "beverageId","beverageName" if not provided.
    :type rows: string
    :param join: How you want to use join in your query.
                 Defaults to "LEFT JOIN" if not provided.
    :type join: string
    :param where: You can add a WHERE clause. It should not include "WHERE".
                  Defaults to none if not provided.
    :type where: string
    :return: The data requested about the beverage.
    :rtype: tuple
    """
    conn = get_db_connection()

    # The formatting of sql_rows
    sql_rows = ""
    for row in rows:
        sql_rows += row + ", "

    # Remove the trailing comma and space from the end of sql_rows
    sql_rows = sql_rows.rstrip(", ")

    # Formatting sql_where
    if where != "":
        sql_where = " WHERE " + where
    else:
        sql_where = ""

    sql_query = (
        f"SELECT {sql_rows} "
        f"FROM beverages {join} locations ON beverageLocationId=locationId"
        f"{sql_where} "
        "ORDER BY beverageName ASC"
    )

    try:
        beverages = conn.execute(sql_query).fetchall()
        conn.close()
    except sqlite3.IntegrityError as integrity_error:
        flash(
            f"An error occurred. Location wasn't saved due to a database integrity error: "
            f"{str(integrity_error)}",
            "error"
        )
    except sqlite3.DatabaseError as db_error:
        flash(f"A database error occured. Location wasn't saved. {str(db_error)}", "error")
    return beverages