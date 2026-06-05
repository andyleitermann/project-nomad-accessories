# extract-books-from-zim.py

Extracts book files (PDF, EPUB, MOBI, etc.) from a Kiwix ZIM archive and imports them into a Calibre library.

Useful for ZIM files that embed downloadable books — for example, the [Survivor Library](https://www.survivorlibrary.com/) ZIM contains over 14,000 PDFs.

## Requirements

- `zimdump` (`sudo apt install zim-tools`)
- `calibredb` (installed with Calibre)
- Python 3, no extra dependencies

## Usage

```bash
# Dry run — see what would be extracted
python3 extract-books-from-zim.py archive.zim --library-path /path/to/calibre --dry-run

# Extract and import (PDF, EPUB, MOBI, DJVU, FB2, AZW, AZW3 by default)
python3 extract-books-from-zim.py archive.zim --library-path /path/to/calibre

# PDFs only
python3 extract-books-from-zim.py archive.zim --library-path /path/to/calibre --formats pdf

# Keep extracted files in a specific staging directory after import
python3 extract-books-from-zim.py archive.zim --library-path /path/to/calibre \
  --staging-dir ~/staging --keep-staging
```

## Options

| Option | Description |
|---|---|
| `--library-path` | Path to Calibre library (required) |
| `--formats` | Comma-separated formats to extract (default: `pdf,epub,mobi,djvu,fb2,azw,azw3`) |
| `--staging-dir` | Where to extract files; uses a temp dir if not specified |
| `--keep-staging` | Keep extracted files after import |
| `--dry-run` | List what would be extracted without doing anything |

## Notes

- Files are extracted one at a time using `zimdump show` — only book files are written to disk, no HTML or images.
- Filename collisions (two entries with the same basename) are resolved by appending the entry index.
- If `calibredb` is locked by another running import, wait for it to finish first.
