#!/usr/bin/env python3
"""Build a self-contained offline viewer solely from measured replay receipts."""
import argparse
import json
from pathlib import Path
import replay_loop as loop

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / 'replay-viewer.html.in'


def render(result):
    payload = {k: result[k] for k in ('summary', 'credit_ledger', 'frames')}
    payload['groups'] = {g: {k: v[k] for k in ('physical_records', 'invalid_records', 'logical_records', 'selected_valid_records', 'first_attempt_valid_records', 'invalid_then_valid_logical_records')} for g, v in result['reference_reports'].items()}
    encoded = json.dumps(payload, separators=(',', ':'), ensure_ascii=True).replace('<', '\\u003c')
    return TEMPLATE.read_text().replace('__REPLAY_DATA__', encoded)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    result = loop.run()
    if result != loop.load_json(loop.RESULTS / 'replay.json'):
        raise ValueError('viewer requires verified saved replay')
    html = render(result)
    out = loop.RESULTS / 'replay.html'
    if args.verify:
        if out.read_text() != html:
            raise ValueError('viewer does not match replay')
        print('Viewer matches every saved frame and receipt.')
    else:
        with out.open('x') as f:
            f.write(html)
        print('Wrote self-contained offline viewer: ' + str(out.relative_to(HERE)))


if __name__ == '__main__':
    main()
