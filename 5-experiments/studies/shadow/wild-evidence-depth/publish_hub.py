#!/usr/bin/env python3
"""Optional retrospective result publication. Requires configured swarm_report client.

The offline analyzer never imports this module. No secrets are printed or saved.
"""
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def main():
    try:
        import swarm_report as sr
    except ImportError:
        print('BLOCKED: put the configured swarm_report client on PYTHONPATH; offline results are complete.')
        return 2
    cfg = sr._config()
    if not cfg.get('SWARM_HUB_URL') or not cfg.get('SWARM_HUB_TOKEN'):
        print('BLOCKED: hub URL/token not configured; no network write attempted.')
        return 2
    os.environ['SWARM_SOURCE'] = 'shadow/sol-audit-gap'
    spec = json.loads((ROOT / 'experiment.json').read_text())
    result = json.loads((ROOT / 'results/summary.json').read_text())
    sr.register(spec['id'], **{k: spec[k] for k in ('title', 'description', 'owner', 'url', 'params', 'metrics', 'primary_metric')})
    with sr.start(spec['id'], run='wild-evidence-depth/A1-census', params={'stage': 'A1'},
                  message='Retrospective saved-data census upload, not new model execution') as run:
        for relative, name in [('results/summary.json', 'summary.json'), ('results/coverage.svg', 'coverage.svg'),
                               ('results/reference-check.json', 'reference-check.json'), ('FINDING.md', 'FINDING.md')]:
            run.artifact(ROOT / relative, name)
        d = result['payload_direct_response_coverage']
        run.done(message='Fixed-export census complete. Coverage is not success.',
                 payload_response_coverage=d['fraction'], rows=result['rows'],
                 payloads=d['denominator'], response_linked_payloads=d['numerator'], cost_usd=0, model_calls=0)
    print('Published own saved-data census and four derived artifacts.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
