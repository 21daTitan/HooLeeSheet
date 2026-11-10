#!/usr/bin/env python3
"""Compila a lista não verificada de fontes do usuário a partir do catalog_raw.txt."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ONLY = {'EVASION', 'CHEATS', 'C2', 'AD', 'AI-ATTACK', 'KERNEL', 'REDTEAM'}
MANUAL_REVIEW = {'NETWORK', 'MOBILE', 'EXTRA_RE', 'EXTRA_TOOLS'}

index = {}
for ln, line in enumerate((ROOT / 'references/catalog_raw.txt').read_text().splitlines(), 1):
    if not line.strip():
        continue
    category, items = line.split(':', 1)
    for item in items.split(','):
        slug = item.strip()
        if slug.count('/') != 1 or ' ' in slug:
            raise ValueError(f'slug inválido {slug!r} linha {ln}')
        key = slug.casefold()
        if key not in index:
            index[key] = {
                'repo': slug,
                'url': f'https://github.com/{slug}',
                'categories': [],
                'review_status': 'not_verified',
                'clone_permission': 'none',
                'scope': ('research_only' if category in RESEARCH_ONLY
                          else ('manual_review' if category in MANUAL_REVIEW else 'read_only')),
            }
        obj = index[key]
        if category not in obj['categories']:
            obj['categories'].append(category)
        if category in RESEARCH_ONLY:
            obj['scope'] = 'research_only'
        elif category in MANUAL_REVIEW and obj['scope'] == 'read_only':
            obj['scope'] = 'manual_review'

aliases = json.loads((ROOT / 'references/aliases.json').read_text())['aliases']
for old, info in aliases.items():
    obj = index[old.casefold()]
    obj['current_repo'] = info['current']
    obj['current_url'] = f"https://github.com/{info['current']}"
    obj['current_basis'] = info['basis']
out = list(index.values())
(ROOT / 'references/repository_catalog.json').write_text(
    json.dumps({
        'notice': 'Source slugs as provided; not yet verified as extant, safe, open source, or currently maintained. Never auto-clone, install, run, or execute them.',
        'total_distinct': len(out),
        'entries': out,
    }, ensure_ascii=False, indent=2) + '\n')
print(f'{len(out)} repos distintos, {sum(len(v["categories"]) for v in out)} atribuições de categoria')
