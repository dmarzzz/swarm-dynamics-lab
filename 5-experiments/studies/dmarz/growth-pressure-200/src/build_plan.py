#!/usr/bin/env python3
"""Build the public document from PLAN, preserving text and usable repository links."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
source = BASE/'PLAN.md'
text = source.read_text()

def link(match):
    label, dest = match.groups()
    if '://' in dest or dest.startswith('#'):
        return match.group(0)
    local, sep, anchor = dest.partition('#')
    relative = (BASE/local).resolve().relative_to(ROOT).as_posix()
    return f'[{label}](https://github.com/dmarzzz/swarm-lab/blob/main/{relative}' + (f'#{anchor}' if sep else '') + ')'

text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
text += '\n\n---\n\nThis filed copy is generated from the study’s PLAN.md. Git and Flight Deck preserve the source and ingredient digests; related working-document links use main. Operational preregistration must use the immutable publication revision and content hash.\n'
out = BASE/'src/out/growth-pressure-200-plan.md'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(text)
print(out)
