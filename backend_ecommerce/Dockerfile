FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required by Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput

# Start server
CMD ["gunicorn", "ecommerce_project.wsgi:application", "--bind", "0.0.0.0:8000"]