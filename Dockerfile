# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by Flask and requests
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5001 to the outside world
EXPOSE 5001

# Define environment variable
ENV FLASK_APP=app.py

# Run the Flask app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app", "--workers=3"]
