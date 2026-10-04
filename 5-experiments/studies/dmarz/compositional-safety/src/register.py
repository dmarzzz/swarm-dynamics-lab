"""Publish one attempt's frozen plan on the hub and write its source/content-bound receipt (run on the host)."""
import hashlib
import re
import time
import urllib.request
import yaml
import common

HEADINGS = ('TLDR', 'Question and prediction', 'Setup', 'Protocol', 'Metrics', 'Visualization mapping')


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'SwarmLab-PlanPreflight/1.0'}), timeout=25) as r:
        return r.status, r.read(2_000_000).decode()


def register(attempt, getter=fetch, sr=None):
    if sr is None: import swarm_report as sr
    revision = common.git('rev-parse', 'HEAD')
    text = (common.ROOT/'reviews'/f'{attempt}-pre.md').read_text()
    if 'Status: ready' not in text: raise ValueError('plan_not_ready')
    url = f'https://github.com/dmarzzz/swarm-lab/blob/{revision}/researchers/dmarz/notes/compositional-safety/reviews/{attempt}-pre.md'
    status, raw = getter(url.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/'))
    if status != 200 or raw != text: raise ValueError('raw_plan_mismatch')
    status, page = getter(url)
    if status != 200 or any(h not in page for h in HEADINGS): raise ValueError('rendered_page_check_failed')
    tldr = 'TLDR: ' + ' '.join(re.search(r'^## TLDR\n(.*?)(?=^## )', text, re.M | re.S).group(1).split())
    definition = yaml.safe_load((common.ROOT/'experiment.yaml').read_text()); exp = definition.pop('id')
    definition.update(url=url, description=tldr)
    sr.register(exp, **definition)
    receipt = dict(url=url, plan_sha256=hashlib.sha256(raw.encode()).hexdigest(), source_hashes=common.hashes(),
                   registered_tldr=tldr, page_verified_at=time.time(),
                   verification='Fetched the raw GitHub file at this revision (byte-identical to the checkout) and the rendered blob page (HTTP 200; headings '+', '.join(HEADINGS)+' present) immediately before registration. Not a visual inspection.')
    (common.ROOT/'registration').mkdir(exist_ok=True)
    common.dump(common.ROOT/'registration'/f'{attempt}.json', receipt)
    return receipt
