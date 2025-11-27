# 🎥 YouTube Playlist Downloader (Emby-Ready)

This script downloads YouTube playlists. It also generates **Emby-compatible metadata** (`.nfo` & thumbnails) for seamless integration.

## 🚀 Features

✅ **Downloads videos in the highest quality available** (merges video and audio streams)\
✅ **Skips already downloaded files** (supports resuming)\
✅ **Generates Emby-compatible **`** and **`** files**\
✅ **Includes a 30-second delay to prevent rate limiting**\
✅ **Saves a CSV index of all downloaded videos**

---

## 📦 Installation

### **1️⃣ Install Required Dependencies**

First, install `yt-dlp`, `ffmpeg`, and Python packages:

```sh
sudo apt update && sudo apt install ffmpeg -y
# (Recommended) Use a Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade yt-dlp pandas requests
```

### **2️⃣ Clone or Download This Repository**

```sh
git clone https://github.com/morgang5522/yt-playlist-downloader.git
cd yt-playlist-downloader
```

---

## ▶️ **Usage**

### **Run the script with a YouTube Playlist ID**

```sh
python3 download-playlist.py PLAYLIST_ID [--reverse] [--season-name "Season 02"]
```

- `--reverse` downloads episodes in reverse order.
- `--season-name` controls both the folder label and the filename prefix. It defaults to `Season 01`, but you can pass text (e.g. `Miami`) or a number (e.g. `Season 2`). If the name contains a number, the script automatically uses it for the Emby metadata season number; otherwise it falls back to `1`.

Example:

```sh
python3 download-playlist.py PL1234567890ABCDEF --season-name "Season 02"
```

Using the helper script:

```sh
./download.sh PL1234567890ABCDEF --season-name "Live Shows" --reverse
```

### **Docker Usage (Manual)**

Build the Docker image:

```sh
docker build -t yt-downloader .
```

Run the container:

```sh
docker run --rm -v "$(pwd)/Download:/app/Download" yt-downloader PL1234567890ABCDEF [--reverse] [--season-name "Season 02"]
```

---

## 📂 Output Folder Structure (Emby-Compatible)

```
/Download/Playlist_Name/Season 01/
    Season 01 - E01 - Video Title.mp4
    Season 01 - E01 - Video Title.nfo
    Season 01 - E01 - Video Title.jpg
    Season 01 - E02 - Another Video.mp4
    Season 01 - E02 - Another Video.nfo
    Season 01 - E02 - Another Video.jpg
    playlist_index.csv
```

- **MP4** → Video file (merged video and audio)
- **NFO** → Metadata for Emby
- **JPG** → Thumbnail for Emby
- **CSV** → Playlist index

> Tip: pass a different `--season-name` to organize multiple playlists from the same creator into separate seasons. If the season name is numeric (like `Season 3`), the script automatically uses that number for the Emby metadata season value.

---

## ⚙️ Configuration

### **Modify Download Folder**

By default, videos are stored in:

```sh
/Download/Playlist_Name/
```

You can change this in the script:

```python
output_directory = os.path.join(os.getcwd(), "Download", playlist_title)
```

### **Change Delay Time**

To modify the 30-second delay between downloads:

```python
time.sleep(30)
```

---

## ❌ Troubleshooting

### **1️⃣ "HTTP Error 403: Forbidden"**

**Solution:** Update `yt-dlp`:

```sh
pip3 install --upgrade yt-dlp
```

### **2️⃣ Some Videos Are Missing**

Some videos might be **age-restricted or private**. Use:

```sh
yt-dlp --cookies-from-browser firefox "https://www.youtube.com/watch?v=VIDEO_ID"
```

### **3️⃣ No Space Left on Device**

If you're running out of space:

```sh
df -h  # Check disk usage
sudo rm -rf /var/lib/apt/lists/*  # Clear package cache
```

---

## 🎯 Why Use This?

- **Perfect for Emby users** (auto-generates metadata)
- **VPS-friendly** (low resource usage)
- **Supports resumable downloads** (won't re-download existing files)
- **Downloads highest quality video and audio** (merges streams)

🚀 **Enjoy downloading your YouTube playlists effortlessly!**

## 📝 License

See the [LICENSE](LICENSE) file for details.

## 🤖 AI-Generated Code

This code was completely generated with AI. Please review and test thoroughly before using in production environments.

---
