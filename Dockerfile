# Dockerfile
# Use the official Python image as the base image
FROM python:3.12.0b3-bookworm

ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /django

# Copy the requirements.txt file to the container
COPY requirements.txt requirements.txt

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the Django project files to the container
COPY . .

CMD gunicorn jobfinderapi.wsgi:application --bind 0.0.0:8000

EXPOSE 8000