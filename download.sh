#!/bin/bash

# Check if a playlist ID is provided
if [ -z "$1" ]; then
  echo "Usage: ./download.sh <YouTube Playlist ID>"
  exit 1
fi

# Set the playlist ID from the first argument
PLAYLIST_ID=$1

# Run the Docker container in detached mode with the specified playlist ID
docker run --rm -d \
  -v "$(pwd)/Download:/app/Download" \
  yt-downloader "$PLAYLIST_ID"
