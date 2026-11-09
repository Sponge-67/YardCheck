#!/usr/bin/env python3
"""Fill public operator/support contact placeholders in the GitHub Pages site.

Never put private access tokens, keystore data or tester details in these pages.
"""
import argparse
from html import escape
from pathlib import Path
import re
import sys

PROJECT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'privacy.html', 'terms.html', 'delete-account.html', 'support.html')


def main():
    parser = argparse.ArgumentParser(description='Finalize public YardCheck policy/support pages')
    parser.add_argument('--operator', required=True, help='Actual operator/developer name to publish')
    parser.add_argument('--support-email', required=True, help='Working public support mailbox (not a private token)')
    args = parser.parse_args()
    name, email = args.operator.strip(), args.support_email.strip()
    if not name or re.search(r'[<>\r\n]',name) or len(name)>120:
        parser.error('Choose a nonempty operator name without HTML markup')
    if not re.fullmatch(r'[A-Za-z0-9.!#$%&\'\*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',email):
        parser.error('Supply an actual email address without spaces or quotation marks')
    for file in (PROJECT/'site'/f for f in PAGES):
        data=file.read_text(encoding='utf-8')
        updated=data.replace('{{OPERATOR_NAME}}',escape(name,quote=True)).replace('{{SUPPORT_EMAIL}}',escape(email,quote=True))
        file.write_text(updated,encoding='utf-8')
    print('Public site operator/contact populated. Review site/privacy.html, terms.html, and deletion process BEFORE publishing.')
    print('Run python3 scripts/check_play_site.py to verify placeholders are gone.')

if __name__ == '__main__':
    main()
