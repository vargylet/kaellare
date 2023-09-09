# kaellare

## Features
kaellare is designed to keep track of the beverages you store at home. The main purpose is to manage your wines but the application is not limited to that. Beer, liqour, and other types of beverages are also possible to store.

## Expectations
I'm a happy hobby programmer and this is my first atempt to properly build something. I'm using kaellare as a project for me to learn new techniques. With that said, there are probably better ways to solve things than I've come up with. Feel free to share your experiences by creating an issue or a pull request.

This project is probably going to evolve quite slowly due to life... :-]

## Install using Docker
```
docker run -d --name=kaellare -p 3000:3000 -v /path/to/data:/app/data ghcr.io/vargylet/kaellare:latest
```

You can also use docker compose:
```
version: "2"

services:
  app:
    image: ghcr.io/vargylet/kaellare:latest
    container_name: kaellare
    ports:
      - 3000:3000
    volumes:
      - /path/to/data:/app/data
```
## Development environment
Requirements:
- Python >= 3.11
- and everything in [requirements](requirements.txt).

```
# Clone the repo
git clone

# Launch the Flask app
flask --debug --app main run
```

Now, go to http://127.0.0.1:5000 in your browser.
