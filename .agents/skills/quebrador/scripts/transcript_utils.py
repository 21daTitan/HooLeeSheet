#!/usr/bin/env python3
"""Normaliza legendas WebVTT como evidência, sem simular visualização do vídeo."""
import html
import re

TIME = re.compile(r'(?P<start>\d{1,2}:\d{2}:\d{2}[.,]\d{1,3})\s*-->\s*(?P<end>\d{1,2}:\d{2}:\d{2}[.,]\d{1,3})')
TAGS = re.compile(r'<[^>]+>')


def parse_vtt(text: str) -> list[dict]:
    """Analisa blocos WebVTT com timecodes, removendo repetições de legendas ASR."""
    segments = []
    for block in re.split(r'\n\s*\n', text.replace('\r\n', '\n')):
        match = TIME.search(block)
        if not match:
            continue
        content = block[match.end():].strip()
        if content and not content.startswith('\n') and re.match(r'^[^\n]*position:', content):
            content = re.sub(r'^\s*[^\n]*\n', '', content, count=1)
        content = html.unescape(TAGS.sub('', content))
        content = ' '.join(content.split())
        if not content:
            continue
        if segments and content == segments[-1]['text']:
            segments[-1]['end'] = match.group('end')
            continue
        segments.append({'start': match.group('start'), 'end': match.group('end'), 'text': content})
    return segments
