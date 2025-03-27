#Builds the web and cron containers with Python, Gunicorn, and cron setup.
FROM python:3.11-slim 
#as the base image (small and efficient).

WORKDIR /app
#Sets the working directory to /app inside the container.

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
#Sets environment variables to keep Python output unbuffered and skip bytecode files.

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    bpfcc-tools \
    python3-bpfcc \
    && rm -rf /var/lib/apt/lists/*

# RUN apt-get ...: Installs `cron` (for scheduling), `bpfcc-tools`, and `python3-bpfcc` (for monitoring), then cleans up.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# COPY requirements.txt ...: Copies the dependency list and installs them with `pip`

COPY . .
# COPY . .: Copies all project files into the container.

COPY crontab /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job && crontab /etc/cron.d/my-cron-job
# COPY crontab ...: Adds a cron job file, sets permissions, and activates it.

EXPOSE 8000
# EXPOSE 8000: Opens port 8000 for the app.

CMD cron && gunicorn todo_list.wsgi:application --bind 0.0.0.0:8000
# CMD ["gunicorn", "todo_list.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD: Runs Gunicorn to serve the Django app on port 8000.


# Gunicorn: A Python WSGI server that runs web applications like Django.
# What it does: Takes web requests (e.g., from users visiting your site) and passes them to your app.
# Why use it: Faster and more reliable than Django’s built-in server, good for production.
# How it works: Listens on a port (e.g., 8000) and manages multiple workers to handle requests.

# FROM python:3.11-slim

# WORKDIR /app

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     cron \
#     bpfcc-tools \
#     python3-bpfcc \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# COPY crontab /etc/cron.d/my-cron-job
# RUN chmod 0644 /etc/cron.d/my-cron-job && crontab /etc/cron.d/my-cron-job

# EXPOSE 8000

# CMD cron && python manage.py runserver 0.0.0.0:8000


# Use an official Python runtime as the base image
# FROM python:3.11-slim

# # Set working directory in the container
# WORKDIR /app

# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1

# # Install system dependencies (for cron)
# RUN apt-get update && apt-get install -y \
#     cron \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements file and install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the entire project to the container
# COPY . .

# # Install the crontab file
# COPY crontab /etc/cron.d/my-cron-job
# RUN chmod 0644 /etc/cron.d/my-cron-job && crontab /etc/cron.d/my-cron-job

# # Expose the port Django will run on
# EXPOSE 8000

# # Command to run both cron and the Django app
# CMD cron && python manage.py runserver 0.0.0.0:8000