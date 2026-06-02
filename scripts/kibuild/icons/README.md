# kibuild — Custom ZIM Icons

ZIM files built with `zimwriterfs` (e.g. YouTube channel archives) often show a generic placeholder icon in the Kiwix library. This optional add-on patches custom 48x48 PNG icons into the library index on every kibuild run.

## How It Works

The patch script reads `kiwix-library.xml` after it's generated and injects base64-encoded PNG icons for any ZIM whose `name` attribute matches a file in the `kiwix-icons/` directory. Icons that don't match a ZIM are silently ignored.

## Setup

1. Create an icons directory inside your ZIM directory:
   ```bash
   mkdir -p /opt/project-nomad/storage/zim/kiwix-icons
   ```

2. Add 48x48 PNG icons named after the ZIM's `name` attribute:
   ```
   kiwix-icons/
   ├── paul_harrell_en.png
   ├── field_manuals.png
   └── hrcc_morse_en.png
   ```
   To find a ZIM's name, check `kiwix-library.xml` for the `name="..."` attribute on its `<book>` entry.

3. Place `kiwix-icon-patch.py` somewhere accessible (e.g. `/opt/project-nomad/`) and ensure the icon patch line is in your kibuild alias or script.

## Generating Icons with Pillow

You can generate simple but recognizable 48x48 icons using Python's Pillow library:

```python
from PIL import Image, ImageDraw
img = Image.new("RGB", (48, 48), "#0a0a0a")
d = ImageDraw.Draw(img)
# draw your icon here
img.save("/opt/project-nomad/storage/zim/kiwix-icons/my_zim_name.png", "PNG")
```

## Notes

- Icons must be exactly 48x48 PNG — this is a Kiwix requirement
- The patch runs after `kiwix-manage` and before `docker restart`, so icons survive every kibuild
- ZIMs from the Kiwix library already have their own icons and won't be overwritten unless you explicitly add a matching file
