import sqlite3

connection = sqlite3.connect("database.db")
connection.row_factory = sqlite3.Row

with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO locations (locationName) VALUES (?)",
            ("Wine cellar",)
            )
cur.execute("INSERT INTO locations (locationName) VALUES (?)",
            ("Kitchen",)
            )

location = cur.execute("SELECT locationId FROM locations ORDER BY locationId ASC LIMIT 1").fetchone()
print(location["locationId"])

cur.execute("INSERT INTO beverages (beverageName, beverageLocationId, beverageYear, beveragePurchaseDate, beverageDrinkBefore, beverageNotes) VALUES (?, ?, ?, ?, ?, ?)",
            ("Serralunga d’Alba Fontanafredda", location['locationId'], 2014, "2019-10-22", "2029-01-01", "Barolo, gifted to me.")
            )

connection.commit()
connection.close()