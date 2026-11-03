# syntax=docker/dockerfile:1

FROM python:3.15.2-alpine3.24

# Set environment variables
# Time zone
ENV TZ=Etc/UTC
# Show Python output in the container logs right away and skip .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Apply the latest OS security updates and install timezone data
RUN apk upgrade --no-cache && \
    apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Change workdir
WORKDIR /app

# Install dependencies first, so this layer is cached until requirements.txt changes
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy files to container
COPY ./app.py /app/app.py
COPY ./main.wsgi /app/main.wsgi
COPY ./init_db.py /app/init_db.py
COPY ./schema.sql /app/schema.sql
COPY ./routes /app/routes
COPY ./static /app/static
COPY ./templates /app/templates
COPY ./utils /app/utils

# Port to use
EXPOSE 3000

# Start app with gunicorn
ENTRYPOINT ["gunicorn", "-w1", "-b0.0.0.0:3000", "--no-control-socket", "app:app"]
