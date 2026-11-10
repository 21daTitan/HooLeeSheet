import argparse
import re
import importlib.util
import io
import json
import os
import tempfile
from unittest import mock
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('quebrador', ROOT / 'scripts/quebrador.py')
quebrador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quebrador)


class CatalogTest(unittest.TestCase):
    def test_catalog_structure(self):
        data = json.loads((ROOT / 'references/repository_catalog.json').read_text())
        repos = data['entries']
        self.assertEqual(len(repos), data['total_distinct'])
        self.assertEqual(len(repos), len({r['repo'].lower() for r in repos}))
        self.assertTrue(all(r['review_status'] == 'not_verified' for r in repos))
        self.assertTrue(all(r['clone_permission'] == 'none' for r in repos))
        self.assertTrue(any('EVASION' in r['categories'] and r['scope'] == 'research_only' for r in repos))

    def test_no_autonomous_critical_change(self):
        cfg = json.loads((ROOT / 'config/policy.json').read_text())
        a = cfg['autonomy']
        for key in ('auto_merge_pr', 'auto_install_dependencies', 'auto_clone_unverified_repositories',
                     'auto_update_protected_master_prompt', 'auto_run_third_party_code'):
            self.assertFalse(a[key])
        self.assertIn('sagaz', cfg['lanes'])
        self.assertIn('creator', cfg['lanes'])
        self.assertTrue(a['require_explicit_owner_permission_for_all_state_changes'])
        self.assertTrue(a['scheduled_changes_disabled_by_default'])
        self.assertEqual(cfg['authorization']['default'], 'deny')
        self.assertFalse(a['auto_open_review_proposals'])

    def test_normalize_youtube(self):
        self.assertEqual(quebrador.clean_url('https://youtu.be/e2Fykz51Nxg?is=x'),
                         'https://www.youtube.com/watch?v=e2Fykz51Nxg')
        self.assertEqual(quebrador.clean_url('https://www.youtube.com/watch?v=e2Fykz51Nxg&t=22'),
                         'https://www.youtube.com/watch?v=e2Fykz51Nxg')
        with self.assertRaises(ValueError):
            quebrador.clean_url('file:///etc/passwd')
        with self.assertRaises(ValueError):
            quebrador.clean_url('http://admin:pw@localhost/a')

    def test_intake_evidence_defaults(self):
        entry = quebrador.record_reference('https://youtu.be/e2Fykz51Nxg', 'creator', 'test')
        self.assertEqual(entry['status'], 'queued_not_analyzed')
        self.assertEqual(entry['confidence'], 0.0)
        self.assertEqual(entry['approval'], 'pending')
        self.assertEqual(entry['lane'], 'creator')
        with self.assertRaises(ValueError):
            quebrador.record_reference('https://example.com', 'unallowed')

    def test_transcript_parser(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from transcript_utils import parse_vtt
        source = 'WEBVTT\n\n00:00:00.100 --> 00:00:01.100\n<v Speaker>Olá</v> mundo\n\n00:00:01.100 --> 00:00:02.100\nOlá mundo\n'
        cues = parse_vtt(source)
        self.assertEqual(len(cues), 1)
        self.assertEqual(cues[0]['text'], 'Olá mundo')
        self.assertEqual(cues[0]['end'], '00:00:02.100')

    def test_source_list_unverified(self):
        src = json.loads((ROOT / 'references/sources.json').read_text())
        self.assertEqual(src['verification_state'], 'pending')
        self.assertEqual(len(src['youtube']), 10)

    def test_sources_has_domains(self):
        src = json.loads((ROOT / 'references/sources.json').read_text())
        self.assertIn('domains', src)
        self.assertIn('security', src['domains'])
        self.assertIn('youtube', src['domains'])
        self.assertIn('creative', src['domains'])

    def test_reference_catalogs_exist(self):
        for path in ['security/repos-catalog.md', 'security/mcp-servers.md',
                      'security/skills-catalog.md', 'security/attack-surface-map.md',
                      'websites/bancos-exploits.md', 'creative/ferramentas-design.md',
                      'youtube/fontes-aprendizado.json', 'external/projetos-github.md']:
            self.assertTrue((ROOT / 'references' / path).exists(), f'Faltando: references/{path}')

    def test_youtube_catalog_structure(self):
        data = json.loads((ROOT / 'references/youtube/fontes-aprendizado.json').read_text())
        self.assertIn('entries', data)
        self.assertTrue(all(e.get('status') == 'nao_revisado' for e in data['entries']))

    def test_policy_version(self):
        cfg = json.loads((ROOT / 'config/policy.json').read_text())
        self.assertEqual(cfg['version'], '1.2.1')

    def test_validate_json_files(self):
        for jfile in (ROOT / 'references').rglob('*.json'):
            try:
                json.loads(jfile.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                self.fail(f'JSON inválido: {jfile.relative_to(ROOT)}')


class AudioTest(unittest.TestCase):
    def _sfx_args(self, **kw):
        return argparse.Namespace(**{'query': 'chuva', 'limit': 5, 'max_duration': 30, 'download': 0, **kw})

    def _tts_args(self, **kw):
        base = {'text': 'teste', 'out': 'x.wav', 'server': 'http://localhost:8080', 'format': 'wav',
                'reference_id': None, 'reference_audio': None, 'reference_text': '', 'consent': False, 'timeout': 5}
        return argparse.Namespace(**{**base, **kw})

    def test_sfx_requires_key(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                quebrador.sfx(self._sfx_args())

    def test_sfx_parses_results_and_hides_key(self):
        payload = {'results': [{'id': 7, 'name': 'Chuva forte', 'duration': 4.2, 'username': 'ana',
                                'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
                                'previews': {'preview-hq-mp3': 'https://cdn.freesound.org/previews/0/7.mp3'}}]}
        seen = {}

        def fake(req, timeout=0):
            seen['url'] = req.full_url
            seen['auth'] = req.get_header('Authorization')
            return io.BytesIO(json.dumps(payload).encode())

        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.dict(os.environ, {'FREESOUND_API_KEY': 'CHAVE-TESTE'}), \
                mock.patch.object(quebrador, 'OUTPUT', Path(tmp)), \
                mock.patch.object(quebrador, 'urlopen', fake), \
                mock.patch('builtins.print'):
            results = quebrador.sfx(self._sfx_args())
            saved = list(Path(tmp).glob('sfx-*/results.json'))
            self.assertEqual(len(saved), 1)
            self.assertNotIn('CHAVE-TESTE', saved[0].read_text())
        self.assertNotIn('CHAVE-TESTE', seen['url'])
        self.assertEqual(seen['auth'], 'Token CHAVE-TESTE')
        self.assertEqual(results[0]['author'], 'ana')
        self.assertTrue(results[0]['preview'].endswith('7.mp3'))

    def test_tts_local_only(self):
        for host in ('localhost', '127.0.0.1', '192.168.1.10', '10.0.0.5'):
            self.assertTrue(quebrador._is_local_host(host))
        for host in ('api.fish.audio', '8.8.8.8', 'localhost.evil.com'):
            self.assertFalse(quebrador._is_local_host(host))
        with self.assertRaises(ValueError):
            quebrador.tts(self._tts_args(server='https://api.fish.audio'))

    def test_tts_voice_reference_needs_consent(self):
        with self.assertRaises(ValueError):
            quebrador.tts(self._tts_args(reference_audio='voz.wav', reference_text='oi'))

    def test_tts_body_contract(self):
        body = quebrador.build_tts_body('oi', 'wav', reference_audio=b'RIFF', reference_text='amostra')
        self.assertEqual(body['references'], [{'audio': 'UklGRg==', 'text': 'amostra'}])
        self.assertNotIn('reference_audio', body)
        self.assertEqual(quebrador.build_tts_body('oi'), {'text': 'oi', 'format': 'wav'})


class CatalogCommandTest(unittest.TestCase):
    def _run(self, **kw):
        args = argparse.Namespace(**{'category': None, 'search': None, **kw})
        with mock.patch('builtins.print'):
            return quebrador.catalog(args)

    def test_every_domain_returns_rows(self):
        for domain in ('repos', 'mcp', 'skills', 'web', 'creative', 'external', 'yt'):
            self.assertTrue(self._run(domain=domain), domain)

    def test_filters(self):
        c2 = self._run(domain='repos', category='C2')
        self.assertEqual(len(c2), 18)
        self.assertTrue(any('BishopFox/sliver' in line for line in c2))
        self.assertEqual(len(self._run(domain='mcp')), 30)
        self.assertEqual(len(self._run(domain='skills')), 32)
        self.assertEqual(len(self._run(domain='yt')), 10)
        self.assertTrue(any('publicwww.com' in line for line in self._run(domain='web', search='publicwww')))
        self.assertFalse(any('---' in line or '| URL |' in line for line in self._run(domain='web')))

    def test_owner_site_list_is_complete(self):
        text = ''.join(f.read_text() for f in (ROOT / 'references/websites').glob('*.md'))
        for host in ('exploit-db.com', 'shodan.io', 'zoomeye.hk', 'fofa.info', 'onyphe.io', 'publicwww.com',
                     'packetstormsecurity.com', 'null-byte.wonderhowto.com', 'cve.mitre.org', 'cvedetails.com',
                     'nvd.nist.gov', 'kb.cert.org', 'virustotal.com', 'virusscan.jotti.org', 'kali.org/tools',
                     'blackarch.org', 'pentest-tools.com', 'romhacking.net', 'yougetsignal.com', 'dnswatch.info',
                     'search.dnslytics.com', 'coffer.com', 'bgp.he.net', 'securitytrails.com', 'ip-api.com',
                     'whatismyip.com', 'ip2location.com', 'ipaddress.com', 'cmd5.org', 'crackstation.net',
                     'hash.online-convert.com', 'cryptext.eu', 'crypt.uticraft.com', 'ipleak.net'):
            self.assertIn(host, text)

    def test_documented_commands_exist(self):
        docs = [ROOT / 'SKILL.md', *(ROOT / 'docs').glob('*.md'), *(ROOT / 'references').rglob('*.md')]
        cited = set()
        for doc in docs:
            cited |= set(re.findall(r'quebrador\.py ([a-z][a-z-]*)', doc.read_text()))
        self.assertIn('catalog', cited)
        for cmd in cited:
            self.assertTrue(callable(getattr(quebrador, cmd.replace('-', '_'), None)), cmd)
        table = re.findall(r'\| `catalog ([a-z]+)` \|', (ROOT / 'SKILL.md').read_text())
        self.assertEqual(sorted(table), sorted(['repos', 'mcp', 'skills', 'web', 'yt', 'creative', 'external']))


class HistoryTest(unittest.TestCase):
    def test_chain_detects_tampering(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(quebrador, 'STATE', Path(tmp)):
            quebrador.append_history('intake', {'url': 'https://a.example'})
            quebrador.append_history('tts', {'file': 'x.wav'})
            path = Path(tmp) / 'history.json'
            history = json.loads(path.read_text())
            self.assertIsNone(quebrador.verify_history(history))
            history[0]['detail']['url'] = 'https://b.example'
            self.assertEqual(quebrador.verify_history(history), 0)
            path.write_text(json.dumps(history))
            with mock.patch('builtins.print'), self.assertRaises(RuntimeError):
                quebrador.record(argparse.Namespace(verify=True))


if __name__ == '__main__':
    unittest.main()
