# syntax=docker/dockerfile:1

FROM python:3.11.5-alpine

# Copy files to container
COPY ./requirements.txt /app/requirements.txt
COPY ./app /app

# Change workdir
WORKDIR /app

# Port to use
EXPOSE 3000

# Install dependencies
RUN pip install -r requirements.txt

# Start app with gunicorn
ENTRYPOINT ["gunicorn", "-w1", "-b0.0.0.0:3000", "main:app"]