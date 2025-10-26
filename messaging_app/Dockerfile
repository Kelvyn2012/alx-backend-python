# Use the official Python 3.10 image from Docker Hub as a base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container (adjust the path if necessary)
COPY messaging_app/requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into the container
COPY messaging_app /app/

# Expose the port that Django runs on (default is 8000)
EXPOSE 8000

# Run Django app on the specified port (default is 8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
