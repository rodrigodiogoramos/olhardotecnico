# Use a base image that's known to work well with wkhtmltopdf.
FROM debian:bullseye-slim

# Install system dependencies.
# The `xvfb` and `xfonts` packages are crucial for headless rendering.
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    wkhtmltopdf \
    xvfb \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-cyrillic

# Set working directory inside the container.
WORKDIR /app

# Copy the requirements file and install Python dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code.
COPY . .

# Expose the port that the application will listen on.
EXPOSE 8080

# The Gunicorn server starts your application.
# `xvfb-run` is the key part that runs the process in a virtual display,
# which is required for wkhtmltopdf to work properly.
CMD ["xvfb-run", "-a", "gunicorn", "--bind", "0.0.0.0:8080", "main:app"]