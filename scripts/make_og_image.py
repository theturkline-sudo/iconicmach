# -*- coding: utf-8 -*-
"""Generate the 1200x630 social share image.

    python scripts/make_og_image.py

og:image was pointing at a 720x720 square logo. WhatsApp, LinkedIn and X all
expect roughly 1.91:1 and crop or letterbox anything else — so every link the
sales team shared rendered badly, on WhatsApp especially, which is this
business's main outreach channel.

Re-run this if the logo or brand colours change. Output is committed, so the
site does not depend on Pillow at deploy time.
"""

from __future__ import print_function

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "og-image.png")
LOGO = os.path.join(ROOT, "assets", "images", "footer_logo.png")

W, H = 1200, 630
NAVY = (10, 34, 64)
NAVY_LIGHT = (20, 61, 108)
MINT = (74, 222, 174)
WHITE = (255, 255, 255)
MUTED = (201, 216, 236)

FONT_DIR = r"C:\Windows\Fonts"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except (OSError, IOError):
        return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Subtle diagonal wash so the card is not a flat rectangle.
    for x in range(W):
        t = x / float(W)
        d.line(
            [(x, 0), (x, H)],
            fill=(
                int(NAVY[0] + (NAVY_LIGHT[0] - NAVY[0]) * t),
                int(NAVY[1] + (NAVY_LIGHT[1] - NAVY[1]) * t),
                int(NAVY[2] + (NAVY_LIGHT[2] - NAVY[2]) * t),
            ),
        )

    # Accent bar, mirroring the site's mint highlight.
    d.rectangle([0, 0, 14, H], fill=MINT)

    # Logo, right side, sized to leave room for text.
    if os.path.exists(LOGO):
        logo = Image.open(LOGO).convert("RGBA")
        target = 300
        logo = logo.resize((target, target), Image.LANCZOS)
        img.paste(logo, (W - target - 80, (H - target) // 2), logo)

    x = 80
    d.text((x, 168), "ICONIC MACH", font=font("arialbd.ttf", 68), fill=WHITE)
    d.text((x, 250), "ENGINEERING", font=font("arial.ttf", 44), fill=MINT)

    d.line([(x, 330), (x + 120, 330)], fill=MINT, width=4)

    d.text((x, 366), "Production Lines & Conveyor Systems",
           font=font("arial.ttf", 30), fill=WHITE)
    d.text((x, 412), "Design, manufacture and installation",
           font=font("arial.ttf", 25), fill=MUTED)
    d.text((x, 450), "across Egypt and the GCC",
           font=font("arial.ttf", 25), fill=MUTED)

    d.text((x, 520), "iconicmach.com", font=font("arialbd.ttf", 27), fill=MINT)

    img.save(OUT, "PNG", optimize=True)
    kb = os.path.getsize(OUT) / 1024.0
    print("wrote {} ({}x{}, {:.0f} KB)".format(
        os.path.relpath(OUT, ROOT), img.width, img.height, kb))
    return 0


if __name__ == "__main__":
    sys.exit(main())
