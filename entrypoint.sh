#!/bin/bash

# Check if a playlist ID was provided
if [ -z "$1" ]; then
    echo "Error: No playlist ID provided."
    echo "Usage: docker run yt-downloader PLAYLIST_ID [--reverse] [--season-name ...]"
    exit 1
fi

# Pass through any additional flags (e.g., --reverse, --season-name)
PLAYLIST_ID="$1"
shift
python download-playlist.py "$PLAYLIST_ID" "$@"

# Exit the container automatically after completion
exit 0
