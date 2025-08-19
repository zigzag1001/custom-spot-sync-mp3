# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install spotdl
# RUN pip install spotdl==4.2.11 # this version works better for now
RUN pip install spotdl==4.4.1

# Install ffmpeg, wget for rsgain
RUN apt-get update && apt-get install -y ffmpeg rsgain

ENV HOME="/config"
RUN mkdir -p /config/.spotdl/temp
RUN chown -R 1000:1000 /config/.spotdl

# Define the default command (can be overridden by Compose)
# CMD ["python", "main.py"]  # Replace main.py with your entry point script

