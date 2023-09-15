# syntax=docker/dockerfile:1

FROM python:3.11.5-alpine

# Set environment variables
# Time zone
ENV TZ=Etc/UTC

# Install timezone data
RUN apk update && \
    apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

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
ENTRYPOINT ["gunicorn", "-w1", "-b0.0.0.0:3000", "app:app"]