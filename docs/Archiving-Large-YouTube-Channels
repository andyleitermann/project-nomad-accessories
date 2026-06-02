# Archiving a Large YouTube Channel for Offline Viewing in Kiwix
  
*Note: youtube2zim is purpose-built for turning YouTube channels into zims in one shot. It requires a YouTube Data API v3 key (free from Google Cloud), and it's probably the right option for most cases. In my case, it was a little inflexible for what I needed, because it's a single operation that can't be stopped and resumed easily if the connection breaks, and I kept having other failures. So this is what I was able actually get working for such large channels like youtube.com/@PaulHarrell.*

---

**Tools:** `zimwriterfs`, and `yt-dlp`, which requires `ffmpeg`

**Step 1 — Download the channel**

`yt-dlp \
    --download-archive /path/to/.downloaded \
    -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/
  best[height<=1080]" \
    --merge-output-format mp4 \
    -o "/path/to/output/%(upload_date)s - %(title)s [%(id)s].%(ext)s" \
    --sleep-interval 3 \
    --max-sleep-interval 8 \
    --ignore-errors \
    "https://www.youtube.com/@ChannelName/videos"`

- --download-archive tracks what's already downloaded so restarts are safe
- --sleep-interval / --max-sleep-interval adds random delay between downloads to avoid
  throttling
- --ignore-errors skips unavailable videos instead of stopping
- The filename format includes upload date so videos sort chronologically

This can take days for large channels. Run it as a systemd service with RestartSec=300 so it auto-resumes if it gets throttled or interrupted.

---
**Step 2 — Build the HTML structure for zimwriterfs**

You need a directory with:
- index.html — channel homepage listing all videos
- video-pages/ — one HTML page per video
- videos/ — hardlinks (not copies) to the actual MP4 files
- whatever other assets you'd like to include in the final ZIM
  
The HTML pages link to the local MP4s. Hardlinks keep disk usage from doubling since the files are already on disk.

---
**Step 3 — Generate the ZIM**

`zimwriterfs \
  --welcome index.html \
  --language eng \
  --title "Paul Harrell" \
  --description "Paul Harrell YouTube channel archive" \
  --creator "Paul Harrell" \
  --publisher "Self" \
  --name "paul-harrell" \
  /path/to/build-dir /path/to/output.zim`

This compresses everything into a single portable ZIM file. Expect roughly 50% compression on MP4s — my 449GB of video became a 225GB ZIM.

---
**Step 4 — Load into Kiwix**
  
Drop the .zim file into your Kiwix library directory and restart the Kiwix server container. It'll show up automatically in the web UI.

---
**Notes:**
- YouTube does throttle large downloads. The sleep intervals help but you may still get interrupted. The archive file handles resuming cleanly (which is partly why I was having trouble with youtube2zim on this).
- For channels with hundreds of videos, the HTML build step is the tricky part. You probably want a script to generate the index and per-video pages. Happy to share that as well if people want.
