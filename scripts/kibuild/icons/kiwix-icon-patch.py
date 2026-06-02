#!/usr/bin/env python3
"""
Patch kiwix-library.xml with custom favicons.
Run after kiwix-manage, before docker restart nomad_kiwix_server.

Usage:
    python3 kiwix-icon-patch.py [zim_dir]

Icons stored as {zim_name}.png in a 'kiwix-icons' subdirectory of zim_dir.
Default zim_dir: /opt/project-nomad/storage/zim
"""
import base64, os, re, sys

ZIM_DIR = sys.argv[1] if len(sys.argv) > 1 else "/opt/project-nomad/storage/zim"
LIBRARY = os.path.join(ZIM_DIR, "kiwix-library.xml")
ICONS_DIR = os.path.join(ZIM_DIR, "kiwix-icons")

def b64_icon(name):
    path = os.path.join(ICONS_DIR, f"{name}.png")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

if not os.path.exists(LIBRARY):
    print(f"Library not found: {LIBRARY}", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(ICONS_DIR):
    print(f"Icons dir not found: {ICONS_DIR} — skipping icon patch")
    sys.exit(0)

with open(LIBRARY, "r", encoding="utf-8") as f:
    xml = f.read()

def patch_book(match):
    tag = match.group(0)
    name_m = re.search(r'\bname="([^"]+)"', tag)
    if not name_m:
        return tag
    zim_name = name_m.group(1)
    icon_b64 = b64_icon(zim_name)
    if icon_b64 is None:
        return tag
    tag = re.sub(r'\s+faviconMimeType="[^"]*"', '', tag)
    tag = re.sub(r'\s+favicon="[^"]*"', '', tag)
    tag = re.sub(r'\s*/>$', f' faviconMimeType="image/png" favicon="{icon_b64}" />', tag)
    print(f"  patched: {zim_name}")
    return tag

patched = re.sub(r'<book\b.*?/>', patch_book, xml, flags=re.DOTALL)

with open(LIBRARY, "w", encoding="utf-8") as f:
    f.write(patched)

print("Icon patch complete.")
