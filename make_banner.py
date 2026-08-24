"""
FG Admin Login Customizer banner (1200x525, JED format), matching the
FG Email Remover banner layout: coral "FG" + white title, italic
subtitle, coral rule, four bullet points, mark with drop shadow and a
"System plugin" caption. All text is baked to vector outlines.
"""

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg

FONT_DIR = '/mnt/skills/examples/canvas-design/canvas-fonts'
BOLD = f'{FONT_DIR}/InstrumentSans-Bold.ttf'
REGULAR = f'{FONT_DIR}/InstrumentSans-Regular.ttf'
ITALIC = f'{FONT_DIR}/InstrumentSans-Italic.ttf'

_cache = {}


def _font(path):
    if path not in _cache:
        f = TTFont(path)
        _cache[path] = (f, f.getGlyphSet(), f['head'].unitsPerEm, f.getBestCmap())
    return _cache[path]


def text_path(string, font_path, size, x, y, letter_spacing=0.0):
    font, glyphs, upem, cmap = _font(font_path)
    scale = size / upem
    parts = []
    cursor = 0.0
    for ch in string:
        name = cmap.get(ord(ch))
        if name is None:
            cursor += size * 0.32
            continue
        glyph = glyphs[name]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        d = pen.getCommands()
        if d:
            tx = x + cursor
            parts.append(
                f'<path d="{d}" transform="translate({tx:.2f} {y:.2f}) '
                f'scale({scale:.5f} {-scale:.5f})"/>'
            )
        cursor += glyph.width * scale + letter_spacing
    return ''.join(parts), cursor


def text_width(string, font_path, size, letter_spacing=0.0):
    _, glyphs, upem, cmap = _font(font_path)
    scale = size / upem
    total = 0.0
    for ch in string:
        name = cmap.get(ord(ch))
        total += (glyphs[name].width * scale) if name else size * 0.32
        total += letter_spacing
    return total


W, H = 1200, 525

BG_TOP = '#0C2E4F'
BG_BOTTOM = '#1C5687'
CORAL = '#FF6B4A'
WHITE = '#FFFFFF'
MUTED = '#B9CFE4'
FIELD = '#DCE4EF'
BUTTON = '#164A78'

TX = 465

title_size = 44
fg_d, fg_w = text_path('FG', BOLD, title_size, TX, 80)
title_d, title_w = text_path(' Admin Login Customizer', BOLD, title_size, TX + fg_w, 80)

sub_size = 22
sub_d, sub_w = text_path(
    'Give the login screen your own identity, not Joomla\u2019s.',
    ITALIC, sub_size, TX, 122
)

rule_w = max(fg_w + title_w, sub_w)
rule_y = 144

bullets = [
    ('Full visual control', 'logo, background, colours, card shadow, six presets'),
    ('Text always readable', 'automatic WCAG contrast whenever you set a background'),
    ('Portable settings', 'export or import a look as JSON to reuse it across sites'),
    ('Joomla 5 & 6 native', 'PSR-4, DI container, a single self-hosted update channel'),
]

heading_size = 22
desc_size = 17
bullet_y0 = 198
bullet_step = 62

bullets_svg = []
for i, (head, desc) in enumerate(bullets):
    y = bullet_y0 + i * bullet_step
    head_d, _ = text_path(head, BOLD, heading_size, TX + 21, y)
    desc_d, _ = text_path(desc, REGULAR, desc_size, TX + 21, y + 27)
    bullets_svg.append(
        f'<circle cx="{TX + 5}" cy="{y - 7}" r="5" fill="{CORAL}"/>'
        f'<g fill="{WHITE}">{head_d}</g>'
        f'<g fill="{MUTED}">{desc_d}</g>'
    )
bullets_svg = '\n'.join(bullets_svg)

MARK_SIZE = 290
MARK_X, MARK_Y = 70, 82
s = MARK_SIZE / 512.0


def m(v):
    return v * s


mark = f'''
  <g filter="url(#markBlur)" opacity="0.4">
    <rect x="{MARK_X}" y="{MARK_Y + 14}" width="{MARK_SIZE}" height="{MARK_SIZE}"
          rx="{m(96):.1f}" ry="{m(96):.1f}" fill="#000000"/>
  </g>
  <g transform="translate({MARK_X} {MARK_Y})">
    <rect x="{m(10):.1f}" y="{m(10):.1f}" width="{m(492):.1f}" height="{m(492):.1f}"
          rx="{m(96):.1f}" ry="{m(96):.1f}" fill="url(#markBlue)"/>
    <rect x="{m(116):.1f}" y="{m(106):.1f}" width="{m(280):.1f}" height="{m(292):.1f}"
          rx="{m(30):.1f}" ry="{m(30):.1f}" fill="{WHITE}"/>
    <circle cx="{m(256):.1f}" cy="{m(168):.1f}" r="{m(34):.1f}" fill="{CORAL}"/>
    <rect x="{m(150):.1f}" y="{m(228):.1f}" width="{m(212):.1f}" height="{m(26):.1f}"
          rx="{m(13):.1f}" ry="{m(13):.1f}" fill="{FIELD}"/>
    <rect x="{m(150):.1f}" y="{m(272):.1f}" width="{m(212):.1f}" height="{m(26):.1f}"
          rx="{m(13):.1f}" ry="{m(13):.1f}" fill="{FIELD}"/>
    <rect x="{m(150):.1f}" y="{m(326):.1f}" width="{m(212):.1f}" height="{m(42):.1f}"
          rx="{m(21):.1f}" ry="{m(21):.1f}" fill="{BUTTON}"/>
  </g>
'''

caption_size = 20
caption_text = 'System plugin'
caption_w = text_width(caption_text, BOLD, caption_size, 0.4)
caption_d, _ = text_path(
    caption_text, BOLD, caption_size,
    MARK_X + MARK_SIZE / 2 - caption_w / 2, MARK_Y + MARK_SIZE + 36,
    letter_spacing=0.4
)

blobs = f'''
  <circle cx="1120" cy="60" r="180" fill="#FFFFFF" opacity="0.035"/>
  <circle cx="1180" cy="260" r="130" fill="#FFFFFF" opacity="0.045"/>
  <circle cx="60" cy="470" r="150" fill="#000000" opacity="0.08"/>
  <circle cx="980" cy="470" r="220" fill="#FFFFFF" opacity="0.03"/>
'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
    <linearGradient id="markBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#17456F"/>
      <stop offset="1" stop-color="#2A6BA3"/>
    </linearGradient>
    <filter id="markBlur" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    {blobs}

{mark}
    <g fill="{WHITE}">{caption_d}</g>

    <g fill="{CORAL}">{fg_d}</g>
    <g fill="{WHITE}">{title_d}</g>
    <g fill="{MUTED}" font-style="italic">{sub_d}</g>
    <rect x="{TX}" y="{rule_y}" width="{rule_w:.1f}" height="2" fill="{CORAL}" opacity="0.6"/>

{bullets_svg}
  </g>
</svg>
'''

with open('banner.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

# ------------------------------------------------------------------
# PNG rendering: cairosvg's feGaussianBlur support is unreliable (it
# rendered the shadow as hard-edged flat shapes instead of a soft
# blur in testing). The .svg file above keeps the native filter for
# browsers/vector viewers, which render it correctly. For the PNG we
# rasterize WITHOUT the shadow group and composite a properly
# PIL-blurred shadow underneath the mark ourselves - guaranteed
# correct regardless of the SVG renderer's filter fidelity.
# ------------------------------------------------------------------
mark_no_shadow = mark.split("<g transform=", 1)
mark_no_shadow = "<g transform=" + mark_no_shadow[1]  # drop the shadow <g filter=...> block


from PIL import Image, ImageFilter

# Standalone shadow shape (solid, no blur) on a transparent canvas.
shadow_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect x="{MARK_X}" y="{MARK_Y + 14}" width="{MARK_SIZE}" height="{MARK_SIZE}"
        rx="{m(96):.1f}" ry="{m(96):.1f}" fill="#000000"/>
</svg>
'''
cairosvg.svg2png(bytestring=shadow_svg.encode('utf-8'), write_to='_shadow_solid.png',
                 output_width=W, output_height=H)

shadow = Image.open('_shadow_solid.png').convert('RGBA')

# Blur just the alpha channel, then scale it down to the target opacity.
r, g, b, a = shadow.split()
a = a.filter(ImageFilter.GaussianBlur(radius=20))
a = a.point(lambda v: int(v * 0.40))
shadow = Image.merge('RGBA', (r, g, b, a))

# Content layer (mark + all text) on a FULLY TRANSPARENT background - no
# background rect, no blobs - so it only ever covers its own opaque
# pixels and never blots out the shadow layer beneath it.
content_only_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="markBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#17456F"/>
      <stop offset="1" stop-color="#2A6BA3"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
{mark_no_shadow}
    <g fill="{WHITE}">{caption_d}</g>

    <g fill="{CORAL}">{fg_d}</g>
    <g fill="{WHITE}">{title_d}</g>
    <g fill="{MUTED}" font-style="italic">{sub_d}</g>
    <rect x="{TX}" y="{rule_y}" width="{rule_w:.1f}" height="2" fill="{CORAL}" opacity="0.6"/>

{bullets_svg}
  </g>
</svg>
'''
cairosvg.svg2png(bytestring=content_only_svg.encode('utf-8'), write_to='_content.png',
                 output_width=W, output_height=H)
content = Image.open('_content.png').convert('RGBA')

# Background + blobs only (no mark, no text) to composite under the shadow.
bg_only_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {blobs}
</svg>
'''
cairosvg.svg2png(bytestring=bg_only_svg.encode('utf-8'), write_to='_bgonly.png',
                 output_width=W, output_height=H)
bg_only = Image.open('_bgonly.png').convert('RGBA')

# Layer order: opaque background -> soft blurred shadow -> mark/text on top.
layered = Image.alpha_composite(bg_only, shadow)
layered = Image.alpha_composite(layered, content)
layered.convert('RGB').save('banner.png')

for tmp in ('_shadow_solid.png', '_content.png', '_bgonly.png'):
    import os
    os.remove(tmp)

print('banner.svg + banner.png OK (PIL-composited shadow)')
