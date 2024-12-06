# Stage 1: Base image for installing dependencies
FROM python:3.9-slim as base

# Install build dependencies for whisper and PyTorch
RUN apt-get update && apt-get install -y \
    git ffmpeg libsndfile1 build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Whisper and its dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
