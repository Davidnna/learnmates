#!/usr/bin/env python3
"""Static migration checks for LearnMeets AI. Does not contact services or modify data."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'frontend' / 'src' / 'App.jsx'
CLIENT = ROOT / 'frontend' / 'src' / 'api' / 'client.js'
BACKEND = ROOT / 'app.py'
PKG = ROOT / 'frontend' / 'package.json'

checks = []
def check(label, passed):
    checks.append((label, bool(passed)))

try:
    app = APP.read_text(encoding='utf-8')
    client = CLIENT.read_text(encoding='utf-8')
    backend = BACKEND.read_text(encoding='utf-8')
    package = json.loads(PKG.read_text(encoding='utf-8'))
except Exception as exc:
    print(f'ERROR: Could not read project files: {exc}')
    sys.exit(2)

check('React entry point exists', (ROOT / 'frontend/src/main.jsx').is_file())
check('Vite build script is defined', 'build' in package.get('scripts', {}))
check('API client is present', bool(client.strip()))
check('React app includes account-management UI reference', bool(re.search(r'account', app, re.I)))
check('React app does not contain notification/bell UI references', not bool(re.search(r'notification|bell', app, re.I)))
check('React app includes back-navigation logic/reference', bool(re.search(r'back|navigate\(-1\)|history\.back', app, re.I)))
check('Backend includes account profile API route', '/api/account/profile' in backend)
check('Backend includes account password API route', '/api/account/password' in backend)
check('Backend includes session API route', '/api/session' in backend)
check('Vercel SPA rewrite config exists', (ROOT / 'frontend/vercel.json').is_file())
check('Python test files are present', any((ROOT / 'tests').glob('test_*.py')))

for label, passed in checks:
    print(f"{'PASS' if passed else 'FAIL'}: {label}")
passed = sum(ok for _, ok in checks)
print(f'\nStatic result: {passed}/{len(checks)} passed')
sys.exit(0 if passed == len(checks) else 1)
