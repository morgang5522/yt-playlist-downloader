#!/bin/bash

# Check if a playlist ID is provided
if [ -z "$1" ]; then
  echo "Usage: ./download.sh <YouTube Playlist ID>"
  exit 1
fi

# Set the playlist ID from the first argument
PLAYLIST_ID=$1

# Check if the --reverse flag is provided
REVERSE_FLAG=""
if [ "$2" == "--reverse" ]; then
  REVERSE_FLAG="--reverse"
fi

# Run the Docker container in detached mode with the specified playlist ID and optional reverse flag
docker run --rm -d \
  -v "$(pwd)/Download:/app/Download" \
  yt-downloader "$PLAYLIST_ID" $REVERSE_FLAG
