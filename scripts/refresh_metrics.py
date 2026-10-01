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


def render(repositories):
    projects = [r for r in repositories if r['name'].lower() != OWNER.lower() and not r.get('fork', False)]
    languages = Counter(r['language'] for r in projects if r.get('language'))
    lang_total = sum(languages.values())
    updated = datetime.now(timezone(timedelta(hours=-5))).strftime('%d/%m/%Y')
    s = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="255" viewBox="0 0 1200 255" role="img" aria-labelledby="title desc"><title id="title">GitHub: repositorios públicos y lenguajes principales</title><desc id="desc">Datos de repositorios públicos propios, excluido el repositorio de presentación. El gráfico cuenta el lenguaje principal de cada repositorio.</desc><style>text{font-family:Arial,Helvetica,sans-serif}</style><rect x="1" y="1" width="560" height="253" rx="12" fill="#0d1117" stroke="#30363d"/><rect x="578" y="1" width="621" height="253" rx="12" fill="#0d1117" stroke="#30363d"/>'''
    s += t(26, 39, 'GitHub / datos públicos', 21, '#c9d1d9', '600')
    s += t(28, 107, len(projects), 43, '#edf1f5', '700')
    s += t(265, 107, len(languages), 43, '#edf1f5', '700')
    s += t(28, 138, 'Repositorios propios', 15, '#8b949e')
    s += t(265, 138, 'Lenguajes principales', 15, '#8b949e')
    s += '<path d="M26 169H535" stroke="#30363d"/>'
    s += t(26, 199, 'Versiones, código e historial en GitHub.', 15, '#8b949e')
    s += t(26, 228, 'Actualizado: ' + updated, 12, '#768390')
    s += t(603, 39, 'Lenguaje principal por repositorio', 21, '#c9d1d9', '600')
    s += t(603, 67, f'{lang_total} repositorios públicos con lenguaje detectado', 13, '#8b949e')
    x = 604
    palette = ['#a3b1bf', '#788b9f', '#566b81', '#364b62', '#b9c4cf', '#64778c']
    for i, (name, count) in enumerate(languages.most_common()):
        color = palette[i % len(palette)]
        width = 565 * count / lang_total if lang_total else 0
        s += f'<rect x="{x:.2f}" y="90" width="{width:.2f}" height="12" fill="{color}"/>'
        x += width
        lx, ly = 611 + (i % 2) * 282, 140 + (i // 2) * 27
        s += f'<circle cx="{lx}" cy="{ly-5}" r="4" fill="{color}"/>'
        s += t(lx+12, ly, f'{name} · {count}', 14, '#b6c2cf')
    s += t(603, 228, 'Distribución por repositorios, no por nivel de dominio.', 12, '#768390')
    return s + '</svg>'


if __name__ == '__main__':
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')) if len(sys.argv) > 1 else fetch_public_repositories()
    result = render(data)
    (ROOT/'assets').mkdir(parents=True, exist_ok=True)
    (ROOT/'assets'/'metrics-v2.svg').write_text(result, encoding='utf-8')
    print('Updated assets/metrics-v2.svg from public repository data.')
