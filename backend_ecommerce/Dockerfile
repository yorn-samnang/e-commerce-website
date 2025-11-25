FROM python:3.12-slim

WORKDIR /app

# Install dependencies needed by Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend folder (important!)
COPY . .

# Set workdir before running manage.py
WORKDIR /app/ecommerce_project

# Collect static files
RUN python manage.py collectstatic --noinput

# Go back to root app folder
WORKDIR /app

# Start gunicorn (point to correct wsgi)
CMD ["gunicorn", "ecommerce_project.wsgi:application", "--bind", "0.0.0.0:8000"]
