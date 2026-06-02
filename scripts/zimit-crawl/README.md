# zimit-crawl

A wrapper around [Zimit](https://github.com/openzim/zimit) for [Project N.O.M.A.D.](https://github.com/Crosstalk-Solutions/project-nomad) that crawls a website and adds it to your Kiwix offline library in one command.

## What It Does

1. Crawls a website using the Zimit Docker image
2. Packages it as a `.zim` file in your NOMAD ZIM directory
3. Rebuilds the Kiwix library index
4. Restarts Kiwix so the new content is immediately available

## Installation

```bash
curl -O https://raw.githubusercontent.com/andyleitermann/project-nomad-accessories/main/scripts/zimit-crawl/zimit-crawl
chmod +x zimit-crawl
sudo mv zimit-crawl /usr/local/bin/zimit-crawl
```

## Usage

```bash
zimit-crawl --url <url> --name <zim_name> --title <title> [options]
```

### Required Arguments

| Argument | Description |
|---|---|
| `--url` | URL to crawl (e.g. `https://example.com/docs`) |
| `--name` | ZIM identifier — lowercase, underscores (e.g. `example_docs_en`) |
| `--title` | Display name in Kiwix — **max 30 characters** |

### Optional Arguments

| Argument | Default | Description |
|---|---|---|
| `--desc` | Auto-generated | Short description shown in Kiwix |
| `--depth` | `5` | How many links deep to follow |
| `--limit` | `500` | Max pages to crawl |
| `--workers` | `2` | Parallel browser workers |
| `--exclude` | — | Regex of URL paths to skip |
| `--no-kibuild` | — | Skip Kiwix reload after crawl |

### Examples

**Basic crawl:**
```bash
zimit-crawl \
  --url "https://theboxotruth.com" \
  --name "boxotruth_en" \
  --title "Box O Truth"
```

**Crawl a subdirectory only:**
```bash
zimit-crawl \
  --url "https://www.luckygunner.com/labs" \
  --name "luckygunner_labs_en" \
  --title "Lucky Gunner Labs" \
  --desc "Ammunition ballistics testing and data"
```

**Crawl with exclusions (skip store/login pages):**
```bash
zimit-crawl \
  --url "https://example.com" \
  --name "example_en" \
  --title "Example Site" \
  --exclude "/cart|/checkout|/account|/login|\?s="
```

**Crawl without auto-reloading Kiwix:**
```bash
zimit-crawl \
  --url "https://example.com" \
  --name "example_en" \
  --title "Example Site" \
  --no-kibuild
```

## Configuration

The following environment variables override defaults:

| Variable | Default | Description |
|---|---|---|
| `NOMAD_ZIM_DIR` | `/opt/project-nomad/storage/zim` | Where ZIM files are stored |
| `NOMAD_KIWIX_CONTAINER` | `nomad_kiwix_server` | Kiwix Docker container name |
| `NOMAD_ICON_PATCH` | `/opt/project-nomad/kiwix-icon-patch.py` | Optional icon patch script path |

## Requirements

- Project N.O.M.A.D. installed and running
- Docker (Zimit and kiwix-tools images are pulled automatically on first run)

## Notes

- **Scope:** By default, zimit-crawl uses `prefix` scope — it only crawls pages under the URL path you specify. This prevents crawling the entire domain when you give a specific path like `/docs` or `/labs`.
- **Title limit:** Kiwix enforces a 30-character title limit. zimit-crawl will error before starting if your title is too long.
- **Kiwix downtime:** Kiwix will be briefly unavailable during the library reload at the end. Usually under 30 seconds.
- **Disqus/Facebook errors** in the crawl log are normal and harmless — third-party trackers being blocked by the crawler.
