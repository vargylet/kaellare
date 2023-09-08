import sqlite3, os

# Database filename
database_file_path = "./data/database.db"
# Initial database structure
sql_file_path = "schema.sql"

if not os.path.isfile(database_file_path):
    # Database file doesn't exist
    try:
        connection = sqlite3.connect(database_file_path)
        cursor = connection.cursor()

        # Read sql file and execute its content
        with open(sql_file_path, "r") as sql_file:
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