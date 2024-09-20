# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for SQLite
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a directory for the SQLite database
RUN mkdir -p /app/db

# Set environment variables to tell Django to use this directory
ENV DATABASE_URL=sqlite:///app/db/db.sqlite3

# Set permissions for the db directory
RUN chmod 777 /app/db

# Run migrations to set up the SQLite database
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the app
EXPOSE 8000

# Run the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "BankApp.wsgi:application"]
