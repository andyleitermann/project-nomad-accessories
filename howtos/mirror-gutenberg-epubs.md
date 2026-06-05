# Mirroring All of Project Gutenberg as EPUBs

*Project Gutenberg offers a full rsync mirror of their EPUB catalog. The obvious server to use is `aleph.gutenberg.org`, which is what most guides reference — but it's heavily throttled. After 9 days of crawling I'd only pulled about 60% of the collection. Switching to `rsync.ibiblio.org` (an unthrottled mirror) finished the remaining 40% in under an hour. Use ibiblio.*

---

**Tools:** `rsync`, optionally `systemd` for unattended runs

---

**Step 1 — Run the rsync**

```bash
rsync -avm --ignore-existing --include '*/' --include '*.epub' --exclude '*' --stats \
  rsync.ibiblio.org::gutenberg-epub /your/destination/
```

- `--ignore-existing` skips files already on disk without comparing checksums — critical for fast restarts if the connection drops
- `--include '*/'` is required; without it rsync won't recurse into subdirectories
- `--stats` prints a summary when complete
- The full collection is ~232,000 EPUBs across ~133,000 directories (~20% non-English)

This took about 1-2 hours on a home connection. Expect significant RAM usage (~15GB) while rsync builds the remote file list before transfers begin.

---

**Step 2 — Run it as a systemd service (optional but recommended)**

For large unattended downloads, a systemd service with `Restart=on-failure` handles connection drops cleanly.

`/etc/systemd/system/gutenberg-epub-rsync.service`:

```ini
[Unit]
Description=Project Gutenberg EPUB rsync mirror
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=youruser
ExecStart=/usr/bin/rsync -avm --ignore-existing --include '*/' --include '*.epub' --exclude '*' --stats rsync.ibiblio.org::gutenberg-epub /your/destination/
Restart=on-failure
RestartSec=60
StandardOutput=append:/home/youruser/logs/gutenberg-epub-rsync.log
StandardError=append:/home/youruser/logs/gutenberg-epub-rsync.log

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gutenberg-epub-rsync.service
```

The service exits cleanly when rsync completes and won't restart again (since there's no failure). Check progress by counting EPUBs:

```bash
find /your/destination -name '*.epub' | wc -l
```

---

**Step 3 — Prune non-English books**

About 20% of the collection is non-English. Use the companion script [`gutenberg-prune-non-english.py`](gutenberg-prune-non-english.md) to remove those directories using Gutenberg's own catalog:

```bash
# Dry run first
python3 gutenberg-prune-non-english.py --dir /your/destination --dry-run

# Then for real
python3 gutenberg-prune-non-english.py --dir /your/destination
```

This removes ~16,000 directories and leaves you with ~62,000 English books.

---

**Step 4 — Import into Calibre (optional)**

If you're running Calibre-Web, import the collection into your library:

```bash
nohup calibredb add --recurse /your/destination \
  --library-path /path/to/calibre/library \
  --log ~/logs/gutenberg-calibre-import.log &
```

Expect this to take 18–44 hours for the full English collection.

---

**Notes:**
- Don't use `aleph.gutenberg.org` — it's throttled and took 9 days to get 60% of the way through in my experience.
- The `--ignore-existing` flag is what makes restarts fast. Without it, rsync checksums every file it's already downloaded on each new run, which on 232,000 files takes days.
- rsync builds the complete remote file list in RAM before starting transfers. On a 232k-file collection this peaks around 15GB. Don't be alarmed.
