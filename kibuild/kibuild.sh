#!/bin/bash
# Rebuild the Kiwix library index and restart the Kiwix container.
# Run this after adding or removing ZIM files from your NOMAD Kiwix library.

ZIM_DIR="/opt/project-nomad/storage/zim"
KIWIX_CONTAINER="nomad_kiwix_server"
ICON_PATCH="$(dirname "$0")/icons/kiwix-icon-patch.py"

docker run --rm \
  -v "${ZIM_DIR}:/data" \
  --entrypoint sh \
  ghcr.io/kiwix/kiwix-tools:latest \
  -c 'rm -f /data/kiwix-library.xml && kiwix-manage /data/kiwix-library.xml add /data/*.zim'

# Optional: patch custom icons if the patch script is present
if [ -f "$ICON_PATCH" ]; then
  sudo chown "$(whoami)" "${ZIM_DIR}/kiwix-library.xml"
  python3 "$ICON_PATCH" "$ZIM_DIR"
fi

docker restart "$KIWIX_CONTAINER"
