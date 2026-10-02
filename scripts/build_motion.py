"""Build matte icons and a self-contained animated spiral galaxy."""
from pathlib import Path
import math
import random
import re

ROOT = Path(__file__).resolve().parents[1]


def dot(x, y, radius, color, opacity=1):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{color}" opacity="{opacity:.2f}"/>'


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
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
<title id="title">Anthony Alex · Desarrollo web y datos</title>
<desc id="desc">Galaxia espiral de partículas con cuatro brazos en rotación, sobre un fondo oscuro mate.</desc>
<defs><clipPath id="frame"><rect x="1" y="1" width="1198" height="358" rx="18"/></clipPath></defs>
<style>
text{font-family:Arial,Helvetica,sans-serif}
.galaxy{transform-origin:0 0;animation:turn 52s linear infinite}
.outer-dust{transform-origin:0 0;animation:turn 88s linear infinite}
.scene{animation:drift 14s ease-in-out infinite}
@keyframes turn{to{transform:rotate(360deg)}}
@keyframes drift{0%,100%{transform:translateY(3px)}50%{transform:translateY(-3px)}}
@media(prefers-reduced-motion:reduce){.galaxy,.outer-dust,.scene{animation:none}}
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
<text x="46" y="100" font-size="13" letter-spacing="3" fill="#8999aa">ANTHONYLWZ</text>
<text x="42" y="177" font-size="68" font-weight="700" letter-spacing="-2" fill="#eff3f8">Anthony Alex</text>
<text x="46" y="224" font-size="22" fill="#a9b8c9">Desarrollo web · Datos</text>
<path d="M46 254H164" stroke="#59657a" stroke-width="1"/>
</svg>'''


ICONS = [
    ('html5', 'HTML5', 'float'),
    ('css3', 'CSS3', 'tilt'),
    ('javascript', 'JavaScript', 'breathe'),
    ('react', 'React', 'spin'),
    ('vitejs', 'Vite', 'lift'),
    ('tailwindcss', 'Tailwind CSS', 'drift'),
    ('framermotion', 'Motion / Framer Motion', 'lift'),
    ('php', 'PHP', 'breathe'),
    ('mysql', 'MySQL', 'drift'),
    ('firebase', 'Firebase Cloud Messaging', 'lift'),
    ('python', 'Python', 'tilt'),
    ('pandas', 'pandas', 'float'),
    ('jupyter', 'Notebooks Jupyter (.ipynb)', 'spin'),
    ('git', 'Git', 'tilt'),
    ('github', 'GitHub', 'float'),
]


def icon_svg(name, label, motion, index):
    original = (ROOT / 'assets/icons' / f'{name}-original.svg').read_text(encoding='utf-8').strip()
    original = re.sub(r'<svg\b', '<svg x="16" y="16" width="48" height="48"', original, count=1)
    display = (ROOT / 'assets/icons' / f'{name}.svg').read_text(encoding='utf-8')
    bg = re.search(r'<rect[^>]*fill="([^"]+)"', display).group(1)
    delay = -index * .47
    duration = 5.6 + (index % 4) * .6
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80" role="img" aria-labelledby="title">
<title id="title">{label}</title>
<style>
.tile{{animation:float {duration}s ease-in-out {delay}s infinite}}
.logo{{transform-origin:40px 40px;animation:{motion} {18 if motion == 'spin' else duration}s {'linear' if motion == 'spin' else 'ease-in-out'} {delay}s infinite}}
@keyframes float{{0%,100%{{transform:translateY(2px)}}50%{{transform:translateY(-2px)}}}}
@keyframes tilt{{0%,100%{{transform:rotate(-7deg)}}50%{{transform:rotate(7deg)}}}}
@keyframes breathe{{0%,100%{{transform:scale(.93)}}50%{{transform:scale(1.04)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes lift{{0%,100%{{transform:translateY(3px) scale(.96)}}50%{{transform:translateY(-4px) scale(1.04)}}}}
@keyframes drift{{0%,100%{{transform:translateX(-3px) rotate(-3deg)}}50%{{transform:translateX(3px) rotate(3deg)}}}}
@media(prefers-reduced-motion:reduce){{.tile,.logo{{animation:none}}}}
</style>
<g class="tile">
<rect x="5" y="5" width="70" height="70" rx="17" fill="{bg}" stroke="#748091" stroke-opacity=".18"/>
<g class="logo">{original}</g>
</g>
</svg>'''


if __name__ == '__main__':
    (ROOT / 'assets/header-motion.svg').write_text(galaxy_header(), encoding='utf-8')
    for index, spec in enumerate(ICONS):
        (ROOT / 'assets/icons/motion' / f'{spec[0]}.svg').write_text(icon_svg(*spec, index), encoding='utf-8')
    print('Built the spiral galaxy and 15 matte animated icons.')
