# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install yt-dlp via pip3 (latest version)
RUN pip3 install --no-cache-dir yt-dlp pandas requests

# Copy script and entrypoint
COPY download-playlist.py .
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set the default command
ENTRYPOINT ["./entrypoint.sh"]
