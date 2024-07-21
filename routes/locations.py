import sqlite3
from flask import Blueprint, render_template, redirect, flash, url_for, request
from utils.db import get_db_connection
from utils.locations import get_all_locations, create_location, update_location
from utils.beverage import get_beverages

locations_bp = Blueprint('locations_bp', __name__)


@locations_bp.route("/")
def index():
    """
    Shows the HTML page listing all locations from the database.

    :return: An HTML page listing all current locations and a form to add more.
    :rtype: str
    """
    locations_all = get_all_locations()
    return render_template("locations_view.html", locations=locations_all)


@locations_bp.route("/add_location", methods=["POST"])
def add_location():
    """
    This function stores the name of a new location from the form.

    :return: An HTML page with all current locations.
    :rtype: str
    """
    name = request.form["name"]
    if not name:
        flash("Name is required.", "error")
    else:
        create_location(name)

    return redirect(url_for("locations_bp.index"))


@locations_bp.route("/edit_location/<int:location_id>", methods=["POST"])
def edit_location(location_id):
    """
    Updates the location name and redirects the user back to the list of locations.

    :param location_id: The location's database ID.
    :type location_id: int
    :return: An HTML page with all current locations.
    :rtype: str
    """
    name = request.form["name"]
    update_location(location_id, name)

    return redirect(url_for("locations_bp.index"))


@locations_bp.route("/delete_location/<int:location_id>")
def delete_location(location_id):
    """
    Deletes a location and all its data from the database.

    :param location_id: The location's database ID.
    :type location_id: int
    :return: An HTML page with all current locations.
    :rtype: 
    """
    beverages = get_beverages(("beverageId",), "LEFT JOIN", f"beverageLocationId = {location_id}")
    if len(beverages) != 0:
        flash("You can't delete a location that still holds beverages.", "error")
        return redirect(url_for("locations_bp.index"))

    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM locations "
                     "WHERE locationId = ?",
                     (location_id,)
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
        flash("The location has been deleted.", "info")

    return redirect(url_for("locations_bp.index"))
