"""Render all profile lettering as portable Oxanium SVG paths."""
from functools import lru_cache
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=1)
def font_data():
    return json.loads((ROOT / 'assets/typography/oxanium/glyphs.json').read_text(encoding='utf-8'))


def variant(weight):
    weight = int(weight)
    return font_data()['weights']['800' if weight >= 700 else '600' if weight >= 500 else '400']


def lettering(value, x, baseline, size, color, weight=400, tracking=0, anchor='start', extra=''):
    value = str(value)
    data = variant(weight)
    scale = size / data['units_per_em']
    advance = 0
    paths = []
    for char in value:
        glyph = data['glyphs'].get(char, data['glyphs']['?'])
        if glyph['path']:
            paths.append(f'<path transform="translate({advance:.3f} 0)" d="{glyph["path"]}"/>')
        advance += glyph['advance'] + tracking / scale
    width = max(0, advance * scale - tracking)
    if anchor == 'middle':
        x -= width / 2
    elif anchor == 'end':
        x -= width
    # The outer wrapper keeps optional entrance motion separate from glyph geometry.
    markup = f'<g aria-label="{escape(value, quote=True)}" {extra}><g fill="{color}" transform="translate({x:.3f} {baseline}) scale({scale:.5f} {-scale:.5f})">' + ''.join(paths) + '</g></g>'
    return markup, width


def svg_text(value, x, y, size=18, color='#edf4ff', weight=400, extra=''):
    anchor_match = re.search(r'text-anchor="([^"]+)"', extra)
    spacing_match = re.search(r'letter-spacing="([^"]+)"', extra)
    anchor = anchor_match.group(1) if anchor_match else 'start'
    tracking = float(spacing_match.group(1)) if spacing_match else 0
    if str(value) == '↗':
        return f'<g aria-label="Abrir repositorios" transform="translate({x} {y-size})" fill="none" stroke="{color}" stroke-width="1.8"><path d="M3 18L18 3M8 3H18V13"/></g>'
    return lettering(value, x, y, size, color, weight, tracking, anchor, extra)[0]
