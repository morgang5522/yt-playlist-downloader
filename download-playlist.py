import os
import sys
import time
import argparse
import requests
import subprocess
import pandas as pd
import logging

def sanitize_filename(name):
    """Removes invalid characters for filenames and replaces with spaces."""
    return "".join(c if c.isalnum() or c in " ._-" else " " for c in name).strip()

def infer_season_number_from_name(season_name):
    """
    Attempts to detect a numeric season identifier from a friendly season name.
    Examples:
        "2" -> 2
        "Season 3" -> 3
        "S04" -> 4
    """
    if not season_name:
        return None
    cleaned = season_name.strip()
    if not cleaned:
        return None
    if cleaned.isdigit():
        return int(cleaned)
    lowered = cleaned.lower()
    if lowered.startswith("season"):
        suffix = cleaned[len("season"):].strip()
        if suffix.isdigit():
            return int(suffix)
    if lowered.startswith("s"):
        suffix = cleaned[1:].strip()
        if suffix.isdigit():
            return int(suffix)
    return None

def create_nfo_file(file_path, title, url, description, date, season, episode):
    """Creates an Emby-compatible .nfo metadata file for TV series."""
    nfo_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<episodedetails>
    <title>{title}</title>
    <season>{season}</season>
    <episode>{episode}</episode>
    <plot>{description}</plot>
    <aired>{date}</aired>
    <uniqueid type="youtube">{url}</uniqueid>
</episodedetails>
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(nfo_content)

def download_thumbnail(url, output_path):
    """Downloads the YouTube video thumbnail."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            logging.info(f"Thumbnail saved: {output_path}")
        else:
            logging.error(f"Failed to download thumbnail: {url}")
    except Exception as e:
        logging.error(f"Error downloading thumbnail: {e}")

def download_video(video_url, output_directory, video_title, season_label, episode):
    """Downloads a video using yt-dlp and skips if it already exists."""
    safe_file_name = f"{season_label} - E{episode:02d} - {sanitize_filename(video_title)}.mp4"
    file_path = os.path.join(output_directory, safe_file_name)

    # Skip download if the file already exists
    if os.path.exists(file_path):
        logging.info(f"Skipping {video_title} (already downloaded)")
        return safe_file_name

    # yt-dlp command to download a more filesize-friendly format with 1080p limit
    command = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",  # Limit to 1080p for smaller size
        "--merge-output-format", "mp4",    # Merge into a single MP4 file
        "-o", file_path,                   # Save with formatted filename
        video_url
    ]

    logging.info(f"Downloading: {video_title} ({video_url})")

    # Try up to 3 times with increasing delay on failure
    for attempt in range(3):
        try:
            subprocess.run(command, check=True)
            return safe_file_name  # Success
        except subprocess.CalledProcessError as e:
            wait_time = (attempt + 1) * 30  # Exponential backoff (30s, 60s, 90s)
            logging.error(f"Error downloading {video_title}: {e}")
            logging.info(f"Retrying in {wait_time} seconds... (Attempt {attempt + 1}/3)")
            time.sleep(wait_time)

    logging.error(f"Failed to download after multiple attempts: {video_title}")
    return None  # Failure

def download_playlist(playlist_id, reverse_order=False, season_name="Season 01", season_number=1):
    """Downloads an entire YouTube playlist using yt-dlp with metadata for Emby."""
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    
    # Fetch playlist metadata
    logging.info("Fetching playlist details...")
    result = subprocess.run(["yt-dlp", "--flat-playlist", "-J", playlist_url], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error("Error fetching playlist info. Make sure the playlist ID is correct.")
        sys.exit(1)

    import json
    playlist_data = json.loads(result.stdout)
    playlist_title = sanitize_filename(playlist_data["title"])

    desired_season_name = season_name.strip() if season_name else "Season 01"
    sanitized_season_name = sanitize_filename(desired_season_name) or "Season 01"
    output_directory = os.path.join(os.getcwd(), "Download", playlist_title, sanitized_season_name)
    os.makedirs(output_directory, exist_ok=True)

    video_entries = playlist_data["entries"]
    if reverse_order:
        video_entries.reverse()

    video_data = []
    logging.info(f"Downloading {len(video_entries)} videos from playlist: {playlist_title}")

    for index, entry in enumerate(video_entries, start=1):
        video_url = entry["url"]
        video_title = entry["title"]

        # Download video (if not already downloaded)
        safe_file_name = download_video(video_url, output_directory, video_title, sanitized_season_name, index)
        if safe_file_name is None:
            continue  # Skip failed downloads

        # Get additional metadata
        video_info = entry  # No need for separate metadata file read

        description = video_info.get("description", "No description available.")
        publish_date = video_info.get("upload_date", "Unknown")
        publish_date = f"{publish_date[:4]}-{publish_date[4:6]}-{publish_date[6:]}" if publish_date != "Unknown" else "Unknown"

        # Save NFO metadata
        nfo_file = os.path.join(output_directory, f"{os.path.splitext(safe_file_name)[0]}.nfo")
        create_nfo_file(nfo_file, video_title, video_url, description, publish_date, season_number, index)

        # Download thumbnail
        thumbnail_url = video_info.get("thumbnail")
        if thumbnail_url:
            thumbnail_path = os.path.join(output_directory, f"{os.path.splitext(safe_file_name)[0]}.jpg")
            download_thumbnail(thumbnail_url, thumbnail_path)

        # Save video data
        video_data.append([safe_file_name, video_title])

        # **Prevent rate limiting by waiting 30 seconds**
        logging.info("Waiting 30 seconds before the next download...")
        time.sleep(30)

    # Save index to CSV
    csv_path = os.path.join(output_directory, "playlist_index.csv")
    df = pd.DataFrame(video_data, columns=["File Name", "Video Title"])
    df.to_csv(csv_path, index=False)

    logging.info(f"\nDownload complete! Videos saved in '{output_directory}'. Playlist index saved to '{csv_path}'.")

def parse_args():
    parser = argparse.ArgumentParser(description="Download an entire YouTube playlist with Emby metadata.")
    parser.add_argument("playlist_id", help="The YouTube playlist ID to download.")
    parser.add_argument("--reverse", action="store_true", help="Download episodes in reverse order.")
    parser.add_argument(
        "--season-name",
        help="Custom label for the season (e.g., 'Season 3', 'Miami'). Defaults to 'Season 01'."
    )
    return parser.parse_args()


if __name__ == "__main__":
    cli_args = parse_args()
    season_label = cli_args.season_name.strip() if cli_args.season_name else "Season 01"
    inferred = infer_season_number_from_name(season_label)
    season_number = inferred if inferred else 1
    download_playlist(
        cli_args.playlist_id,
        reverse_order=cli_args.reverse,
        season_name=season_label,
        season_number=season_number
    )
