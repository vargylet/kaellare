"""
This module is run on startup of the app and
creates the SQLite database in data/ if it doesn't already exist.
"""
import sqlite3
import os

# Database directory and filename
DATABASE_DIR = './data'
DATABASE_FILE_PATH = os.path.join(DATABASE_DIR, 'database.db')
# Initial database structure
SQL_FILE_PATH = "schema.sql"

# Create data directory if it doesn't exist
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

if not os.path.isfile(DATABASE_FILE_PATH):
    # Database file doesn't exist
    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        cursor = connection.cursor()

        # Read sql file and execute its content
        with open(SQL_FILE_PATH, "r", encoding="utf-8") as sql_file:
            sql_command = sql_file.read()
            cursor.executescript(sql_command)

        # Save to database
        connection.commit()

        print("Database has been created and SQL commands have been executed.")

        # Close connection
        connection.close()

    except sqlite3.Error as e:
        print("An error occurred", e)
else:
    # Database file already exists
    print("A database already exists. No changes were made.")
