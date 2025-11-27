#!/bin/bash

# Usage message
usage() {
  echo "Usage: ./download.sh <YouTube Playlist ID> [--reverse] [--season-name \"Name or Number\"] [--docker]"
  exit 1
}

# Check for minimum arguments
if [ -z "$1" ]; then
  usage
fi

# Parse arguments
PLAYLIST_ID=""
REVERSE_FLAG=""
SEASON_NAME=""
DOCKER_FLAG=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --reverse)
      REVERSE_FLAG="--reverse"
      shift
      ;;
    --docker)
      DOCKER_FLAG=1
      shift
      ;;
    --season-name)
      if [[ -z "$2" ]]; then
        echo "--season-name requires a value."
        usage
      fi
      SEASON_NAME="$2"
      shift 2
      ;;
    *)
      if [[ -z "$PLAYLIST_ID" ]]; then
        PLAYLIST_ID="$1"
        shift
      else
        usage
      fi
      ;;
  esac
done

if [ -z "$PLAYLIST_ID" ]; then
  usage
fi

EXTRA_ARGS=()
if [[ -n "$REVERSE_FLAG" ]]; then
  EXTRA_ARGS+=("$REVERSE_FLAG")
fi
if [[ -n "$SEASON_NAME" ]]; then
  EXTRA_ARGS+=("--season-name" "$SEASON_NAME")
fi

if [ $DOCKER_FLAG -eq 1 ]; then
  # Run in Docker (detached mode)
  docker run --rm -d \
    -v "$(pwd)/Download:/app/Download" \
    yt-downloader "$PLAYLIST_ID" "${EXTRA_ARGS[@]}"
else
  # Run locally
  python3 download-playlist.py "$PLAYLIST_ID" "${EXTRA_ARGS[@]}"
fi
