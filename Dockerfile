# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages with specific order to resolve dependencies
RUN pip install --no-cache-dir \
    Django==5.0.2 \
    psycopg2-binary==2.9.10 \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8080

# Run the Django development server
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8080"]
