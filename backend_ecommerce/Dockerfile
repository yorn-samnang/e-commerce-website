FROM python:3.12-slim

WORKDIR /app

# Install system libraries needed for Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Move into folder containing manage.py
WORKDIR /app/ecommerce_project

# Collect static files
RUN python manage.py collectstatic --noinput

# Back to root app folder
WORKDIR /app

# FIX: Correct Gunicorn WSGI path
CMD ["gunicorn", "ecommerce_project.ecommerce_project.wsgi:application", "--bind", "0.0.0.0:8000"]