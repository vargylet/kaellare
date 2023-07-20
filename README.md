# kaellare

## Features
kaellare is designed to keep track of the beverages you store at home. The main purpose is to manage your wines but the application is not limited to that, beer, liqour, and other types are also possible.

## Expectations
I'm a happy hobby programmer and this is my first atempt to properly build something. I'm using kaellare as a project for me to learn new techniques. With that said, there are probably better ways to solve things than I've come up with. Feel free to share your experiences by creating an issue or a pull request.

This project is probably going to evolve quite slowly due to life... :-]

## Requirements
- Python >= 3.6
- flask >= 2.3.2
- dotenv >= 1.0.0

## Installation

```
# Create <YOUR_SECRET_KEY>
python3
>>> import os
>>> os.urandom(24).hex()
# Copy the output

# Create .env file in directory app
nano app/.env

# Add the following in the .env file and save
SECRET_KEY=<YOUR_SECRET_KEY>

# Create sqlite3 database
python init_db.py
```

Now, go to http://localhost:5000 in your browser.