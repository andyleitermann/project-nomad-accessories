#!/usr/bin/env python3
"""
gutenberg-prune-non-english.py
Remove non-English books from a local Gutenberg EPUB mirror.
Downloads pg_catalog.csv from gutenberg.org to determine language.
Books with 'en' anywhere in their language field are kept.

Usage:
  python3 gutenberg-prune-non-english.py --dir /mnt/bulk/gutenberg-epub [--dry-run]
"""

import argparse
import csv
import shutil
import urllib.request
import sys
from pathlib import Path

CATALOG_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"

def main():
    parser = argparse.ArgumentParser(description="Prune non-English books from Gutenberg EPUB mirror")
    parser.add_argument("--dir", required=True, help="Path to gutenberg-epub mirror directory")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be deleted without deleting")
    parser.add_argument("--catalog", help="Path to local pg_catalog.csv (skips download)")
    args = parser.parse_args()

    mirror_dir = Path(args.dir)
    if not mirror_dir.is_dir():
        print(f"Error: {mirror_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Download or use local catalog
    if args.catalog:
        catalog_path = args.catalog
        print(f"Using local catalog: {catalog_path}")
    else:
        catalog_path = "/tmp/pg_catalog.csv"
        print(f"Downloading catalog from {CATALOG_URL} ...")
        urllib.request.urlretrieve(CATALOG_URL, catalog_path)
        print("Download complete.")

    # Parse catalog
    non_english_ids = []
    english_count = 0

    with open(catalog_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lang = row["Language"].strip()
            book_id = row["Text#"].strip()
            if "en" in lang.split("; "):
                english_count += 1
            else:
                non_english_ids.append(book_id)

    print(f"\nCatalog: {english_count + len(non_english_ids):,} entries total")
    print(f"  English (keep): {english_count:,}")
    print(f"  Non-English in catalog: {len(non_english_ids):,}")

    # Find which non-English dirs exist locally
    to_delete = [mirror_dir / bid for bid in non_english_ids if (mirror_dir / bid).is_dir()]
    print(f"  Non-English dirs found locally: {len(to_delete):,}")

    if not to_delete:
        print("\nNothing to delete.")
        return

    if args.dry_run:
        print(f"\n[DRY RUN] Would delete {len(to_delete):,} directories:")
        for d in to_delete[:20]:
            print(f"  {d}")
        if len(to_delete) > 20:
            print(f"  ... and {len(to_delete) - 20} more")
        return

    # Delete
    print(f"\nDeleting {len(to_delete):,} directories...")
    deleted = 0
    errors = 0
    for d in to_delete:
        try:
            shutil.rmtree(d)
            deleted += 1
            if deleted % 1000 == 0:
                print(f"  {deleted:,} deleted...")
        except Exception as e:
            print(f"  Error deleting {d}: {e}", file=sys.stderr)
            errors += 1

    print(f"\nDone. Deleted: {deleted:,}  Errors: {errors}")

if __name__ == "__main__":
    main()
