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
python3 download-playlist.py PLAYLIST_ID [--reverse]
```

Example:

```sh
python3 download-playlist.py PL1234567890ABCDEF --reverse
```

### **Docker Usage**

Build the Docker image:

```sh
docker build -t yt-downloader .
```

Run the container:

```sh
docker run --rm -v "$(pwd)/Download:/app/Download" yt-downloader PL1234567890ABCDEF [--reverse]
```

---

## 📂 Output Folder Structure (Emby-Compatible)

```
/Download/Playlist_Name/Season 01/
    S01E01 - Video Title.mp4
    S01E01 - Video Title.nfo
    S01E01 - Video Title.jpg
    S01E02 - Another Video.mp4
    S01E02 - Another Video.nfo
    S01E02 - Another Video.jpg
    playlist_index.csv
```

- **MP4** → Video file (merged video and audio)
- **NFO** → Metadata for Emby
- **JPG** → Thumbnail for Emby
- **CSV** → Playlist index

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤖 AI-Generated Code

This code was completely generated with AI. Please review and test thoroughly before using in production environments.

---
