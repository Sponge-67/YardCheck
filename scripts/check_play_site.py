#!/usr/bin/env python3
"""Reject incomplete or accidentally unsafe public policy pages before deployment."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
PAGES = ('index.html', 'privacy.html', 'terms.html', 'delete-account.html', 'support.html')


def validate(directory=SITE):
    errors = []
    for name in (*PAGES, 'style.css', 'yardcheck-logo.webp'):
        if not (directory / name).is_file():
            errors.append(f'Missing: site/{name}')
    for name in PAGES:
        file = directory / name
        if not file.is_file():
            continue
        text = file.read_text(encoding='utf-8')
        if re.search(r'\{\{[^}]+\}\}', text):
            errors.append(f'{name}: owner placeholders not replaced')
        if name != 'index.html' and not re.search(r'@[^\s<"&]+\.[A-Za-z]{2,}', text):
            errors.append(f'{name}: no actual support email visible')
        if 'href="mailto:' in text and re.search(r'mailto:.*\{\{', text):
            errors.append(f'{name}: invalid mailto placeholder')
    return errors


if __name__ == '__main__':
    failures = validate()
    if failures:
        print('Policy site NOT publishable:\n' + '\n'.join('  - '+e for e in failures), file=sys.stderr)
        sys.exit(2)
    print('Policy site files and contact placeholders: PASS. Owner must still verify every claim, links, and support process.')
