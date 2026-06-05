# extract-books-from-zim.py

Extracts book files (PDF, EPUB, MOBI, etc.) from a Kiwix ZIM archive. Optionally imports them into a Calibre library.

Useful for ZIM files that embed downloadable books — for example, the [Survivor Library](https://www.survivorlibrary.com/) ZIM contains over 14,000 PDFs.

## Requirements

- `zimdump` (`sudo apt install zim-tools`)
- `calibredb` (installed with Calibre) — only needed if importing into Calibre
- Python 3, no extra dependencies

## Usage

```bash
# Extract to a directory (no Calibre needed)
python3 extract-books-from-zim.py archive.zim --output-dir /path/to/output

# Extract and import into Calibre
python3 extract-books-from-zim.py archive.zim --library-path /path/to/calibre

# Dry run — see what would be extracted without doing anything
python3 extract-books-from-zim.py archive.zim --output-dir /tmp/books --dry-run

# PDFs only
python3 extract-books-from-zim.py archive.zim --output-dir /tmp/books --formats pdf

# Import into Calibre but keep the extracted files too
python3 extract-books-from-zim.py archive.zim --library-path /path/to/calibre \
  --staging-dir ~/staging --keep-staging
```

## Options

| Option | Description |
|---|---|
| `--output-dir` | Extract files here and stop (no Calibre import) |
| `--library-path` | Import into this Calibre library after extraction |
| `--formats` | Comma-separated formats to extract (default: `pdf,epub,mobi,djvu,fb2,azw,azw3`) |
| `--staging-dir` | Temp directory for files before Calibre import (default: system temp) |
| `--keep-staging` | Keep extracted files after Calibre import |
| `--dry-run` | List what would be extracted without doing anything |

One of `--output-dir` or `--library-path` is required.

## Notes

- Files are extracted one at a time using `zimdump show` — only book files touch disk, no HTML or images.
- Filename collisions (two entries with the same basename) are resolved by appending the entry index.
- If `calibredb` is locked by another running import, wait for it to finish first.
