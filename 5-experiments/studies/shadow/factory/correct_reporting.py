"""Dated reporting-only correction. Never modifies frozen specs, code or raw outcomes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
p=ROOT/'README.md';t=p.read_text().replace('all five initial pool attempts returned HTTP429 before any model answer (20 failed requests total)','the five initial pool attempts returned 8 HTTP429 and 12 HTTP503 failures before any model answer (20 failed requests total)');p.write_text(t)
p=ROOT/'AMENDMENT-PAID.md';t=p.read_text().replace('The five pool specs each stopped after their first four qualification requests returned HTTP429:','The five pool specs each stopped after their first four qualification requests failed (8 HTTP429 and12 HTTP503 in total; corrected from the initial429-only shorthand):');p.write_text(t)
p=ROOT.parent/'notes/audit-2026-10-04/sol-factory.md';t=p.read_text().replace('**20 pool HTTP429 failures**','**20 pool transport failures (8 HTTP429,12 HTTP503)**');p.write_text(t)
for name in ('split-sonnet-four-checks','split-sonnet-no-links-strong','split-sonnet-no-links-weak'):
    p=ROOT/'results'/(name+'-or')/'FINDING.md'
    if p.exists():p.write_text(p.read_text().replace('four HTTP429 errors','four HTTP503 errors'))
