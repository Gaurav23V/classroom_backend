# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application into the container
COPY . .

# Expose port 5000 for the Flask app to run on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=core/server.py
ENV FLASK_ENV=production

# Define the command to run your application
CMD ["flask", "run", "--host=0.0.0.0"]