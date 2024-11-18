# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY *.py *.env requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install spotdl
RUN pip install spotdl

# Ensure the .env file is used
ENV PYTHONUNBUFFERED=1

# Define the default command (can be overridden by Compose)
CMD ["python", "main.py"]  # Replace main.py with your entry point script

