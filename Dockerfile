# Use your base image (e.g., Python image)
FROM python:3.12-slim

# Install required system dependencies, including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the command to run your script
CMD ["python", "generate_audio.py"]
