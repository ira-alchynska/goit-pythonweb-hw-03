# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install the required Python packages (here, Flask)
# If you have a requirements.txt file, use:
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask

# Expose the port that the app runs on
EXPOSE 3000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD ["flask", "run", "--port=3000"]
