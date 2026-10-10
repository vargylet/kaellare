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


def init_db():
    """
    Creates the data directory and the database if they don't already exist.
    """
    # Create data directory if it doesn't exist
    os.makedirs(DATABASE_DIR, exist_ok=True)

    if os.path.isfile(DATABASE_FILE_PATH):
        # Database file already exists
        print("A database already exists. No changes were made.")
        return

    try:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        try:
            # Read sql file and execute its content
            with open(SQL_FILE_PATH, "r", encoding="utf-8") as sql_file:
                connection.executescript(sql_file.read())

            # Save to database
            connection.commit()
        finally:
            connection.close()

        print("Database has been created and SQL commands have been executed.")

    except sqlite3.Error as e:
        print("An error occurred", e)


if __name__ == '__main__':
    init_db()
