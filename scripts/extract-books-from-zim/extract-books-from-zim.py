#!/usr/bin/env python3
"""
extract-books-from-zim.py
Extract book files from a ZIM archive, optionally importing them into a Calibre library.

Usage:
  python3 extract-books-from-zim.py <zim-file> --output-dir /path/to/books [options]
  python3 extract-books-from-zim.py <zim-file> --library-path /path/to/calibre [options]
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_FORMATS = ['pdf', 'epub', 'mobi', 'djvu', 'fb2', 'azw', 'azw3']


def list_book_entries(zim_file, formats):
    result = subprocess.run(
        ['zimdump', 'list', '--', zim_file],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error listing ZIM contents: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    entries = []
    for line in result.stdout.splitlines():
        url = line.strip()
        ext = url.rsplit('.', 1)[-1].lower() if '.' in url else ''
        if ext in formats:
            entries.append(url)
    return entries


def extract_entry(zim_file, url, output_path):
    result = subprocess.run(
        ['zimdump', 'show', f'--url={url}', '--', zim_file],
        capture_output=True
    )
    if result.returncode != 0:
        return False
    with open(output_path, 'wb') as f:
        f.write(result.stdout)
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Extract books from a ZIM file and import into Calibre'
    )
    parser.add_argument('zim_file', help='Path to the ZIM file')
    parser.add_argument('--library-path', help='Path to Calibre library (import after extraction)')
    parser.add_argument('--output-dir', help='Extract files here without importing into Calibre')
    parser.add_argument(
        '--formats',
        default=','.join(DEFAULT_FORMATS),
        help=f'Comma-separated formats to extract (default: {",".join(DEFAULT_FORMATS)})'
    )
    parser.add_argument('--staging-dir', help='Temp directory for extracted files before Calibre import (default: temp dir)')
    parser.add_argument('--keep-staging', action='store_true', help='Keep extracted files after Calibre import')
    parser.add_argument('--dry-run', action='store_true', help='List what would be extracted without extracting')
    args = parser.parse_args()

    zim_file = str(Path(args.zim_file).resolve())
    if not os.path.isfile(zim_file):
        print(f"Error: ZIM file not found: {zim_file}", file=sys.stderr)
        sys.exit(1)

    if not args.library_path and not args.output_dir:
        print("Error: provide --library-path (import into Calibre) or --output-dir (extract only)", file=sys.stderr)
        sys.exit(1)

    formats = {f.strip().lower() for f in args.formats.split(',')}

    print(f"Scanning {zim_file} for formats: {', '.join(sorted(formats))} ...")
    entries = list_book_entries(zim_file, formats)

    if not entries:
        print("No matching book files found in ZIM.")
        return

    print(f"Found {len(entries):,} book files.")

    if args.dry_run:
        print(f"\n[DRY RUN] Would extract:")
        for e in entries[:20]:
            print(f"  {e}")
        if len(entries) > 20:
            print(f"  ... and {len(entries) - 20} more")
        return

    # Set up output/staging dir
    extract_only = bool(args.output_dir)
    temp_dir = None
    if args.output_dir:
        staging_dir = Path(args.output_dir)
        staging_dir.mkdir(parents=True, exist_ok=True)
    elif args.staging_dir:
        staging_dir = Path(args.staging_dir)
        staging_dir.mkdir(parents=True, exist_ok=True)
    else:
        temp_dir = tempfile.mkdtemp(prefix='zim-extract-')
        staging_dir = Path(temp_dir)

    print(f"Extracting to: {staging_dir}")

    try:
        extracted = 0
        errors = 0
        renamed = 0

        for i, url in enumerate(entries, 1):
            filename = url.rsplit('/', 1)[-1]
            output_path = staging_dir / filename
            if output_path.exists():
                stem = output_path.stem
                ext = output_path.suffix
                output_path = staging_dir / f"{stem}_{i}{ext}"
                renamed += 1

            if extract_entry(zim_file, url, output_path):
                extracted += 1
            else:
                errors += 1

            if i % 500 == 0:
                print(f"  {i:,}/{len(entries):,} processed ({extracted:,} extracted, {errors} errors)...")

        print(f"\nExtraction complete: {extracted:,} files, {errors} errors, {renamed} renamed (collision)")

        if extracted == 0:
            print("Nothing to import.")
            return

        if extract_only:
            print(f"\nExtraction complete. Files are in: {staging_dir}")
            return

        print(f"\nImporting into Calibre library: {args.library_path}")
        result = subprocess.run(
            ['calibredb', 'add', '-r', str(staging_dir), '--library-path', args.library_path]
        )
        if result.returncode != 0:
            print("calibredb exited with errors — check output above.", file=sys.stderr)

    finally:
        if extract_only:
            pass  # always keep --output-dir files
        elif not args.keep_staging:
            if temp_dir:
                shutil.rmtree(temp_dir, ignore_errors=True)
            elif args.staging_dir:
                shutil.rmtree(staging_dir, ignore_errors=True)
        else:
            print(f"\nStaging files kept at: {staging_dir}")


if __name__ == '__main__':
    main()
