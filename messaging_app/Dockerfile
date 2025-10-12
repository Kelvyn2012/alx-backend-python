# Use official Python 3.10 image
FROM python:3.10

# Set working directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Copy requirements first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Expose Django default port
EXPOSE 8000

# Run migrations and start Django server (includes port)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
