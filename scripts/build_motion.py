"""Build the profile's self-contained SVG motion assets (standard library only)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

HEADER = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="230" viewBox="0 0 1200 230" role="img" aria-labelledby="title desc">
<title id="title">Anthony Alex · Desarrollo web y datos</title>
<desc id="desc">Órbitas de luz, un símbolo de código flotante y ondas suaves en movimiento.</desc>
<defs>
  <linearGradient id="surface" x2="1" y2="1"><stop stop-color="#101720"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
  <linearGradient id="accent"><stop stop-color="#70cee8"/><stop offset=".55" stop-color="#8da9f6"/><stop offset="1" stop-color="#b8a1e4"/></linearGradient>
  <linearGradient id="fade"><stop stop-color="#72cde7" stop-opacity="0"/><stop offset=".5" stop-color="#72cde7" stop-opacity=".65"/><stop offset="1" stop-color="#a6a4ed" stop-opacity="0"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#779fd1" stop-opacity=".16"/><stop offset="1" stop-color="#779fd1" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect x="1" y="1" width="1198" height="228" rx="18"/></clipPath>
</defs>
<style>
text{font-family:Arial,Helvetica,sans-serif}
.aura{transform-origin:940px 115px;animation:aura 9s ease-in-out infinite}
.wave{animation:wave 11s ease-in-out infinite}.wave.second{animation-delay:-5.5s}
.trail{stroke-dasharray:45 1255;animation:travel 12s linear infinite}
.trail.second{animation-delay:-6s;animation-duration:16s}
.outer{transform-origin:950px 115px;animation:orbit 24s linear infinite}
.inner{transform-origin:950px 115px;animation:orbit 17s linear infinite reverse}
.orbit-dot{transform-origin:950px 115px;animation:orbit 11s linear infinite}
.orbit-dot.second{animation-duration:19s;animation-direction:reverse}
.core{animation:float 5.5s ease-in-out infinite}
.code{stroke-dasharray:110;animation:draw 7s ease-in-out infinite}
.slash{animation:slash 5.5s ease-in-out infinite;transform-origin:950px 115px}
.cursor{animation:blink 1.2s steps(2,end) infinite}
.underline{stroke-dasharray:100 440;animation:underline 8s ease-in-out infinite}
.spark{animation:spark 4s ease-in-out infinite}.s2{animation-delay:-1.4s}.s3{animation-delay:-2.8s}
@keyframes aura{0%,100%{transform:scale(.9);opacity:.7}50%{transform:scale(1.2);opacity:1}}
@keyframes wave{0%,100%{transform:translateY(5px);opacity:.25}50%{transform:translateY(-12px);opacity:.55}}
@keyframes travel{to{stroke-dashoffset:-1300}}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes float{0%,100%{transform:translateY(5px)}50%{transform:translateY(-6px)}}
@keyframes draw{0%,100%{stroke-dashoffset:0;opacity:1}45%{stroke-dashoffset:8;opacity:.65}60%{stroke-dashoffset:0;opacity:1}}
@keyframes slash{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
@keyframes blink{50%{opacity:.15}}
@keyframes underline{0%,100%{stroke-dashoffset:440;opacity:.35}50%{stroke-dashoffset:0;opacity:.85}}
@keyframes spark{0%,100%{opacity:.25}50%{opacity:.9}}
@media(prefers-reduced-motion:reduce){.aura,.wave,.trail,.outer,.inner,.orbit-dot,.core,.code,.slash,.cursor,.underline,.spark{animation:none}.trail,.underline{stroke-dasharray:none;opacity:.3}}
</style>
<rect x="1" y="1" width="1198" height="228" rx="18" fill="url(#surface)" stroke="#303946"/>
<g clip-path="url(#card)">
  <ellipse class="aura" cx="940" cy="115" rx="270" ry="190" fill="url(#glow)"/>
  <g fill="none" stroke="url(#fade)" stroke-width="1">
    <path class="wave" d="M520 210C700 140 766 252 940 186S1140 145 1260 178"/>
    <path class="wave second" d="M550 214C731 175 829 245 995 189S1165 181 1260 201"/>
    <path class="trail" d="M520 210C700 140 766 252 940 186S1140 145 1260 178" stroke-width="2"/>
    <path class="trail second" d="M550 214C731 175 829 245 995 189S1165 181 1260 201" stroke-width="2"/>
  </g>
  <g fill="none" stroke="#819bb4" stroke-width="1" opacity=".25">
    <path d="M694 47H713M703.5 37.5V56.5M1147 157H1164M1155.5 148.5V165.5"/>
    <path d="M739 183h11m-5.5-5.5v11M1085 44h11m-5.5-5.5v11"/>
  </g>
  <g fill="#a9cbd9"><circle class="spark" cx="726" cy="92" r="1.7"/><circle class="spark s2" cx="1125" cy="77" r="1.7"/><circle class="spark s3" cx="1101" cy="192" r="1.7"/></g>
  <g class="outer" fill="none" stroke="url(#accent)">
    <circle cx="950" cy="115" r="92" stroke-opacity=".12"/>
    <circle cx="950" cy="115" r="92" stroke-width="1.8" stroke-dasharray="120 458" stroke-linecap="round" stroke-opacity=".65"/>
    <circle cx="950" cy="115" r="92" stroke-width="1" stroke-dasharray="2 22" stroke-opacity=".3"/>
  </g>
  <g class="inner" fill="none" stroke="url(#accent)">
    <ellipse cx="950" cy="115" rx="117" ry="47" transform="rotate(-28 950 115)" stroke-opacity=".25"/>
    <ellipse cx="950" cy="115" rx="117" ry="47" transform="rotate(-28 950 115)" stroke-width="2" stroke-dasharray="48 489" stroke-linecap="round" stroke-opacity=".7"/>
  </g>
  <g class="orbit-dot"><circle cx="1042" cy="115" r="6" fill="#80d4eb" opacity=".15"/><circle cx="1042" cy="115" r="2.6" fill="#96ddec"/></g>
  <g class="orbit-dot second"><circle cx="950" cy="23" r="4.5" fill="#b2a2ec" opacity=".18"/><circle cx="950" cy="23" r="2" fill="#b2a2ec"/></g>
  <g class="core">
    <rect x="900" y="65" width="100" height="100" rx="24" fill="#131c28" stroke="#65839e" stroke-opacity=".45"/>
    <rect x="906" y="71" width="88" height="88" rx="19" fill="none" stroke="#738da8" stroke-opacity=".1"/>
    <g fill="none" stroke="url(#accent)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <path class="code" d="M930 99L915 115L930 131M970 99L985 115L970 131"/>
      <path class="slash" d="M958 94L942 136"/>
    </g>
  </g>
  <path d="M1 229H1199" stroke="url(#fade)" stroke-opacity=".45"/>
</g>
<text x="43" y="57" font-size="13" letter-spacing="3" fill="#8999aa">ANTHONYLWZ</text>
<text x="40" y="133" font-size="66" font-weight="700" letter-spacing="-2" fill="#eff3f8">Anthony Alex<tspan class="cursor" fill="#86c9df">_</tspan></text>
<text x="44" y="180" font-size="22" fill="#a9b8c9">Desarrollo web · Datos</text>
<path class="underline" d="M44 200H570" fill="none" stroke="url(#accent)" stroke-width="1.4" stroke-linecap="round"/>
</svg>'''

ICONS = [
    ('html5', 'HTML5', '#ef896c', 'float'),
    ('css3', 'CSS3', '#70b8e7', 'tilt'),
    ('javascript', 'JavaScript', '#e6d779', 'breathe'),
    ('react', 'React', '#79d5ec', 'spin'),
    ('vitejs', 'Vite', '#b69be4', 'lift'),
    ('tailwindcss', 'Tailwind CSS', '#6dc9dd', 'drift'),
    ('framermotion', 'Motion / Framer Motion', '#929ce6', 'lift'),
    ('php', 'PHP', '#a7a9d6', 'breathe'),
    ('mysql', 'MySQL', '#72bad7', 'drift'),
    ('firebase', 'Firebase Cloud Messaging', '#efbe68', 'lift'),
    ('python', 'Python', '#8cbcd9', 'tilt'),
    ('pandas', 'pandas', '#a498d4', 'float'),
    ('jupyter', 'Notebooks Jupyter (.ipynb)', '#eaaa79', 'spin'),
    ('git', 'Git', '#e99983', 'tilt'),
    ('github', 'GitHub', '#afc0d1', 'float'),
]


def icon_svg(name, label, accent, motion, index):
    original = (ROOT / 'assets/icons' / f'{name}-original.svg').read_text(encoding='utf-8').strip()
    original = re.sub(r'<svg\b', '<svg x="16" y="16" width="48" height="48"', original, count=1)
    display = (ROOT / 'assets/icons' / f'{name}.svg').read_text(encoding='utf-8')
    bg = re.search(r'<rect[^>]*fill="([^"]+)"', display).group(1)
    delay = -index * .47
    duration = 5.6 + (index % 4) * .6
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80" role="img" aria-labelledby="title">
<title id="title">{label}</title>
<defs>
<linearGradient id="glass" x2="0" y2="1"><stop stop-color="#ffffff" stop-opacity=".06"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<linearGradient id="shine"><stop stop-color="#ffffff" stop-opacity="0"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".09"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<clipPath id="clip"><rect x="5" y="5" width="70" height="70" rx="17"/></clipPath>
</defs>
<style>
.tile{{animation:float {duration}s ease-in-out {delay}s infinite}}
.logo{{transform-origin:40px 40px;animation:{motion} {18 if motion == 'spin' else duration}s {'linear' if motion == 'spin' else 'ease-in-out'} {delay}s infinite}}
.edge{{stroke-dasharray:34 228;animation:edge {8 + index % 3}s linear {delay}s infinite}}
.sheen{{animation:shine {7.5 + index % 3}s ease-in-out {delay}s infinite}}
.status{{animation:pulse 3.5s ease-in-out {delay}s infinite}}
@keyframes float{{0%,100%{{transform:translateY(2px)}}50%{{transform:translateY(-2px)}}}}
@keyframes tilt{{0%,100%{{transform:rotate(-7deg)}}50%{{transform:rotate(7deg)}}}}
@keyframes breathe{{0%,100%{{transform:scale(.93)}}50%{{transform:scale(1.04)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes lift{{0%,100%{{transform:translateY(3px) scale(.96)}}50%{{transform:translateY(-4px) scale(1.04)}}}}
@keyframes drift{{0%,100%{{transform:translateX(-3px) rotate(-3deg)}}50%{{transform:translateX(3px) rotate(3deg)}}}}
@keyframes edge{{to{{stroke-dashoffset:-262}}}}
@keyframes shine{{0%,15%{{transform:translateX(-90px)}}65%,100%{{transform:translateX(100px)}}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:.9}}}}
@media(prefers-reduced-motion:reduce){{.tile,.logo,.edge,.sheen,.status{{animation:none}}.sheen{{display:none}}.edge{{stroke-dasharray:none;opacity:.35}}}}
</style>
<g class="tile">
<rect x="5" y="5" width="70" height="70" rx="17" fill="{bg}"/>
<rect x="5" y="5" width="70" height="70" rx="17" fill="url(#glass)" stroke="{accent}" stroke-opacity=".18"/>
<rect class="edge" x="5" y="5" width="70" height="70" rx="17" fill="none" stroke="{accent}" stroke-width="1.3" stroke-linecap="round" opacity=".8"/>
<g class="logo">{original}</g>
<g clip-path="url(#clip)"><path class="sheen" d="M-28 3H-2L32 77H6Z" fill="url(#shine)"/></g>
<circle class="status" cx="64" cy="64" r="1.8" fill="{accent}"/>
</g>
</svg>'''


if __name__ == '__main__':
    (ROOT / 'assets/header-motion.svg').write_text(HEADER, encoding='utf-8')
    for index, spec in enumerate(ICONS):
        (ROOT / 'assets/icons/motion' / f'{spec[0]}.svg').write_text(icon_svg(*spec, index), encoding='utf-8')
    print('Built header and 15 animated technology icons.')
