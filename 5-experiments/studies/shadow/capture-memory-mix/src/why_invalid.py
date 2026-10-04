#!/usr/bin/env python3
"""Count invalid-episode reasons per pilot dir."""
import json, sys
from collections import Counter
from pathlib import Path
for d in sys.argv[1:]:
    c = Counter()
    for f in Path(d).glob("MP_*.jsonl"):
        for l in f.read_text().splitlines():
            e = json.loads(l)
            if not e["validity"]["ok"]:
                c[e["validity"]["error"][:90]] += 1
    print(d, dict(c))
