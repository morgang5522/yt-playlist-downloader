#!/bin/bash

# Check if a playlist ID was provided
if [ -z "$1" ]; then
    echo "Error: No playlist ID provided."
    echo "Usage: docker run yt-downloader PLAYLIST_ID"
    exit 1
fi

# Check if the --reverse flag is provided
REVERSE_FLAG=""
if [ "$2" == "--reverse" ]; then
    REVERSE_FLAG="--reverse"
fi

# Run the Python script with the playlist ID and optional reverse flag
python download-playlist.py "$1" $REVERSE_FLAG

# Exit the container automatically after completion
exit 0
