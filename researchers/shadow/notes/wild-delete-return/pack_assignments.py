#!/usr/bin/env python3
"""Losslessly package the frozen derived table; keep the raw JSON local and unchanged."""
import gzip
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent/'results/A1'
raw=(ROOT/'assignments.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='6d73776a23153143e681dbd5ac7cecdc86eb8d78881e5438e353536c3061d75a'
target=ROOT/'assignments.json.gz'
packed=gzip.compress(raw,compresslevel=9,mtime=0)
assert gzip.decompress(packed)==raw
if target.exists():
    assert target.read_bytes()==packed
else:
    target.write_bytes(packed)
    target.chmod(0o444)
print(f'Frozen derived table: {len(raw)} bytes -> {len(packed)} bytes, round-trip exact')
