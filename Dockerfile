# use python:3.12-slim as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

CMD ["python", "google-routes.py"]
