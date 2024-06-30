"""
This module is the main module for the app.
It performs all the core features when the app is running.
"""
import os
import sqlite3
import subprocess
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from dotenv import load_dotenv

app = Flask(__name__)

def get_db_connection():
    """
    Connecting to the SQLite database.

    :return: The database connection.
    :rtype: object
    """
    conn = sqlite3.connect("./data/database.db")
    conn.row_factory = sqlite3.Row
    return conn

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

@app.route("/")
@app.route("/dashboard")
def dashboard():
    """
    Fetches beverages from the database and shows the user the list of beverages in the database.

    :return: An HTML page with some of the beverages' information.
    :rtype: str
    """

    filter_value = request.args.get('filter')

    # All beverages in the database
    if filter_value == 'all':
        beverages = get_beverages(
            ("beverageId", "beverageName", "beverageYear", "locationId", "locationName")
        )
    # Beverages currently not in storage
    elif filter_value == 'not_stored':
        beverages = get_beverages(
            ("beverageId", "beverageName", "beverageYear", "locationId", "locationName"), 
            "LEFT JOIN", 
            "beverageLocationId = 0"
        )
    # Beverages in storage
    else:
        beverages = get_beverages(
            ("beverageId", "beverageName", "beverageYear", "locationId", "locationName"), 
            "LEFT JOIN", 
            "beverageLocationId != 0"
        )

    return render_template("dashboard.html", beverages=beverages)

@app.route("/add_beverage", methods=("GET", "POST"))
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
            return redirect(url_for("dashboard"))

    locations_all = get_all_locations()

    return render_template("beverage_add.html", locations=locations_all)

@app.route("/view/<int:beverage_id>")
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

@app.route("/edit/<int:beverage_id>", methods=["GET", "POST"])
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
            return redirect(url_for("dashboard"))

    beverage = get_beverage(beverage_id)
    locations_all = get_all_locations()

    return render_template("beverage_edit.html", beverage=beverage, locations=locations_all)

@app.route("/finished/<int:beverage_id>")
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
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:beverage_id>")
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
    return redirect(url_for("dashboard"))

@app.route("/locations")
def locations():
    """
    Shows the HTML page listing all locations from the database.

    :return: An HTML page listing all current locations and a form to add more.
    :rtype: str
    """
    locations_all = get_all_locations()
    return render_template("locations_view.html", locations=locations_all)

@app.route("/add_location", methods=["POST"])
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

    return redirect(url_for("locations"))

@app.route("/edit_location/<int:location_id>", methods=["POST"])
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

    return redirect(url_for("locations"))

@app.route("/delete_location/<int:location_id>")
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
        return redirect(url_for("locations"))

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

    return redirect(url_for("locations"))

with app.app_context():
    # Generate secret key
    secret_key = os.urandom(24).hex()
    ENV_FILE_PATH = ".env"

    # Write secret key to dotenv
    try:
        # open file to write
        with open(ENV_FILE_PATH, "w", encoding="utf-8") as env_file:
            env_file.write(f"SECRET_KEY={secret_key}\n")
    except PermissionError as permission_error:
        flash(f"A permission error occured while opening the .env file: {str(permission_error)}")
    except IOError as io_error:
        flash(f"An IO error occured while opening the .env file: {str(io_error)}")

    # Load dotenv and secret key
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Creating and configurating the database
    try:
        subprocess.run(["python3", "init_db.py"], check=True)
    except subprocess.CalledProcessError as error:
        print(f"Error running init_db.py: {str(error)}")

if __name__ == "__main__":
    app.run()
