# Use a full Python image to ensure apt-get is available
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for WeasyPrint
# This command is more robust for a standard Debian-based image
RUN apt-get update && \
    apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-xlib-2.0-0 libffi-dev

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for Gunicorn
EXPOSE 8080

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]