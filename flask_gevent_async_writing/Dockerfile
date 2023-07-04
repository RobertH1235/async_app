# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code to the container
COPY . .

# Create the uploads folder in the container
RUN mkdir -p /app/uploads

# Expose port 5000 for the Flask application
EXPOSE 5000

# Start Gunicorn with gevent worker
CMD ["gunicorn", "--worker-class", "gevent", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]
