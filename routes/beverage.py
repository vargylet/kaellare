"""
Route for showing pages related to single beverage.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils.db import get_db_connection
from utils.beverage import get_beverage, get_beverages
from utils.locations import get_all_locations

beverage_bp = Blueprint('beverage_bp', __name__)


@beverage_bp.route("/add_beverage", methods=("GET", "POST"))
def add_beverage():
    """
    This route can show the user the form to add a new beverage to the system
    or store the data from the form to the database.

    - GET: Shows the form to add a new beverage.
    - POST: Stores the new beverage in the database.

    :return: Flashes a message above the HTML form if a beverage has been stored
             or shows the form without a flash.
    :rtype: str
    """
    if request.method == "POST":
        location = request.form["location"]
        name = request.form["name"]
        year = request.form["year"]
        purchase_date = request.form["purchaseDate"]
        drink_before = request.form["drinkBefore"]
        notes = request.form["notes"]

        if not location:
            flash("Location is required.", "error")
        elif not name:
            flash("Name is required", "error")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO beverages (beverageName, beverageLocationId, beverageYear, "
                "beveragePurchaseDate, beverageDrinkBefore, beverageNotes) "
                "VALUES (?, ?, ?, ?, ?, ?)",
			    (name, location, year, purchase_date, drink_before, notes)
            )
            conn.commit()
            conn.close()

            flash(f"{name} has been saved.", "info")
            return redirect(url_for("beverages_bp.index"))

    locations_all = get_all_locations()

    return render_template("beverage_add.html", locations=locations_all)


@beverage_bp.route("/view/<int:beverage_id>")
def view_beverage(beverage_id):
    """
    Shows all information about a beverage based on the provided database ID.

    :param beverage_id: The beverage's database ID.
    :type beverage_id: int
    :return: An HTML page showing all information stored about the beverage.
    :rtype: str
    """
    beverage = get_beverage(beverage_id)

    return render_template("beverage_view.html", beverage=beverage)


@beverage_bp.route("/edit/<int:beverage_id>", methods=["GET", "POST"])
def edit_beverage(beverage_id):
    """
    Shows the page with a form to edit a beverage
    or updates the data in the database about a beverage.

    :param beverage_id: The beverage's database ID.
    :type beverage_id: int
    :return: Flashes a message above the HTML form if a beverage has been updated
             or shows the form without a flash.
    :rtype: str
    """
    if request.method == "POST":
        location = request.form["location"]
        name = request.form["name"]
        year = request.form["year"]
        purchase_date = request.form["purchaseDate"]
        drink_before = request.form["drinkBefore"]
        notes = request.form["notes"]

        if not location:
            flash("Location is required.", "error")
        elif not name:
            flash("Name if required", "error")
        else:
            conn = get_db_connection()
            conn.execute(
                "UPDATE beverages "
                "SET beverageLocationId = ?, beverageName = ?, beverageYear = ?, "
                "beveragePurchaseDate = ?, beverageDrinkBefore = ?, beverageNotes = ? "
                "WHERE beverageId = ?",
                (location, name, year, purchase_date, drink_before, notes, beverage_id)
            )
            conn.commit()
            conn.close()

            flash(f"{name} has been updated.", "info")
            return redirect(url_for("beverages_bp.index"))

    beverage = get_beverage(beverage_id)
    locations_all = get_all_locations()

    return render_template("beverage_edit.html", beverage=beverage, locations=locations_all)


@beverage_bp.route("/finished/<int:beverage_id>")
def finish_beverage(beverage_id):
    """
    Marks a beverage as finished and stores that information in the database.

    :param beverage_id: The beverage's database ID.
    :type beverage_id: int
    :return: Flashes a message above the HTML dashboard with all beverages.
    :rtype: str
    """
    conn = get_db_connection()
    beverage = get_beverage(beverage_id)
    conn.execute("UPDATE beverages "
                 "SET beverageLocationId = 0 "
                 "WHERE beverageId = ?",
                 (beverage_id,)
    )
    conn.commit()
    conn.close()

    flash(f"{beverage['beverageName']} has been marked as finished.", "info")
    return redirect(url_for("beverages_bp.index"))


@beverage_bp.route("/delete/<int:beverage_id>")
def delete_beverage(beverage_id):
    """
    Deletes a beverage from the database and all its data.

    :param beverage_id: The beverage's database ID.
    :type beverage_id: int
    :return: Flashes a message above the HTML dashboard with all beverages.
    :rtype: str
    """
    beverage = get_beverage(beverage_id)
    conn = get_db_connection()
    conn.execute("DELETE FROM beverages "
                 "WHERE beverageId = ?",
                 (beverage_id,)
    )
    conn.commit()
    conn.close()

    flash(f"{beverage['beverageName']} has been deleted.", "info")
    return redirect(url_for("beverages_bp.index"))
