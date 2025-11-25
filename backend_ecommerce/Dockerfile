# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend project
COPY . .

# Ensure Python output is shown in logs
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput

# Start Gunicorn server
CMD ["gunicorn", "ecommerce_project.wsgi:application", "--bind", "0.0.0.0:8000"]
