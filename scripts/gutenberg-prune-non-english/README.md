# gutenberg-prune-non-english.py

Removes non-English books from a local [Project Gutenberg](https://www.gutenberg.org) EPUB mirror.

Downloads `pg_catalog.csv` from Gutenberg to determine each book's language, then deletes local directories for any book where English (`en`) is not listed as a language.

## Usage

```bash
# Dry run — shows what would be deleted without deleting anything
python3 gutenberg-prune-non-english.py --dir /path/to/gutenberg-epub --dry-run

# Real delete
python3 gutenberg-prune-non-english.py --dir /path/to/gutenberg-epub

# Use an already-downloaded catalog (skips re-downloading)
python3 gutenberg-prune-non-english.py --dir /path/to/gutenberg-epub --catalog /tmp/pg_catalog.csv
```

## Requirements

Python 3, no external dependencies.

## Notes

- Books with multiple languages (e.g. `en; fr`) are **kept** as long as `en` is one of them.
- The catalog is downloaded fresh from Gutenberg each run unless `--catalog` is specified.
- Pairs well with the rsync mirror command:
  ```bash
  rsync -avm --ignore-existing --include '*/' --include '*.epub' --exclude '*' --stats \
    rsync.ibiblio.org::gutenberg-epub /your/destination/
  ```
