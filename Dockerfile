# Use a slim Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install system dependencies required for OpenCV, numpy, scipy, and others
RUN apt-get update && apt-get install -y \
    gcc g++ make build-essential \
    libffi-dev libssl-dev \
    libjpeg-dev libpng-dev libtiff-dev \
    libopencv-dev && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip to avoid old package issues
RUN pip install --upgrade pip

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask's port
EXPOSE 3000

# Run the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]
