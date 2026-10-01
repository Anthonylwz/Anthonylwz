"""Render public-only GitHub metrics without external packages or image services."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone, timedelta
from html import escape
import json
import os
from pathlib import Path
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'Anthonylwz'


def fetch_public_repositories():
    """Use the public user endpoint, then defensively exclude any private record."""
    repositories = []
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Anthonylwz-profile-metrics', 'X-GitHub-Api-Version': '2022-11-28'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    page = 1
    while True:
        url = f'https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}'
        batch = None
        for attempt in range(3):
            try:
                with urlopen(Request(url, headers=headers), timeout=30) as response:
                    batch = json.load(response)
                break
            except (HTTPError, URLError, TimeoutError):
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        if not isinstance(batch, list):
            raise ValueError('The public repositories endpoint returned unexpected data.')
        repositories.extend(r for r in batch if not r.get('private', True) and r.get('owner', {}).get('login', '').lower() == OWNER.lower())
        if len(batch) < 100:
            return repositories
        page += 1


def t(x, y, value, size=18, color='#edf4ff', weight='400', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def render_counts(repo_count, languages, updated):
    import math
    total = sum(languages.values())
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="216" viewBox="0 0 1200 216" role="img" aria-labelledby="title desc"><title id="title">Datos públicos de GitHub</title><desc id="desc">Repositorios propios y distribución del lenguaje principal por repositorio. No es una escala de dominio.</desc><style>text{font-family:Arial,Helvetica,sans-serif}.metric{animation:appear 1.2s ease-out both}.second{animation-delay:.18s}.slice{animation:appear 1.5s ease-out both}.halo{transform-origin:663px 107px;animation:orbit 12s linear infinite}@keyframes appear{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}@keyframes orbit{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.metric,.slice,.halo{animation:none}}</style><rect x="1" y="1" width="1198" height="214" rx="14" fill="#0d1117" stroke="#30363d"/>'
    s += t(30, 35, 'GITHUB / DATOS PÚBLICOS', 13, '#8b949e', extra='letter-spacing="2"')
    s += '<path d="M538 28V187" stroke="#30363d"/>'
    s += t(38, 123, repo_count, 53, '#edf1f5', '700', extra='class="metric"')
    s += t(269, 123, len(languages), 53, '#edf1f5', '700', extra='class="metric second"')
    s += t(40, 157, 'Repositorios propios', 16, '#8b949e')
    s += t(270, 157, 'Lenguajes principales', 16, '#8b949e')
    s += t(1128, 35, '↗', 27, '#a3b1bf')
    s += t(782, 58, 'Lenguaje principal · repositorios', 17, '#c9d1d9', '600')
    s += '<circle cx="663" cy="107" r="58" fill="none" stroke="#212830" stroke-width="16"/>'
    circumference = 2 * math.pi * 58
    offset = 0
    palette = ['#b4bfca', '#8799ab', '#576d83', '#354b63', '#9cadbc', '#63768a']
    for i, (name, count) in enumerate(languages.most_common()):
        color = palette[i % len(palette)]
        length = circumference * count / total if total else 0
        s += f'<circle class="slice" style="animation-delay:{i*.12:.2f}s" cx="663" cy="107" r="58" fill="none" stroke="{color}" stroke-width="16" stroke-dasharray="{length:.3f} {circumference-length:.3f}" stroke-dashoffset="{-offset:.3f}" transform="rotate(-90 663 107)"/>'
        offset += length
        yy = 90 + i * 25
        s += f'<circle cx="788" cy="{yy-5}" r="4" fill="{color}"/>'
        label = 'Notebooks' if name == 'Jupyter Notebook' else name
        s += t(805, yy, label, 16, '#aebbc8')
        s += t(1119, yy, count, 16, '#e5eaf0', '600', extra='text-anchor="end"')
    s += '<circle class="halo" cx="663" cy="107" r="75" fill="none" stroke="#75899d" stroke-width="1.3" stroke-dasharray="16 39" opacity=".65"/>'
    s += t(663, 115, total, 29, '#e5eaf0', '600', extra='text-anchor="middle"')
    s += t(32, 196, updated, 11, '#687789')
    return s + '</svg>'


def render(repositories):
    projects = [r for r in repositories if r['name'].lower() != OWNER.lower() and not r.get('fork', False) and not r.get('private', True)]
    languages = Counter(r['language'] for r in projects if r.get('language'))
    updated = datetime.now(timezone(timedelta(hours=-5))).strftime('%d/%m/%Y')
    return render_counts(len(projects), languages, updated)


if __name__ == '__main__':
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')) if len(sys.argv) > 1 else fetch_public_repositories()
    result = render(data)
    (ROOT/'assets').mkdir(parents=True, exist_ok=True)
    (ROOT/'assets'/'metrics-v2.svg').write_text(result, encoding='utf-8')
    print('Updated assets/metrics-v2.svg from public repository data.')
