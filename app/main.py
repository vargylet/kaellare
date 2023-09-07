import os, sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# sqlite connection
def get_db_connection():
	conn = sqlite3.connect("database.db")
	conn.row_factory = sqlite3.Row
	return conn

# Fetch all locations
def get_locations():
	conn = get_db_connection()
	locations = conn.execute("SELECT locationId, locationName FROM locations ORDER BY locationName ASC").fetchall()
	conn.close()
	return locations

# Fetch one location
def get_location(id):
	conn = get_db_connection()
	location = conn.execute("SELECT locationName FROM locations WHERE locationId = ?",
			 				(id,)).fetchone()
	conn.close()
	return location

# Create location
def create_location(name):
	conn = get_db_connection()
	try:
		conn.execute("INSERT INTO locations (locationName) VALUES (?)",
	       			(name,))
		conn.commit()
		conn.close()
	except:
		flash("An error occurred. Location wasn't saved.", "error")
	else:
		flash(f"{name} has been added.", "info")

# Update location
def update_location(id, newName):
	conn = get_db_connection()
	try:
		conn.execute("UPDATE locations SET locationName = ? WHERE locationId = ?",
	      		(newName, id))
		conn.commit()
		conn.close()
	except:
		flash("An error occurred. Location wasn't updated.", "error")
	else:
		flash(f"{newName} has been updated.", "info")

# Fetch beverage data
def get_beverage(id):
	conn = get_db_connection()
	beverage = conn.execute("SELECT beverageId, beverageName, beverageYear, beveragePurchaseDate, beverageDrinkBefore, beverageNotes, locationId, locationName FROM beverages FULL JOIN locations ON beverageLocationId=locationId WHERE beverageId = ?",
			 (id,)).fetchone()
	conn.close()
	if beverage is None:
		abort(404)
	return beverage

def get_beverages(rows=("beverageId","beverageName"), join="LEFT JOIN", where=("")):
	conn = get_db_connection()

	# Formatting sqlRows
	for row in rows:
		try:
			sqlRows
		except:
			sqlRows = row
		else:
			sqlRows = sqlRows + ", " + row

	# Formatting sqlWhere
	if where != "":
		sqlWhere = " WHERE " + where
	else:
		sqlWhere = ""

	sqlQuery = f"SELECT {sqlRows} FROM beverages {join} locations ON beverageLocationId=locationId{sqlWhere} ORDER BY beverageName ASC"

	try:
		beverages = conn.execute(sqlQuery).fetchall()
		conn.close()
	except:
		flash("An error occurred when fetching the beverages.", "error")
		return False
	else:
		return beverages

@app.route("/")
@app.route("/dashboard")
def dashboard():
	beverages = get_beverages(("beverageId", "beverageName", "beverageYear", "locationId", "locationName"))

	return render_template("dashboard.html", beverages=beverages)

@app.route("/add_beverage", methods=("GET", "POST"))
def add_beverage():

	# Save to database
	if request.method == "POST":
		location = request.form["location"]
		name = request.form["name"]
		year = request.form["year"]
		purchaseDate = request.form["purchaseDate"]
		drinkBefore = request.form["drinkBefore"]
		notes = request.form["notes"]

		if not location:
			flash("Location is required.", "error")
		elif not name:
			flash("Name is required", "error")
		else:
			conn = get_db_connection()
			conn.execute("INSERT INTO beverages (beverageName, beverageLocationId, beverageYear, beveragePurchaseDate, beverageDrinkBefore, beverageNotes) VALUES (?, ?, ?, ?, ?, ?)",
						(name, location, year, purchaseDate, drinkBefore, notes)
			)
			conn.commit()
			conn.close()

			flash(f"{name} has been saved.", "info")
			return redirect(url_for("dashboard"))

	locations = get_locations()
	
	return render_template("beverage_add.html", locations=locations)

@app.route("/view/<int:id>")
def view_beverage(id):
	beverage = get_beverage(id)

	return render_template("beverage_view.html", beverage=beverage)

@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit_beverage(id):

	if request.method == "POST":
		location = request.form["location"]
		name = request.form["name"]
		year = request.form["year"]
		purchaseDate = request.form["purchaseDate"]
		drinkBefore = request.form["drinkBefore"]
		notes = request.form["notes"]

		if not location:
			flash("Location is required.", "error")
		elif not name:
			flash("Name if required", "error")
		else:
			conn = get_db_connection()
			conn.execute("UPDATE beverages SET beverageLocationId = ?, beverageName = ?, beverageYear = ?, beveragePurchaseDate = ?, beverageDrinkBefore = ?, beverageNotes = ? WHERE beverageId = ?",
						(location, name, year, purchaseDate, drinkBefore, notes, id))
			conn.commit()
			conn.close()

			flash(f"{name} has been updated.", "info")
			return redirect(url_for("dashboard"))
		
	beverage = get_beverage(id)
	locations = get_locations()

	return render_template("beverage_edit.html", beverage=beverage, locations=locations)

@app.route("/finished/<int:id>")
def finish_beverage(id):
	conn = get_db_connection()
	beverage = get_beverage(id)
	conn.execute("UPDATE beverages SET beverageLocationId = 0 WHERE beverageId = ?",
	      		(id,))
	conn.commit()
	conn.close()

	flash(f"{beverage['beverageName']} has been marked as finished.", "info")
	return redirect(url_for("dashboard"))

@app.route("/delete/<int:id>")
def delete_beverage(id):
	beverage = get_beverage(id)
	conn = get_db_connection()
	conn.execute("DELETE FROM beverages WHERE beverageId = ?",
	      		(id,))
	conn.commit()
	conn.close()

	flash(f"{beverage['beverageName']} has been deleted.", "info")
	return redirect(url_for("dashboard"))

@app.route("/locations", methods=("POST", "GET"))
def locations():
	locations = get_locations()
	return render_template("locations_view.html", locations=locations)

@app.route("/add_location", methods=("POST", "GET"))
def add_location():
	name = request.form["name"]
	if not name:
		flash("Name is required.", "error")
	else:
		create_location(name)
	
	return redirect(url_for("locations"))

@app.route("/edit_location/<int:id>", methods=("POST", "GET"))
def edit_location(id):
	name = request.form["name"]
	update_location(id, name)

	return redirect(url_for("locations"))

@app.route("/delete_location/<int:id>", methods=("POST", "GET"))
def delete_location(id):
	beverages = get_beverages(("beverageId",), "LEFT JOIN", f"beverageLocationId = {id}")
	if len(beverages) != 0:
		flash("You can't delete a location that still holds beverages.", "error")
		return redirect(url_for("locations"))

	try:
		conn = get_db_connection()
		conn.execute("DELETE FROM locations WHERE locationId = ?",
	       			(id,))
		conn.commit()
		conn.close()
	except:
		flash("An error occurred. The location wasn't deleted.", "error")
	else:
		flash("The location has been deleted.", "info")
	finally:
		return redirect(url_for("locations"))
	
if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0")