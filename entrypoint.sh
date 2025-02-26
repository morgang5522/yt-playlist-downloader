#!/bin/bash

# Check if a playlist ID was provided
if [ -z "$1" ]; then
    echo "Error: No playlist ID provided."
    echo "Usage: docker run yt-downloader PLAYLIST_ID"
    exit 1
fi

# Run the Python script with the playlist ID
python download-playlist.py "$1"

# Exit the container automatically after completion
exit 0
