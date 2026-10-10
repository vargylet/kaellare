"""
Main module for the app.
"""
import os
import secrets
from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from init_db import init_db, DATABASE_DIR
from routes.beverages import beverages_bp
from routes.beverage import beverage_bp
from routes.locations import locations_bp

# Stored next to the database so it survives container restarts
SECRET_KEY_FILE_PATH = os.path.join(DATABASE_DIR, "secret_key")


def get_secret_key():
    """
    Returns the secret key from the SECRET_KEY environment variable (or .env).
    If it isn't set, the key is read from data/secret_key, or generated
    and stored there on first start.

    :return: The secret key.
    :rtype: str
    """
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        return secret_key

    try:
        with open(SECRET_KEY_FILE_PATH, "r", encoding="utf-8") as key_file:
            secret_key = key_file.read().strip()
    except FileNotFoundError:
        secret_key = ""

    if not secret_key:
        secret_key = secrets.token_hex(24)
        try:
            # Only readable by the owner
            fd = os.open(SECRET_KEY_FILE_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as key_file:
                key_file.write(secret_key)
        except OSError as os_error:
            print(f"Couldn't store the secret key, sessions won't survive a restart: {os_error}")

    return secret_key


# Creating and configurating the database (also creates the data directory)
init_db()

app = Flask(__name__)
app.config["SECRET_KEY"] = get_secret_key()
app.register_blueprint(beverages_bp, url_prefix='/beverages')
app.register_blueprint(beverage_bp, url_prefix='/beverage')
app.register_blueprint(locations_bp, url_prefix='/locations')

@app.route('/')
def index():
    return redirect(url_for('beverages_bp.index'))

if __name__ == '__main__':
    app.run()
