#!/usr/bin/env python3
"""Generate every app, installer and web icon from tools/rebrand/assets:
emblem-source.png (rhinoceros emblem, used for icons) and logo-source.png
(emblem with wordmark, used for the installer sidebar and in-app logo).

Needs Pillow. Run from the repository root:
    python3 -I tools/rebrand/make_icons.py
Replace the two source images (and ICON_BOX below) with new artwork and re-run to update all sizes.
"""
from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path.cwd()
SRC = ROOT / "tools/rebrand/assets/logo-source.png"
EMBLEM = ROOT / "tools/rebrand/assets/emblem-source.png"
# Square region of the emblem holding the rhinoceros head (left, top, right, bottom).
ICON_BOX = (298, 222, 958, 882)
NIGHT = (6, 6, 24)
ICONS = ROOT / "desktop/src-tauri/icons"
GRAPHITE = (35, 38, 43)
PAPER = (242, 238, 228)
RED = (216, 54, 42)


def icon_master(size: int = 1024) -> Image.Image:
    """Rhinoceros head on its dark field, with rounded corners."""
    head = Image.open(EMBLEM).convert("RGBA").crop(ICON_BOX).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.2), fill=255)
    head.putalpha(mask)
    return head


def svg_wrap(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    w, h = img.size
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
        f"<title>ArchiSavvyERP</title>"
        f'<image width="{w}" height="{h}" href="data:image/png;base64,{data}"/></svg>\n'
    )


def main() -> None:
    master = icon_master()
    full = Image.open(SRC).convert("RGB")
    for path in sorted(ICONS.rglob("*.png")):
        w, h = Image.open(path).size
        master.resize((w, h), Image.LANCZOS).save(path)
    master.save(ICONS / "icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (256, 256)])
    master.save(ICONS / "icon.icns")

    # NSIS installer artwork (24-bit BMP, sizes fixed by NSIS).
    # The header strip sits on the installer's white title band, so its
    # background must be white: only the rounded icon shows, at the right edge,
    # next to the page title (same layout as the original artwork).
    header = Image.new("RGB", (150, 57), (255, 255, 255))
    small = master.resize((45, 45), Image.LANCZOS)
    header.paste(small, (99, 6), small)
    header.save(ROOT / "desktop/src-tauri/installer/header.bmp")
    side = Image.new("RGB", (164, 314), NIGHT)
    fw = 164
    fh = round(full.height * fw / full.width)
    side.paste(full.resize((fw, fh), Image.LANCZOS), (0, (314 - fh) // 2))
    side.save(ROOT / "desktop/src-tauri/installer/sidebar.bmp")

    # Web assets: SVG wrappers so existing /logo.svg and /favicon.svg references keep working.
    pub = ROOT / "frontend/public"
    (pub / "logo.svg").write_text(svg_wrap(master.resize((256, 256), Image.LANCZOS)), encoding="utf-8")
    (pub / "favicon.svg").write_text(svg_wrap(master.resize((96, 96), Image.LANCZOS)), encoding="utf-8")
    for path in (pub / "pwa").glob("*.svg"):
        path.write_text(svg_wrap(master.resize((192, 192), Image.LANCZOS)), encoding="utf-8")
    brand = pub / "brand"
    full.resize((900, round(full.height * 900 / full.width)), Image.LANCZOS).save(brand / "archi-savvy-logo.webp", quality=88)
    print("icons written")


if __name__ == "__main__":
    main()
