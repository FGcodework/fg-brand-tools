"""
FG Editor Switcher banner (1200x525, JED format), matching the established
FG banner layout: coral "FG" + white title, italic subtitle, coral rule,
four bullet points, mark with drop shadow and an "Editor plugin" caption.
All text is baked to vector outlines.

Mark: a browser-window card (matching assets/logo.png's own icon) with a
coral "swap" badge (two opposing thick arrows) over its bottom-right corner,
echoing the plugin's actual function - swapping which editor is shown.
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

BG_TOP = '#081D32'
BG_BOTTOM = '#113758'
CORAL = '#FF6B4A'
WHITE = '#FFFFFF'
MUTED = '#B9CFE4'
HEADER = '#DCE4EF'
LINE = '#C7D3E0'
DOT = '#0B263F'

TX = 465

title_size = 44
# Vertical centering: with the original y-values, the text block (title
# through last bullet) spanned roughly y=48..415 in the 525-tall canvas -
# 48px top margin vs. 110px bottom margin, visibly off-center high. Shifting
# every y-coordinate down by this amount balances the margins.
Y_SHIFT = 31
fg_d, fg_w = text_path('FG', BOLD, title_size, TX, 80 + Y_SHIFT)
title_d, title_w = text_path(' Editor Switcher', BOLD, title_size, TX + fg_w, 80 + Y_SHIFT)

sub_size = 22
sub_d, sub_w = text_path(
    'Switch WYSIWYG editors on the fly \u2014 without losing what you typed.',
    ITALIC, sub_size, TX, 122 + Y_SHIFT
)

rule_w = max(fg_w + title_w, sub_w)
rule_y = 144 + Y_SHIFT

bullets = [
    ('Any editor, any time', 'TinyMCE, CodeMirror, JCE and more - pick per session'),
    ('Content never lost', 'unsaved changes carry over automatically when you switch'),
    ('Works everywhere', 'subform rows, AJAX-loaded forms, front-end and back-end'),
    ('Joomla 4, 5 & 6 native', 'PSR-4, DI container, a self-hosted update channel'),
]

heading_size = 22
desc_size = 17
bullet_y0 = 198 + Y_SHIFT
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
MARK_SHIFT = 18  # mark+caption block needs a smaller shift than the text block (different height)
MARK_X, MARK_Y = 70, 82 + MARK_SHIFT
s = MARK_SIZE / 512.0


def m(v):
    return v * s


# Browser-window card (matches assets/logo.png): header bar with three
# dots, body with three text-line bars, all within the navy squircle tile.
WIN_X, WIN_Y, WIN_W, WIN_H = 90, 88, 298, 248
HEAD_H = 52

window = f'''
    <rect x="{m(WIN_X):.1f}" y="{m(WIN_Y):.1f}" width="{m(WIN_W):.1f}" height="{m(WIN_H):.1f}"
          rx="{m(26):.1f}" ry="{m(26):.1f}" fill="{HEADER}"/>
    <rect x="{m(WIN_X):.1f}" y="{m(WIN_Y + HEAD_H):.1f}" width="{m(WIN_W):.1f}" height="{m(WIN_H - HEAD_H):.1f}"
          rx="{m(10):.1f}" ry="{m(10):.1f}" fill="{WHITE}"/>
    <rect x="{m(WIN_X + 22):.1f}" y="{m(WIN_Y + 16):.1f}" width="{m(20):.1f}" height="{m(20):.1f}"
          rx="{m(6):.1f}" ry="{m(6):.1f}" fill="{DOT}"/>
    <rect x="{m(WIN_X + 58):.1f}" y="{m(WIN_Y + 16):.1f}" width="{m(20):.1f}" height="{m(20):.1f}"
          rx="{m(6):.1f}" ry="{m(6):.1f}" fill="{DOT}"/>
    <rect x="{m(WIN_X + 94):.1f}" y="{m(WIN_Y + 16):.1f}" width="{m(20):.1f}" height="{m(20):.1f}"
          rx="{m(6):.1f}" ry="{m(6):.1f}" fill="{DOT}"/>
    <rect x="{m(WIN_X + 22):.1f}" y="{m(WIN_Y + 90):.1f}" width="{m(200):.1f}" height="{m(18):.1f}"
          rx="{m(9):.1f}" ry="{m(9):.1f}" fill="{LINE}"/>
    <rect x="{m(WIN_X + 22):.1f}" y="{m(WIN_Y + 126):.1f}" width="{m(170):.1f}" height="{m(18):.1f}"
          rx="{m(9):.1f}" ry="{m(9):.1f}" fill="{LINE}"/>
    <rect x="{m(WIN_X + 22):.1f}" y="{m(WIN_Y + 162):.1f}" width="{m(130):.1f}" height="{m(18):.1f}"
          rx="{m(9):.1f}" ry="{m(9):.1f}" fill="{LINE}"/>
'''

# Coral "swap" badge over the window's bottom-right corner: two opposing
# thick arrows (echoes the plugin switching between editors).
BADGE_CX, BADGE_CY, BADGE_R = 378, 330, 90
ARROW_D = 'M -35,-9 L 15,-9 L 15,-20 L 35,0 L 15,20 L 15,9 L -35,9 Z'

badge = f'''
    <circle cx="{m(BADGE_CX):.1f}" cy="{m(BADGE_CY):.1f}" r="{m(BADGE_R):.1f}" fill="{CORAL}"/>
    <g fill="{WHITE}">
      <path d="{ARROW_D}" transform="translate({m(BADGE_CX - 8):.1f} {m(BADGE_CY - 22):.1f}) scale({s:.5f})"/>
      <path d="{ARROW_D}" transform="translate({m(BADGE_CX + 8):.1f} {m(BADGE_CY + 22):.1f}) scale({-s:.5f} {-s:.5f})"/>
    </g>
'''

mark = f'''
  <g filter="url(#markBlur)" opacity="0.4">
    <rect x="{MARK_X}" y="{MARK_Y + 14}" width="{MARK_SIZE}" height="{MARK_SIZE}"
          rx="{m(96):.1f}" ry="{m(96):.1f}" fill="#000000"/>
  </g>
  <g transform="translate({MARK_X} {MARK_Y})">
    <rect x="{m(10):.1f}" y="{m(10):.1f}" width="{m(492):.1f}" height="{m(492):.1f}"
          rx="{m(96):.1f}" ry="{m(96):.1f}" fill="url(#markBlue)"/>
{window}
{badge}
  </g>
'''

caption_size = 20
caption_text = 'Editor plugin'
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
    <linearGradient id="markBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOTTOM}"/>
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
    <linearGradient id="markBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOTTOM}"/>
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
