"""
This module is the main module for the app.
It performs all the core features when the app is running.
"""
import os
import subprocess
from flask import Flask, flash
from dotenv import load_dotenv
from routes.beverage import beverage_bp
from routes.locations import locations_bp

app = Flask(__name__)
app.register_blueprint(beverage_bp, url_prefix='/beverage')
app.register_blueprint(locations_bp, url_prefix='/locations')

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

if __name__ == '__main__':
    app.run()
