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
COLORS = {'HTML': '#fb8b9a', 'JavaScript': '#f5d574', 'CSS': '#b4a2ff', 'Jupyter Notebook': '#42e8e0', 'Python': '#75b4e8', 'PHP': '#f3a6ca'}


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
    metrics = [('PROYECTOS PÚBLICOS', len(projects), 'Repositorios propios'), ('SITIOS CON GITHUB PAGES', sum(bool(r.get('has_pages')) for r in projects), 'Pages habilitado'), ('LENGUAJES PRINCIPALES', len(languages), 'Detectados por GitHub'), ('FORKS RECIBIDOS', sum(r.get('forks_count', 0) for r in projects), 'En proyectos públicos')]
    updated = datetime.now(timezone(timedelta(hours=-5))).strftime('%d/%m/%Y')
    s = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="380" viewBox="0 0 1280 380" role="img" aria-labelledby="title desc"><title id="title">GitHub: proyectos públicos y lenguajes principales</title><desc id="desc">Métricas calculadas sobre repositorios públicos propios. El gráfico cuenta el lenguaje principal de cada repositorio; no mide nivel de dominio ni porcentaje de líneas de código.</desc><style>text{font-family:Arial,Helvetica,sans-serif}.light{animation:pulse 4s ease-in-out infinite}@keyframes pulse{50%{opacity:.4}}@media(prefers-reduced-motion:reduce){.light{animation:none}}</style><rect x="1" y="1" width="1278" height="378" rx="18" fill="#080d19" stroke="#26354c"/>'''
    for i, (label, value, subtitle) in enumerate(metrics):
        x = 28 + i * 313
        color = ['#42e8e0', '#a995ff', '#f3a6ca', '#f5d574'][i]
        s += f'<rect x="{x}" y="24" width="286" height="132" rx="13" fill="#101829" stroke="#26354c"/>'
        s += t(x+17, 51, label, 11, color, '700', 'letter-spacing="1.2"')
        s += t(x+17, 106, value, 45, '#edf4ff', '700')
        s += t(x+17, 134, subtitle, 12, '#8fa3bf')
    s += t(28, 197, 'LENGUAJE PRINCIPAL POR PROYECTO', 12, '#a995ff', '700', 'letter-spacing="2"')
    s += t(28, 224, f'{lang_total} repositorios con lenguaje identificado', 14, '#8fa3bf')
    x = 28
    for i, (name, count) in enumerate(languages.most_common()):
        color = COLORS.get(name, '#95a7c8')
        w = (1200 * count / lang_total) if lang_total else 0
        s += f'<rect x="{x:.2f}" y="245" width="{w:.2f}" height="15" fill="{color}"/>'
        x += w
        col, row = i % 4, i // 4
        lx, ly = 34 + col * 300, 290 + row * 22
        s += f'<circle cx="{lx}" cy="{ly-5}" r="5" fill="{color}"/>'
        s += t(lx+13, ly, f'{name} · {count} ({count/lang_total:.0%})', 14, '#c4d0e3')
    s += '<path d="M28 331H1252" stroke="#26354c"/>'
    s += '<circle cx="34" cy="353" r="4" fill="#42e8e0" class="light"/>'
    s += t(47, 358, f'Actualizado: {updated} · Solo proyectos públicos · Perfil excluido del cálculo', 12, '#8fa3bf')
    s += t(1073, 358, 'GITHUB / METRICS', 11, '#42e8e0', '700', 'letter-spacing="1"')
    s += '</svg>'
    return s


if __name__ == '__main__':
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')) if len(sys.argv) > 1 else fetch_public_repositories()
    result = render(data)
    (ROOT/'assets').mkdir(parents=True, exist_ok=True)
    (ROOT/'assets'/'metrics-v2.svg').write_text(result, encoding='utf-8')
    print('Updated assets/metrics-v2.svg from public repository data.')
