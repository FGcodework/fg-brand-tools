#!/usr/bin/env python3
"""FG brand logo for plg_system_fgcustomrightclick (System - FG Custom Right Click).

Mark: computer mouse with the RIGHT button in coral (the plugin is about the
right click), blocked by a coral "prohibited" badge.

FG standard: 512x512 rounded tile (rx=95 = 18.55%, matching the other FG
logos and the fg-banner-generator JED frame: 56px radius / 302px inner box), navy gradient #081D32 -> #113758,
coral #FF6B4A accent, white mark, flat (no shadow), strictly binary alpha.

Output: logo.svg + logo.png (copy both to the plugin repo's assets/).
"""
import io
import cairosvg
from PIL import Image

NAVY_1, NAVY_2 = "#081D32", "#113758"
CORAL, WHITE = "#FF6B4A", "#FFFFFF"


def ban_badge(cx, cy, r):
    """Coral badge with a navy cut-out ring and a white 'prohibited' glyph."""
    g = r * 0.52
    w = r * 0.17
    d = g * 0.7071
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r + 10}" fill="{NAVY_1}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CORAL}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{g:.2f}" fill="none" stroke="{WHITE}" stroke-width="{w:.2f}"/>'
        f'<line x1="{cx - d:.2f}" y1="{cy - d:.2f}" x2="{cx + d:.2f}" y2="{cy + d:.2f}" '
        f'stroke="{WHITE}" stroke-width="{w:.2f}" stroke-linecap="round"/>'
    )


def mark():
    x, y, w, h = 124, 78, 216, 330
    split = y + 132
    mid = x + w / 2
    return (
        f'<defs><clipPath id="body"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w / 2}"/></clipPath></defs>'
        # mouse body
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w / 2}" fill="{WHITE}"/>'
        # right button in coral
        f'<rect x="{mid}" y="{y}" width="{w / 2}" height="{split - y}" fill="{CORAL}" clip-path="url(#body)"/>'
        # button split lines + scroll wheel
        f'<line x1="{mid}" y1="{y}" x2="{mid}" y2="{split}" stroke="{NAVY_1}" stroke-width="10"/>'
        f'<line x1="{x}" y1="{split}" x2="{x + w}" y2="{split}" stroke="{NAVY_1}" stroke-width="10"/>'
        f'<rect x="{mid - 14}" y="{y + 40}" width="28" height="58" rx="14" fill="{NAVY_1}"/>'
        + ban_badge(372, 376, 84)
    )


SVG = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="{NAVY_1}"/><stop offset="100%" stop-color="{NAVY_2}"/>
</linearGradient></defs>
<rect x="0" y="0" width="512" height="512" rx="95" ry="95" fill="url(#bg)"/>
{mark()}
</svg>
'''

if __name__ == "__main__":
    with open("logo.svg", "w", encoding="utf-8") as f:
        f.write(SVG)
    png = cairosvg.svg2png(bytestring=SVG.encode(), output_width=512, output_height=512)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    r, g, b, a = im.split()
    a = a.point(lambda v: 255 if v >= 128 else 0)  # strictly binary alpha
    Image.merge("RGBA", (r, g, b, a)).save("logo.png", optimize=True)
    print("logo.svg + logo.png written")
