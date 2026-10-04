#!/usr/bin/env python3
"""Ownership-safe retention of an artifact already produced by fd.py add.

fd.py add refreshes EVERY peer lock entry/attestation on a different host. Keep
only its generated owned entry, and restore unrelated tracked attestations to
HEAD. No provenance facts are hand-authored; Flight Deck's serializer writes the
unchanged old entries plus the fd-generated new entry. Not a generic tool fix.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT/'.flightdeck'))
import artifacts_check as ac

KEY = 'wild-halflife-adoption@1'


def main():
    current = ac.load_lock(str(ROOT))
    old = json.loads(subprocess.check_output(['git', 'show', 'HEAD:artifacts.lock.json'], cwd=ROOT))
    assert KEY not in old['entries'], 'Only safe for a genuinely new owned artifact'
    generated = current['entries'][KEY]
    assert generated['path'] == 'artifacts/wild-halflife-adoption/wild-halflife-adoption-v1.png'
    old['entries'][KEY] = generated
    old['generated'] = current['generated']
    ac.write_lock(str(ROOT), old)
    changed = subprocess.check_output(['git', 'diff', '--name-only', '--', 'attestations'], cwd=ROOT, text=True).splitlines()
    assert all('wild-halflife' not in path for path in changed)
    if changed:
        subprocess.run(['git', 'restore', '--', *changed], cwd=ROOT, check=True)
    # fd add defaults to move. The finding also needs its working-copy figure.
    src = ROOT/generated['path']
    destination = ROOT/'researchers/shadow/notes/wild-halflife/results/fig-adoption.png'
    shutil.copy2(src, destination)
    # Check every peer entry against original, and the generated entry hash.
    result = ac.load_lock(str(ROOT))
    original = json.loads(subprocess.check_output(['git', 'show', 'HEAD:artifacts.lock.json'], cwd=ROOT))
    assert {k:v for k,v in result['entries'].items() if k != KEY} == original['entries']
    assert ac.file_facts(str(src))['sha256'] == generated['sha256']
    print('Kept fd-generated owned figure and provenance; preserved all peer lock entries and attestations')


if __name__ == '__main__':
    main()
