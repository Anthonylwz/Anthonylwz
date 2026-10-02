"""Build the Oxanium profile, static technology icons and spiral galaxy."""
from pathlib import Path
import math
import json
import random
import re

ROOT = Path(__file__).resolve().parents[1]


def dot(x, y, radius, color, opacity=1):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{color}" opacity="{opacity:.2f}"/>'




from profile_typography import lettering, variant


def animated_name():
    words = [('ANTHONY', 42, 152, 104, '#eff3f8'), ('ALEX', 42, 247, 104, '#bfb3e3')]
    markup, rules, events = [], [], []
    count = 0
    first_end = 42
    for row, (word, x, baseline, size, color) in enumerate(words):
        _, width = lettering(word, x, baseline, size, color, 800, 1)
        size = min(size, size * 552 / width)
        scale = size / variant(800)['units_per_em']
        for char in word:
            glyph = variant(800)['glyphs'][char]
            advance = glyph['advance'] * scale + 1
            on = 6 + count * 2 + (4 if row else 0)
            off = 88 + (10 - count) * .95
            cls = f'typed-{count}'
            letter, _ = lettering(char, x, baseline, size, color, 800, extra=f'class="typed-letter {cls}"')
            markup.append(letter)
            rules.append(f'.{cls}{{animation:{cls} 14s steps(1,end) infinite}}')
            rules.append(f'@keyframes {cls}{{0%,{on-.01:.2f}%{{opacity:0}}{on:.2f}%,{off-.01:.2f}%{{opacity:1}}{off:.2f}%,100%{{opacity:0}}}}')
            cursor_y = baseline - 78
            events.append((on, x + advance, cursor_y))
            events.append((off, x, cursor_y))
            x += advance
            count += 1
        if row == 0:
            first_end = x
    events += [(0, 42, 74), (22, 42, 169), (91.3, first_end, 74), (100, 42, 74)]
    frames = ''.join(f'{time:.2f}%{{transform:translate({x:.2f}px,{y:.2f}px)}}' for time, x, y in sorted(events))
    rules.append('.type-cursor{animation:cursor-position 14s steps(1,end) infinite, cursor-blink .9s steps(2,end) infinite}')
    rules.append('@keyframes cursor-position{' + frames + '}@keyframes cursor-blink{50%{opacity:.3}}')
    rules.append('@media(prefers-reduced-motion:reduce){.typed-letter{animation:none;opacity:1}.type-cursor{display:none}}')
    markup.append('<rect class="type-cursor" x="0" y="0" width="3" height="82" rx="1" fill="#aab5c9"/>')
    return '<g aria-label="Anthony Alex">' + ''.join(markup) + '</g>', ''.join(rules)


def galaxy_header():
    rng = random.Random(192707923)
    stars, arms, dust, bulge, lanes = [], [], [], [], []
    # Stationary, crisp stars. No bloom, glossy overlays or blinking.
    for _ in range(105):
        x, y = rng.uniform(620, 1190), rng.uniform(18, 342)
        stars.append(dot(x, y, rng.uniform(.55, 1.15), '#9eabc7', rng.uniform(.20, .52)))
    colors = ['#a8badc', '#899dc5', '#b1a3ce', '#d9d4e1', '#91b7cb']
    # Four coherent logarithmic-looking arms, with deterministic stellar scatter.
    for arm in range(4):
        points = []
        for j in range(100):
            t = j / 99
            r = 23 + 237 * t
            angle = arm * math.pi / 2 + 4.55 * (1 - t)
            points.append(f'{r * math.cos(angle):.2f},{r * math.sin(angle):.2f}')
        lanes.append('<polyline points="' + ' '.join(points) + '" fill="none" stroke="' + colors[arm] + '" stroke-width="7" opacity=".07"/>')
        for _ in range(510):
            t = rng.random() ** .78
            r = 23 + 237 * t
            angle = arm * math.pi / 2 + 4.55 * (1 - t)
            scatter = 2.6 + 7.5 * t
            x = r * math.cos(angle) + rng.gauss(0, scatter)
            y = r * math.sin(angle) + rng.gauss(0, scatter)
            arms.append(dot(x, y, rng.uniform(.6, 1.65) * (1.2 - .35 * t), rng.choice(colors), rng.uniform(.38, .92)))
    # Matte inter-arm dust makes the structure read as a disk at profile sizes.
    for _ in range(410):
        r = 265 * math.sqrt(rng.random())
        theta = rng.uniform(0, math.tau)
        dust.append(dot(r * math.cos(theta), r * math.sin(theta), rng.uniform(.45, .9), '#687591', rng.uniform(.12, .30)))
    for _ in range(260):
        x, y = rng.gauss(0, 19), rng.gauss(0, 19)
        bulge.append(dot(x, y, rng.uniform(.5, 1.3), rng.choice(['#e7dfd4', '#c8c4d8', '#c1b7c9']), rng.uniform(.35, .82)))
    name_svg, typing_css = animated_name()
    username_svg, _ = lettering('ANTHONYLWZ', 46, 51, 13, '#929bb2', 600, 2.5)
    description_svg, _ = lettering('Desarrollo web · Datos', 46, 292, 22, '#b0b7ca', 400)
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
<title id="title">Anthony Alex · Desarrollo web y datos</title>
<desc id="desc">Anthony Alex con tipografía Oxanium de gran formato, escritura letra por letra y una galaxia espiral animada.</desc>
<defs><clipPath id="frame"><rect x="1" y="1" width="1198" height="358" rx="18"/></clipPath></defs>
<style>
.galaxy{transform-origin:0 0;animation:turn 52s linear infinite}
.outer-dust{transform-origin:0 0;animation:turn 88s linear infinite}
.scene{animation:drift 14s ease-in-out infinite}
@keyframes turn{to{transform:rotate(360deg)}}
@keyframes drift{0%,100%{transform:translateY(3px)}50%{transform:translateY(-3px)}}
@media(prefers-reduced-motion:reduce){.galaxy,.outer-dust,.scene{animation:none}}
''' + typing_css + '''
</style>
<rect x="1" y="1" width="1198" height="358" rx="18" fill="#0c1018" stroke="#303946"/>
<g clip-path="url(#frame)">
''' + ''.join(stars) + '''
<g class="scene"><g transform="translate(925 180) rotate(-16) scale(1 .61)">
<g class="outer-dust">''' + ''.join(dust) + '''</g>
<g class="galaxy">''' + ''.join(lanes + arms + bulge) + '''</g>
<circle r="4.2" fill="#e9e3d9"/>
</g></g>
</g>
''' + username_svg + name_svg + description_svg + '''
<path d="M46 315H178" stroke="#59657a" stroke-width="1"/>
</svg>'''


ICONS = [
    ('html5', 'HTML5'),
    ('css3', 'CSS3'),
    ('javascript', 'JavaScript'),
    ('react', 'React'),
    ('vitejs', 'Vite'),
    ('tailwindcss', 'Tailwind CSS'),
    ('framermotion', 'Motion / Framer Motion'),
    ('php', 'PHP'),
    ('mysql', 'MySQL'),
    ('firebase', 'Firebase Cloud Messaging'),
    ('python', 'Python'),
    ('pandas', 'pandas'),
    ('jupyter', 'Notebooks Jupyter (.ipynb)'),
    ('git', 'Git'),
    ('github', 'GitHub'),
]


def icon_svg(name, label):
    original = (ROOT / 'assets/icons' / f'{name}-original.svg').read_text(encoding='utf-8').strip()
    original = re.sub(r'<svg\b', '<svg x="16" y="16" width="48" height="48"', original, count=1)
    for old_id in re.findall(r'id="([^"]+)"', original):
        new_id = name + '-' + old_id
        original = original.replace('id="' + old_id + '"', 'id="' + new_id + '"').replace('url(#' + old_id + ')', 'url(#' + new_id + ')').replace('href="#' + old_id + '"', 'href="#' + new_id + '"')
    display = (ROOT / 'assets/icons' / f'{name}.svg').read_text(encoding='utf-8')
    bg = re.search(r'<rect[^>]*fill="([^"]+)"', display).group(1)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80" role="img" aria-labelledby="title-{name}">
<title id="title-{name}">{label}</title>
<rect x="5" y="5" width="70" height="70" rx="17" fill="{bg}" stroke="#748091" stroke-opacity=".18"/>
{original}
</svg>'''


def stack_board():
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="374" viewBox="0 0 1200 374" role="img" aria-labelledby="title"><title id="title">Frontend, Backend, Python y notebooks, Versiones</title><rect x="1" y="1" width="1198" height="372" rx="18" fill="#10151e" stroke="#303946"/><path d="M24 184H1176M400 208V350M800 208V350" fill="none" stroke="#303946"/>'
    headings = [('FRONTEND', 600, 47), ('BACKEND', 200, 231), ('PYTHON Y NOTEBOOKS', 600, 231), ('VERSIONES', 1000, 231)]
    for label, x, y in headings:
        s += lettering(label, x, y, 30, '#c2c8df', 600, .7, 'middle')[0]
    positions = [(189 + i * 120, 67) for i in range(7)]
    positions += [(31 + i * 118, 253) for i in range(3)]
    positions += [(431 + i * 118, 253) for i in range(3)]
    positions += [(839 + i * 120, 253) for i in range(2)]
    for (name, label), (x, y) in zip(ICONS, positions):
        icon = icon_svg(name, label)
        body = icon[icon.index('>') + 1:icon.rfind('</svg>')]
        s += f'<svg x="{x}" y="{y}" width="102" height="102" viewBox="0 0 80 80" role="img" aria-labelledby="title-{name}">' + body + '</svg>'
    return s + '</svg>'


if __name__ == '__main__':
    (ROOT / 'assets/header-motion.svg').write_text(galaxy_header(), encoding='utf-8')
    (ROOT / 'assets/icons/static').mkdir(parents=True, exist_ok=True)
    for spec in ICONS:
        (ROOT / 'assets/icons/static' / f'{spec[0]}.svg').write_text(icon_svg(*spec), encoding='utf-8')
    (ROOT / 'assets/stack-display.svg').write_text(stack_board(), encoding='utf-8')
    print('Built Oxanium header, typography panel and 15 static icons.')
