# kibuild

A simple script for [Project N.O.M.A.D.](https://github.com/Crosstalk-Solutions/project-nomad) that rebuilds the Kiwix library index after adding or removing ZIM files.

## The Problem

When you add a new ZIM file to your NOMAD Kiwix library, Kiwix doesn't automatically pick it up. You have to regenerate the library index and restart the container. This script does that in one command.

## Installation

```bash
curl -O https://raw.githubusercontent.com/andyleitermann/project-nomad-accessories/main/kibuild/kibuild.sh
chmod +x kibuild.sh
sudo mv kibuild.sh /usr/local/bin/kibuild
```

Then just run:

```bash
kibuild
```

## What It Does

1. Uses the `kiwix-tools` Docker image to regenerate `kiwix-library.xml` from all `*.zim` files in your ZIM directory
2. Optionally patches custom icons into the library index (see below)
3. Restarts the `nomad_kiwix_server` container so Kiwix picks up the changes

## Requirements

- Project N.O.M.A.D. installed and running
- Docker
- ZIM files in `/opt/project-nomad/storage/zim/`

## Optional: Custom ZIM Icons

By default, ZIM files you build yourself often show a generic placeholder question-mark icon in the Kiwix library. The `icons/` directory contains an optional patch system that injects custom 48x48 PNG icons into the library index automatically on each kibuild run.

See [icons/README.md](icons/README.md) for setup instructions.

## Notes

- `kiwix-tools` is pulled automatically by Docker on first run — no manual install needed
- Safe to run at any time; Kiwix will be briefly unavailable during the container restart
- If you run kibuild as an alias rather than a script, the icon patch will not run automatically unless you add it to the alias manually
