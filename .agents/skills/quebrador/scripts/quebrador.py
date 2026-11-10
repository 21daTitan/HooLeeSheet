#!/usr/bin/env python3
"""Foco No Progresso — Quebrador CLI v1.3.0

Sem dependências externas obrigatórias. Backends opcionais para análise audiovisual.
Nenhum código de terceiros é executado, instalado ou clonado sem autorização.
"""
from __future__ import annotations
import argparse
import base64
import importlib.util
import ipaddress
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from urllib.parse import urlparse, urlunparse, parse_qs, parse_qsl, urlencode, quote
from urllib.request import ProxyHandler, Request, build_opener, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/policy.json'
CATALOG = ROOT / 'references/repository_catalog.json'
STATE = ROOT / 'state'
OUTPUT = ROOT / 'outputs'
LANES = set(json.loads(CONFIG.read_text(encoding='utf-8'))['lanes'])


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    tmp.replace(path)


def clean_url(raw: str) -> str:
    """Normaliza URLs públicas suportadas. Nenhuma requisição é feita."""
    src = raw.strip()
    p = urlparse(src)
    if p.scheme not in ('https', 'http') or not p.hostname:
        raise ValueError('Use a valid http(s) URL; local files are handled by video command')
    host = p.hostname.lower()
    if p.username or p.password or host in ('localhost',) or host.endswith(('.local', '.internal', '.localhost')):
        raise ValueError('Refusing URLs with embedded credentials or local hosts')
    try:
        ip = ipaddress.ip_address(host)
        if not ip.is_global:
            raise ValueError('Non-public IP host refused')
    except ValueError as exc:
        if str(exc) == 'Non-public IP host refused':
            raise
    if host in ('youtu.be', 'www.youtu.be'):
        ident = p.path.strip('/').split('/')[0]
        if not re.fullmatch(r'[a-zA-Z0-9_-]{11}', ident):
            raise ValueError('Invalid YouTube video ID')
        return f'https://www.youtube.com/watch?v={ident}'
    if host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        if p.path == '/watch':
            ident = parse_qs(p.query).get('v', [''])[0]
            if not re.fullmatch(r'[a-zA-Z0-9_-]{11}', ident):
                raise ValueError('Invalid YouTube video ID')
            return f'https://www.youtube.com/watch?v={ident}'
        if p.path == '/playlist':
            ident = parse_qs(p.query).get('list', [''])[0]
            if not re.fullmatch(r'[a-zA-Z0-9_-]+', ident):
                raise ValueError('Invalid playlist ID')
            return f'https://www.youtube.com/playlist?list={ident}'
    query = urlencode([(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                       if not k.lower().startswith('utm_') and k.lower() not in ('si', 'is', 'feature', 'fbclid', 'gclid')])
    return urlunparse(('https', host, p.path.rstrip('/') or '/', '', query, ''))


def detect_type(url: str) -> str:
    host = urlparse(url).hostname or ''
    if host.endswith('youtube.com') or host.endswith('youtu.be'):
        return 'youtube'
    if host.endswith('github.com'):
        return 'github'
    if 'notion.' in host:
        return 'notion'
    return 'web'


def record_reference(url: str, lane: str, note: str = '') -> dict:
    if lane not in LANES:
        raise ValueError(f'Invalid lane {lane}; choose {sorted(LANES)}')
    canonical = clean_url(url)
    return {
        'id': sha256(canonical.encode()).hexdigest()[:16],
        'url': canonical,
        'type': detect_type(canonical),
        'lane': lane,
        'note': note,
        'intake_utc': stamp(),
        'status': 'queued_not_analyzed',
        'source_evidence': [],
        'confidence': 0.0,
        'approval': 'pending',
    }


# ── Subcomandos ──────────────────────────────────────────────────────────────

def doctor(args):
    print('Quebrador — Diagnóstico de ambiente (somente leitura)')
    print('Python:', sys.version.split()[0])
    print('Root:', ROOT)
    for binname in ('ffprobe', 'ffmpeg', 'scenedetect', 'yt-dlp', 'git', 'gh', 'repomix'):
        print(f'{binname}: {shutil.which(binname) or "não encontrado (opcional)"}')
    for name in ('faster_whisper', 'scenedetect'):
        try:
            ok = importlib.util.find_spec(name) is not None
        except Exception:
            ok = False
        print(f'Python {name}:', 'disponível' if ok else 'não instalado (opcional)')
    ref_files = list((ROOT / 'references').rglob('*.md')) + list((ROOT / 'references').rglob('*.json'))
    print(f'Arquivos de referência: {len(ref_files)}')
    print('Política: sem clone em massa, sem auto-install, sem auto-merge, master protegido')


def inventory(args):
    doc = load_json(CATALOG, {'entries': []})
    scopes = Counter(x['scope'] for x in doc['entries'])
    print(f"Repositórios no catálogo: {len(doc['entries'])} distintos; verificação não implícita")
    print('Escopos:', dict(scopes))
    print('MCPs no inventário:', len((ROOT / 'references/mcps_requested.txt').read_text().splitlines()), 'não instalados')
    print('Skills no inventário:', len((ROOT / 'references/skills_requested.txt').read_text().splitlines()), 'não instaladas')
    refs = load_json(ROOT / 'references/sources.json', {})
    print('Links YouTube referenciados:', len(refs.get('youtube', [])), 'na fila, não assistidos')
    print('Fila de intake:', len(load_json(STATE / 'intake.json', [])))
    results = load_json(STATE / 'repo-health.json', {'repositories': {}}).get('repositories', {})
    print('Verificações de metadados:', len(results), '(não são clones)')
    cl = load_json(STATE / 'clone-report.json', [])
    print('Repos clonados com autorização:', sum(x.get('status') == 'cloned_for_read_only_review' for x in cl))
    print('Pacotes instalados por esta skill: 0')
    cat_dirs = ['security', 'websites', 'youtube', 'creative', 'external']
    for d in cat_dirs:
        p = ROOT / 'references' / d
        if p.exists():
            files = list(p.rglob('*'))
            print(f'Catálogo {d}/: {len([f for f in files if f.is_file()])} arquivo(s)')


def intake(args):
    entry = record_reference(args.url, args.lane, args.note)
    path = STATE / 'intake.json'
    items = load_json(path, [])
    duplicates = [i for i in items if i['id'] == entry['id']]
    if duplicates:
        print(f"Referência existente: {entry['id']} ({duplicates[0]['lane']}) — não adicionada novamente")
        return
    items.append(entry)
    save_json(path, items)
    append_history('intake', {'id': entry['id'], 'url': entry['url'], 'lane': entry['lane']})
    print(json.dumps(entry, ensure_ascii=False, indent=2))


def _github_metadata(slug: str, timeout: int = 12):
    parts = slug.split('/')
    if len(parts) != 2 or not all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) for p in parts):
        return {'status': 'invalid_identifier', 'reason': 'Invalid owner/repo structure'}
    url = 'https://api.github.com/repos/' + quote(parts[0]) + '/' + quote(parts[1])
    req = Request(url, headers={'User-Agent': 'Quebrador-Research/1.1', 'Accept': 'application/vnd.github+json'})
    try:
        with urlopen(req, timeout=timeout) as response:
            value = json.load(response)
        return {
            'status': 'found',
            'canonical_name': value.get('full_name', ''),
            'archived': bool(value.get('archived')),
            'disabled': bool(value.get('disabled')),
            'visibility': value.get('visibility', 'unknown'),
            'default_branch': value.get('default_branch'),
            'license': (value.get('license') or {}).get('spdx_id'),
            'pushed_at': value.get('pushed_at'),
            'description': str(value.get('description') or '')[:200],
        }
    except HTTPError as exc:
        if exc.code == 404:
            return {'status': 'not_found', 'reason': 'HTTP 404; moved/private/removed/typo possible'}
        if exc.code in (401, 403, 429):
            return {'status': 'blocked', 'reason': f'HTTP {exc.code}; auth/rate limit'}
        return {'status': 'temporary_error', 'reason': f'HTTP {exc.code}'}
    except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        return {'status': 'temporary_error', 'reason': type(exc).__name__}


def search_batches(slugs: list[str], size: int = 5, max_query: int = 240) -> list[list[str]]:
    """Agrupa slugs em lotes que cabem no limite de tamanho da busca do GitHub."""
    batches, current = [], []
    for slug in slugs:
        candidate = current + [slug]
        if current and (len(candidate) > size or len(_search_query(candidate)) > max_query):
            batches.append(current)
            current = [slug]
        else:
            current = candidate
    if current:
        batches.append(current)
    return batches


def _search_query(slugs: list[str]) -> str:
    return ' '.join('repo:' + s for s in slugs) + ' fork:true'


def _gh_search(slugs: list[str], timeout: int = 40) -> dict | None:
    """Metadados por nome canônico (casefold); None quando nenhum slug existe (HTTP 422)."""
    proc = subprocess.run(['gh', 'api', '-X', 'GET', 'search/repositories', '-f', 'q=' + _search_query(slugs),
                           '-f', 'per_page=100'], capture_output=True, text=True, timeout=timeout)
    if proc.returncode:
        if 'HTTP 422' in proc.stderr:
            return None
        raise RuntimeError((proc.stderr or proc.stdout).strip()[-300:] or 'gh api falhou')
    found = {}
    for item in json.loads(proc.stdout).get('items', []):
        found[item['full_name'].casefold()] = {
            'status': 'found', 'method': 'search', 'canonical_name': item['full_name'],
            'archived': bool(item.get('archived')), 'disabled': bool(item.get('disabled')),
            'fork': bool(item.get('fork')), 'visibility': item.get('visibility', 'unknown'),
            'default_branch': item.get('default_branch'),
            'license': (item.get('license') or {}).get('spdx_id'),
            'pushed_at': item.get('pushed_at'), 'description': str(item.get('description') or '')[:200]}
    return found


NOT_FOUND = {'status': 'not_found', 'method': 'search',
             'reason': 'Busca não encontrou; inexistente, privado, removido ou renomeado'}


def check_repos_search(args, pause=time.sleep):
    """Verifica o catálogo pela busca do GitHub, em lotes; não clona nem baixa código."""
    if not shutil.which('gh'):
        raise RuntimeError('gh ausente; o backend search depende do GitHub CLI')
    slugs = [r['repo'] for r in load_json(CATALOG, {'entries': []})['entries']]
    if not args.all:
        slugs = slugs[:args.limit]
    state = load_json(STATE / 'repo-health.json', {'cursor': 0, 'repositories': {}})
    results = state.get('repositories', {})
    changed, queries = [], 0

    def query(group):
        nonlocal queries
        if queries:
            pause(2.2)
        queries += 1
        try:
            return _gh_search(group)
        except RuntimeError as exc:
            if 'rate limit' not in str(exc).lower():
                raise
            pause(65)
            return _gh_search(group)

    def store(slug, result):
        if results.get(slug) != result:
            changed.append({'repo': slug, 'previous': results.get(slug), 'current': result})
        results[slug] = result
        print(f"[{result['status']}] {slug}")

    pending = []
    for group in search_batches(slugs):
        found = query(group) or {}
        for slug in group:
            if slug.casefold() in found:
                store(slug, found[slug.casefold()])
            else:
                pending.append(slug)
    for slug in pending:
        found = query([slug])
        if not found:
            store(slug, dict(NOT_FOUND))
        else:
            result = dict(next(iter(found.values())))
            if result['canonical_name'].casefold() != slug.casefold():
                result['renamed_from'] = slug
            store(slug, result)
    count = Counter(results[s]['status'] for s in slugs)
    state['repositories'] = results
    save_json(STATE / 'repo-health.json', state)
    save_json(STATE / 'repo-delta.json', {'generated_utc': stamp(), 'changes': changed,
                                          'checked': dict(count), 'processed': len(slugs)})
    append_history('check-repos-search', {'processed': len(slugs), 'states': dict(count), 'queries': queries})
    print('RELATÓRIO:', json.dumps({'processados': len(slugs), 'consultas': queries, 'estados': dict(count),
                                    'mudanças': len(changed)}, ensure_ascii=False))
    return results


def check_repos(args):
    if args.backend == 'search':
        return check_repos_search(args)
    doc = load_json(CATALOG, {'entries': []})
    records = doc['entries']
    if not records:
        raise RuntimeError('Catálogo de repositórios vazio')
    existing = load_json(STATE / 'repo-health.json', {'cursor': 0, 'repositories': {}})
    cursor = existing.get('cursor', 0) % len(records)
    limit = min(args.limit, len(records))
    results = existing.get('repositories', {})
    count = {'found': 0, 'not_found': 0, 'blocked': 0, 'temporary_error': 0, 'invalid_identifier': 0}
    changed = []
    processed = 0
    for i in range(limit):
        index = (cursor + i) % len(records)
        item = records[index]
        result = _github_metadata(item['repo'], timeout=args.timeout)
        status = result.get('status')
        count[status] = count.get(status, 0) + 1
        if status in ('blocked', 'temporary_error'):
            print(f"[!] {item['repo']}: {result['reason']}")
            if status == 'blocked':
                break
            continue
        old = results.get(item['repo'])
        if old != result:
            changed.append({'repo': item['repo'], 'previous': old, 'current': result})
        results[item['repo']] = result
        processed = i + 1
        print(f"[{status}] {item['repo']}")
    existing['cursor'] = (cursor + processed) % len(records)
    existing['repositories'] = results
    save_json(STATE / 'repo-health.json', existing)
    save_json(STATE / 'repo-delta.json', {'generated_utc': stamp(), 'changes': changed, 'checked': count, 'processed': processed})
    print('RELATÓRIO:', json.dumps({'processados': processed, 'total_metadata': len(results), 'estados': count, 'mudanças': len(changed)}, ensure_ascii=False))


MEDIA_HOSTS = ('youtube.com', 'youtu.be', 'vimeo.com', 'tiktok.com', 'instagram.com', 'facebook.com')


def video_url(args):
    canonical = clean_url(args.url)
    host = urlparse(canonical).hostname or ''
    if not any(host == x or host.endswith('.' + x) for x in MEDIA_HOSTS):
        raise ValueError('Host de mídia não suportado; registre via intake')
    if not shutil.which('yt-dlp'):
        raise RuntimeError('yt-dlp ausente. Ver docs/RESEARCH.md; nenhuma requisição tentada')
    ident = sha256(canonical.encode('utf-8')).hexdigest()[:16]
    dest = OUTPUT / ('url-' + ident)
    dest.mkdir(exist_ok=True, parents=True)
    cmd = ['yt-dlp', '--dump-single-json', '--skip-download', '--no-warnings', '--no-playlist', canonical]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=160, cwd=dest)
    except subprocess.TimeoutExpired:
        raise RuntimeError('Timeout de 160 segundos na busca de metadados')
    if proc.returncode:
        result = {'id': ident, 'source': canonical, 'status': 'blocked_or_unavailable',
                  'reason': proc.stderr[-700:], 'observed_at': stamp(), 'caption_evidence': False}
        save_json(dest / 'reference.json', result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    try:
        meta = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError('Extrator retornou JSON inválido') from exc
    allowed = {'id', 'title', 'uploader', 'channel', 'webpage_url', 'duration', 'upload_date', 'description',
               'language', 'view_count', 'categories', 'tags', 'license', 'extractor_key'}
    safe = {key: meta.get(key) for key in allowed if key in meta}
    if safe.get('description'):
        safe['description'] = safe['description'][:5000]
    if safe.get('tags'):
        safe['tags'] = safe['tags'][:30]
    result = {'id': ident, 'source': canonical, 'status': 'metadata_only',
              'observed_at': stamp(), 'metadata': safe, 'subtitles': {'status': 'not_requested'},
              'video_frames': 'not_analyzed', 'sound_design': 'not_analyzed', 'creative_breakdown': 'pending'}
    if args.subtitles:
        subcmd = ['yt-dlp', '--skip-download', '--no-warnings', '--no-playlist', '--write-subs',
                  '--write-auto-subs', '--sub-langs', 'pt.*,en.*', '--sub-format', 'vtt',
                  '-o', str(dest / 'subtitles.%(ext)s'), canonical]
        try:
            p2 = subprocess.run(subcmd, capture_output=True, text=True, timeout=160, cwd=dest)
            paths = list(dest.glob('subtitles.*.vtt'))
            sys.path.insert(0, str(ROOT / 'scripts'))
            from transcript_utils import parse_vtt
            captions = []
            for file in paths[:8]:
                cues = parse_vtt(file.read_text(encoding='utf-8', errors='replace'))
                captions.append({'filename': file.name, 'cue_count': len(cues), 'cues': cues})
            result['subtitles'] = {'status': 'ok' if captions else 'unavailable',
                                   'files': captions, 'error': p2.stderr[-400:] if p2.returncode else ''}
            if captions:
                result['status'] = 'metadata_and_subtitles'
        except subprocess.TimeoutExpired:
            result['subtitles'] = {'status': 'timeout'}
    save_json(dest / 'reference.json', result)
    print(f"Referência salva: {dest / 'reference.json'}")
    print(f"Nível de evidência: {result['status']}; visuais/áudio não afirmados")


def clone_approved(args):
    """Clone explícito de fonte verificada e baixo risco, sem execução."""
    if not args.approve:
        raise ValueError('Clone bloqueado até --approve explícito; revise o repo e riscos antes')
    record = next((r for r in load_json(CATALOG, {'entries': []})['entries']
                    if r['repo'].casefold() == args.repo.casefold()), None)
    if not record:
        raise ValueError('Repositório não está no catálogo')
    if record['scope'] != 'read_only':
        raise ValueError('Categoria do repositório requer revisão manual de risco')
    validated = load_json(ROOT / 'references/verification_sample.json', {}).get('confirmed_public', [])
    if not any(v.casefold() == args.repo.casefold() for v in validated):
        raise ValueError('Sem aprovação verificada de baixo risco para este repositório')
    if not shutil.which('git'):
        raise RuntimeError('git ausente')
    out = (ROOT / 'vendor-review' / args.repo.replace('/', '__')).resolve()
    if out.exists():
        raise ValueError(f'Destino já existe: {out}; sem sobrescrita')
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run(['git', 'clone', '--depth', '1', '--no-recurse-submodules',
                               'https://github.com/' + args.repo + '.git', str(out)],
                              timeout=240, capture_output=True, text=True)
        status = 'cloned_for_read_only_review' if proc.returncode == 0 else 'failed'
        reason = proc.stderr[-500:] if proc.returncode else ''
    except subprocess.TimeoutExpired:
        status = 'failed'
        reason = 'timeout after 240s'
    report = {'repo': args.repo, 'status': status, 'reason': reason, 'path': str(out),
              'timestamp': stamp(), 'executed_third_party_code': False}
    log = load_json(STATE / 'clone-report.json', [])
    log.append(report)
    save_json(STATE / 'clone-report.json', log)
    append_history('clone-approved', {'repo': args.repo, 'status': status})
    print(json.dumps(report, ensure_ascii=False, indent=2))


def _ffprobe(path: Path):
    if not shutil.which('ffprobe'):
        return {'status': 'tool_missing', 'tool': 'ffprobe'}
    proc = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries',
         'format=duration,size,format_name:stream=index,codec_type,codec_name,width,height,avg_frame_rate,sample_rate',
         '-of', 'json', str(path)],
        capture_output=True, text=True, timeout=40)
    if proc.returncode:
        return {'status': 'error', 'stderr': proc.stderr[:800]}
    return {'status': 'ok', 'data': json.loads(proc.stdout)}


def video(args):
    path = Path(args.path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f'Arquivo de vídeo não encontrado: {path}')
    if path.stat().st_size > 10 * 1024 ** 3:
        raise ValueError('Arquivo acima de 10GiB; inspecione separadamente')
    hash_ = sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 ** 2), b''):
            hash_.update(chunk)
    key = hash_.hexdigest()[:16]
    item_dir = OUTPUT / key
    item_dir.mkdir(parents=True, exist_ok=True)
    result = {
        'id': key, 'file': str(path), 'sha256': hash_.hexdigest(), 'date_utc': stamp(),
        'authorization': 'Arquivo local fornecido pelo usuário; usuário responsável pelos direitos',
        'technical': _ffprobe(path), 'scenes': {'status': 'not_analyzed'},
        'frames': {'status': 'not_analyzed'}, 'transcript': {'status': 'not_analyzed'},
        'creative_analysis': {
            'status': 'pending_human_or_multimodal_review',
            'not_verified': ['hook', 'CTA', 'camera', 'color', 'audio_design', 'copy', 'storytelling'],
        },
    }
    if args.scenes:
        try:
            from scenedetect import detect, ContentDetector
            scenes = detect(str(path), ContentDetector())
            result['scenes'] = {'status': 'ok', 'cut_count': max(0, len(scenes) - 1),
                                'intervals': [{'start': a.get_timecode(), 'end': b.get_timecode()} for a, b in scenes[:200]]}
        except ImportError:
            result['scenes'] = {'status': 'tool_missing', 'tool': 'scenedetect'}
        except Exception as exc:
            result['scenes'] = {'status': 'error', 'reason': str(exc)[:500]}
    if args.frames:
        if not shutil.which('ffmpeg'):
            result['frames'] = {'status': 'tool_missing', 'tool': 'ffmpeg'}
        else:
            frames = item_dir / 'frames'
            frames.mkdir(exist_ok=True)
            subprocess.run(
                ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(path),
                 '-vf', "select='eq(n,0)+gte(t,10*selected_n)',scale=480:-2",
                 '-fps_mode', 'vfr', '-frames:v', '24', str(frames / 'frame_%03d.png')],
                capture_output=True, text=True, timeout=600)
            pics = sorted(p.name for p in frames.glob('frame_*.png'))
            result['frames'] = {'status': 'ok' if pics else 'error', 'count': len(pics), 'files': pics}
    if args.transcribe:
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel(args.model, device='cpu', compute_type='int8')
            segments, info = model.transcribe(str(path), beam_size=3)
            transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segments]
            result['transcript'] = {'status': 'ok', 'language': info.language, 'segments': transcript}
        except ImportError:
            result['transcript'] = {'status': 'tool_missing', 'tool': 'faster_whisper'}
        except Exception as exc:
            result['transcript'] = {'status': 'error', 'reason': str(exc)[:500]}
    save_json(item_dir / 'analysis.json', result)
    print(f"Análise salva: {item_dir / 'analysis.json'}")
    print(f"Técnico: {result['technical']['status']} | Cenas: {result['scenes']['status']} | "
          f"Frames: {result['frames']['status']} | Transcrição: {result['transcript']['status']}")


def report(args):
    doc = load_json(CATALOG, {'entries': []})
    health = load_json(STATE / 'repo-health.json', {'repositories': {}})
    changes = load_json(STATE / 'repo-delta.json', {'changes': [], 'checked': {}, 'processed': 0})
    intake_items = load_json(STATE / 'intake.json', [])
    statuses = Counter(x['status'] for x in health['repositories'].values())
    clones = load_json(STATE / 'clone-report.json', [])
    lines = [
        '# Foco No Progresso — Status da pesquisa', '',
        f'Gerado: {stamp()}', '',
        f"- Repositórios distintos no catálogo: **{len(doc['entries'])}** (listados, não clonados).",
        f"- Repositórios consultados via metadados públicos: **{len(health['repositories'])}**.",
        f'- Estados de metadata: {dict(statuses)}.',
        f"- Alterações em última consulta: **{len(changes.get('changes', []))}**.",
        f"- Links adicionados ao intake: **{len(intake_items)}** (conteúdo não consumido automaticamente).",
        f"- Repos clonados com autorização: **{sum(c.get('status') == 'cloned_for_read_only_review' for c in clones)}**; "
        f"falhas: **{sum(c.get('status') == 'failed' for c in clones)}**; pacotes instalados: **0**.",
        '- Ferramentas MCP em inventário: **30**, não instaladas.',
        '- Skill labels em inventário: **32**, não instaladas.',
        '', '## Alterações encontradas — revisar', '',
    ]
    for ch in changes.get('changes', [])[:80]:
        lines.append(f"- `{ch['repo']}`: `{(ch['previous'] or {}).get('status', 'new')}` → `{ch['current'].get('status')}`")
    if not changes.get('changes'):
        lines.append('- Nenhuma mudança registrada na última execução.')
    lines += ['', '## Regras de publicação', '',
              'Apenas metadados e relatórios entram na proposta automatizada; nenhum código de terceiros foi executado ou instalado.',
              'Qualquer mudança no master prompt, política, identidade, dependências ou código requer aprovação explícita.']
    text = '\n'.join(lines) + '\n'
    path = STATE / 'research-report.md'
    path.write_text(text, encoding='utf-8')
    print(text)


FREESOUND_SEARCH = 'https://freesound.org/apiv2/search/text/'


def sfx(args):
    """Busca efeitos sonoros no Freesound; baixa prévias só com --download."""
    key = os.environ.get('FREESOUND_API_KEY')
    if not key:
        raise RuntimeError('FREESOUND_API_KEY ausente. Crie uma chave gratuita em '
                           'https://freesound.org/apiv2/apply/ e defina a variável de ambiente')
    params = urlencode({'query': args.query, 'page_size': args.limit,
                        'fields': 'id,name,duration,license,username,previews',
                        'filter': f'duration:[0 TO {args.max_duration}]'})
    req = Request(FREESOUND_SEARCH + '?' + params,
                  headers={'Authorization': 'Token ' + key, 'User-Agent': 'Quebrador-Research/1.2'})
    try:
        with urlopen(req, timeout=20) as response:
            data = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f'Freesound respondeu HTTP {exc.code}') from exc
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f'Falha ao consultar o Freesound: {type(exc).__name__}') from exc
    results = [{'id': r.get('id'), 'name': r.get('name'), 'duration': r.get('duration'),
                'license': r.get('license'), 'author': r.get('username'),
                'preview': (r.get('previews') or {}).get('preview-hq-mp3')}
               for r in data.get('results', [])]
    dest = OUTPUT / ('sfx-' + sha256(args.query.encode('utf-8')).hexdigest()[:16])
    for item in results[:args.download]:
        url = urlparse(item['preview'] or '')
        host = url.hostname or ''
        if url.scheme != 'https' or not (host == 'freesound.org' or host.endswith('.freesound.org')):
            item['download'] = 'recusado: host fora do Freesound'
            continue
        dest.mkdir(parents=True, exist_ok=True)
        target = dest / f"{int(item['id'])}.mp3"
        try:
            with urlopen(Request(item['preview'], headers={'User-Agent': 'Quebrador-Research/1.2'}), timeout=60) as response:
                target.write_bytes(response.read())
            item['download'] = str(target)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            item['download'] = f'falhou: {type(exc).__name__}'
    save_json(dest / 'results.json', {'query': args.query, 'source': 'freesound.org',
                                      'observed_at': stamp(), 'results': results})
    if args.download:
        append_history('sfx-download', {'query': args.query, 'files': [i.get('download') for i in results[:args.download]]})
    for item in results:
        print(f"[{item['id']}] {item['name']} — {item['duration']}s — autor: {item['author']}")
        print(f"    licença: {item['license']}")
        print(f"    prévia: {item.get('download') or item['preview']}")
    print(f"{len(results)} resultado(s) salvos em {dest / 'results.json'}; respeite a licença e a atribuição de cada som")
    return results


def _is_local_host(host: str) -> bool:
    if host == 'localhost':
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_loopback or ip.is_private


def build_tts_body(text: str, fmt: str = 'wav', reference_id: str | None = None,
                   reference_audio: bytes | None = None, reference_text: str = '') -> dict:
    """Corpo no contrato ServeTTSRequest do Fish Speech."""
    body = {'text': text, 'format': fmt}
    if reference_id:
        body['reference_id'] = reference_id
    if reference_audio is not None:
        body['references'] = [{'audio': base64.b64encode(reference_audio).decode('ascii'), 'text': reference_text}]
    return body


def tts(args):
    """Gera voz por um servidor Fish Speech local; nunca chama serviço pago."""
    server = urlparse(args.server)
    if server.scheme not in ('http', 'https') or not server.hostname or not _is_local_host(server.hostname):
        raise ValueError('Servidor recusado: tts só usa Fish Speech local (localhost ou rede privada). '
                         'Serviço pago exige autorização específica do dono')
    audio = None
    if args.reference_audio:
        if not args.consent:
            raise ValueError('Referência de voz bloqueada sem --consent: use só voz própria ou com consentimento verificável')
        if not args.reference_text:
            raise ValueError('--reference-audio exige --reference-text com a transcrição da amostra')
        audio = Path(args.reference_audio).expanduser().read_bytes()
    body = build_tts_body(args.text, args.format, args.reference_id, audio, args.reference_text)
    req = Request(args.server.rstrip('/') + '/v1/tts', data=json.dumps(body).encode('utf-8'),
                  headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with build_opener(ProxyHandler({})).open(req, timeout=args.timeout) as response:
            data = response.read()
    except HTTPError as exc:
        raise RuntimeError(f'Servidor Fish local respondeu HTTP {exc.code}: {exc.read()[:300]!r}') from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f'Servidor Fish local não respondeu em {args.server} ({type(exc).__name__}); '
                           'ver references/creative/audio-efeitos-sonoros.md') from exc
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    ident = sha256(data).hexdigest()
    save_json(OUTPUT / f'tts-{ident[:16]}.json', {
        'text': args.text, 'server': args.server, 'format': args.format, 'file': str(out), 'sha256': ident,
        'reference_id': args.reference_id, 'voice_reference_used': audio is not None,
        'consent_declared': bool(args.consent), 'date_utc': stamp()})
    append_history('tts', {'file': str(out), 'sha256': ident, 'voice_reference_used': audio is not None})
    print(f'Áudio salvo: {out} ({len(data)} bytes)')


def validate(args):
    """Valida consistência dos catálogos."""
    errors = []
    doc = load_json(CATALOG, {'entries': []})
    urls_seen = set()
    for entry in doc['entries']:
        key = entry['repo'].casefold()
        if key in urls_seen:
            errors.append(f"Duplicata no catálogo: {entry['repo']}")
        urls_seen.add(key)
        if entry['review_status'] != 'not_verified':
            errors.append(f"Status inesperado para {entry['repo']}: {entry['review_status']}")
        if entry['clone_permission'] != 'none':
            errors.append(f"Permissão de clone inesperada para {entry['repo']}: {entry['clone_permission']}")

    for jfile in (ROOT / 'references').rglob('*.json'):
        try:
            json.loads(jfile.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            errors.append(f"JSON inválido em {jfile.relative_to(ROOT)}: {exc}")

    policy = load_json(CONFIG, {})
    if policy.get('authorization', {}).get('default') != 'deny':
        errors.append("Política de autorização não está em 'deny' por padrão")

    sources = load_json(ROOT / 'references/sources.json', {})
    if sources.get('verification_state') != 'pending':
        errors.append("Estado de verificação deveria ser 'pending'")

    domain = args.domain
    if domain == 'all' or domain == 'repos':
        print(f"Repositórios no catálogo: {len(doc['entries'])}")
        print(f"URLs únicas: {len(urls_seen)}")
    if domain == 'all' or domain == 'refs':
        json_count = len(list((ROOT / 'references').rglob('*.json')))
        md_count = len(list((ROOT / 'references').rglob('*.md')))
        print(f"Arquivos de referência: {json_count} JSON, {md_count} Markdown")

    if errors:
        print(f"\nERROS ENCONTRADOS: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\nValidação concluída sem erros.")


def refs(args):
    """Lista referências do intake."""
    items = load_json(STATE / 'intake.json', [])
    if not items:
        print('Nenhuma referência no intake.')
        return
    for item in items:
        print(f"[{item['lane']}] {item['url']} — {item['status']} (confiança: {item['confidence']})")


def refs_add(args):
    """Atalho para intake."""
    intake(args)


def _chain(prev: str, entry: dict) -> str:
    core = {k: entry[k] for k in ('timestamp', 'action', 'detail')}
    return sha256((prev + json.dumps(core, sort_keys=True, ensure_ascii=False)).encode('utf-8')).hexdigest()


def append_history(action: str, detail: dict) -> dict:
    path = STATE / 'history.json'
    history = load_json(path, [])
    entry = {'timestamp': stamp(), 'action': action, 'detail': detail}
    entry['chain_hash'] = _chain(history[-1]['chain_hash'] if history else '', entry)
    history.append(entry)
    save_json(path, history)
    return entry


def verify_history(history: list) -> int | None:
    """Índice do primeiro registro adulterado, ou None se a cadeia confere."""
    prev = ''
    for i, entry in enumerate(history):
        try:
            if entry['chain_hash'] != _chain(prev, entry):
                return i
        except (KeyError, TypeError):
            return i
        prev = entry['chain_hash']
    return None


def record(args):
    """Exibe histórico com hash encadeado."""
    history = load_json(STATE / 'history.json', [])
    if not history:
        print('Nenhum registro no histórico.')
        return
    for entry in history[-20:]:
        print(f"[{entry.get('timestamp', '?')}] {entry.get('action', '?')} — hash: {str(entry.get('chain_hash', '?'))[:16]}")
    if args.verify:
        bad = verify_history(history)
        if bad is not None:
            raise RuntimeError(f'Histórico adulterado a partir do registro {bad + 1} de {len(history)}')
        print(f'Cadeia íntegra: {len(history)} registro(s)')


MD_DOMAINS = {'web': 'websites', 'creative': 'creative', 'external': 'external'}


def _md_rows(folder: str) -> list[tuple[str, list[str]]]:
    rows = []
    for file in sorted((ROOT / 'references' / folder).glob('*.md')):
        lines = file.read_text(encoding='utf-8').splitlines()
        for i, line in enumerate(lines):
            if not line.startswith('|') or set(line) <= set('|-: '):
                continue
            if i + 1 < len(lines) and lines[i + 1].startswith('|') and set(lines[i + 1]) <= set('|-: '):
                continue
            rows.append((file.stem, [c.strip() for c in line.strip('|').split('|')]))
    return rows


def catalog(args):
    """Consulta os catálogos locais; somente leitura, sem rede."""
    category = (args.category or '').casefold()
    if args.domain == 'repos':
        items = [(' '.join(e['categories']), f"{e['repo']} [{', '.join(e['categories'])}] {e['scope']} — {e['url']}"
                  + (f" → nome atual provável: {e['current_repo']}" if e.get('current_repo') else ''))
                 for e in load_json(CATALOG, {'entries': []})['entries']
                 if not category or category in (c.casefold() for c in e['categories'])]
    elif args.domain in ('mcp', 'skills'):
        name = 'mcps_requested.txt' if args.domain == 'mcp' else 'skills_requested.txt'
        items = [('', l.strip() + ' (inventário, não instalado)')
                 for l in (ROOT / 'references' / name).read_text(encoding='utf-8').splitlines() if l.strip()]
    elif args.domain == 'yt':
        items = [(e.get('setor', ''), f"[{e.get('setor')}] {e.get('titulo_fornecido')} — {e.get('url')} ({e.get('status')})")
                 for e in load_json(ROOT / 'references/youtube/fontes-aprendizado.json', {'entries': []})['entries']]
        items = [i for i in items if not category or category == i[0].casefold()]
    else:
        items = [(stem, f"[{stem}] " + ' | '.join(cells)) for stem, cells in _md_rows(MD_DOMAINS[args.domain])
                 if not category or category in stem.casefold()]
    term = (args.search or '').casefold()
    lines = [text for _, text in items if term in text.casefold()]
    for text in lines:
        print(text)
    print(f'{len(lines)} resultado(s) em {args.domain}; itens não verificados')
    return lines


def main():
    parser = argparse.ArgumentParser(prog='quebrador', description='Foco No Progresso (Quebrador) — CLI de pesquisa baseada em evidência')
    sub = parser.add_subparsers(dest='cmd', required=True)

    sub.add_parser('doctor', help='Diagnóstico de ambiente')
    sub.add_parser('inventory', help='Inventário completo dos catálogos')
    sub.add_parser('report', help='Gera relatório de status da pesquisa')
    sub.add_parser('refs', help='Lista referências do intake')
    p = sub.add_parser('record', help='Exibe histórico encadeado')
    p.add_argument('--verify', action='store_true', help='Recalcula a cadeia e acusa adulteração')

    p = sub.add_parser('catalog', help='Consulta os catálogos locais')
    p.add_argument('domain', choices=['repos', 'mcp', 'skills', 'web', 'creative', 'external', 'yt'])
    p.add_argument('--category', help='Categoria (repos), arquivo (web/creative/external) ou setor (yt)')
    p.add_argument('--search', help='Termo a procurar')

    p = sub.add_parser('intake', help='Registra nova referência na fila')
    p.add_argument('url')
    p.add_argument('--lane', choices=sorted(LANES), default='core')
    p.add_argument('--note', default='')

    p = sub.add_parser('refs-add', help='Atalho para intake')
    p.add_argument('url')
    p.add_argument('--lane', choices=sorted(LANES), default='core')
    p.add_argument('--note', default='')

    p = sub.add_parser('video-url', help='Extrai metadados/legendas de URL de vídeo')
    p.add_argument('url')
    p.add_argument('--subtitles', action='store_true', help='Buscar legendas disponíveis')

    p = sub.add_parser('video', help='Analisa arquivo de vídeo local')
    p.add_argument('path')
    p.add_argument('--frames', action='store_true')
    p.add_argument('--scenes', action='store_true')
    p.add_argument('--transcribe', action='store_true')
    p.add_argument('--model', default='tiny', help='Modelo Whisper (pode baixar pesos)')

    p = sub.add_parser('clone-approved', help='Clone de fonte verificada com autorização')
    p.add_argument('repo')
    p.add_argument('--approve', action='store_true')

    p = sub.add_parser('check-repos', help='Verifica metadados públicos dos repos')
    p.add_argument('--backend', choices=['api', 'search'], default='api', help='search usa gh api search/repositories')
    p.add_argument('--all', action='store_true', help='Catálogo inteiro (só com --backend search)')
    p.add_argument('--limit', type=int, default=20)
    p.add_argument('--timeout', type=int, default=12)

    p = sub.add_parser('validate', help='Valida consistência dos catálogos')
    p.add_argument('--domain', choices=['all', 'repos', 'refs'], default='all')

    p = sub.add_parser('sfx', help='Busca efeitos sonoros no Freesound (requer FREESOUND_API_KEY)')
    p.add_argument('query')
    p.add_argument('--limit', type=int, default=10, choices=range(1, 31), metavar='1..30')
    p.add_argument('--max-duration', type=int, default=30, help='Duração máxima em segundos')
    p.add_argument('--download', type=int, default=0, help='Baixar a prévia MP3 dos N primeiros')

    p = sub.add_parser('tts', help='Gera voz por servidor Fish Speech local (sem créditos)')
    p.add_argument('text')
    p.add_argument('--out', required=True)
    p.add_argument('--server', default='http://localhost:8080')
    p.add_argument('--format', choices=['wav', 'mp3', 'opus', 'pcm'], default='wav')
    p.add_argument('--reference-id')
    p.add_argument('--reference-audio', help='Amostra de voz autorizada')
    p.add_argument('--reference-text', default='', help='Transcrição da amostra')
    p.add_argument('--consent', action='store_true', help='Declara consentimento do dono da voz')
    p.add_argument('--timeout', type=int, default=300)

    args = parser.parse_args()
    if args.cmd == 'check-repos' and args.all and args.backend != 'search':
        parser.error('--all só vale com --backend search')
    if args.cmd == 'check-repos' and not args.all and not (1 <= args.limit <= 30):
        parser.error('--limit deve ser 1..30 (segurança de rate limit da API GitHub)')
    try:
        globals()[args.cmd.replace('-', '_')](args)
    except (ValueError, RuntimeError, FileNotFoundError) as exc:
        parser.exit(2, f'ERRO: {exc}\n')


if __name__ == '__main__':
    main()
