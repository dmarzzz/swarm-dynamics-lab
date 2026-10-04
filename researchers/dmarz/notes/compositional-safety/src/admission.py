"""Bind a launch to the current immutable, publicly registered attempt plan."""
import hashlib
import json
import re
import time
import urllib.request
import common


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'SwarmLab-PlanPreflight/1.0'}),timeout=25) as response:
        return response.read(2_000_000).decode()


def check(attempt, receipt=None, getter=fetch):
    receipt=receipt or json.loads((common.ROOT/'registration'/f'{attempt}.json').read_text())
    revision=common.git('rev-parse','HEAD')
    relative=f'researchers/dmarz/notes/compositional-safety/reviews/{attempt}-pre.md'
    expected=f'https://github.com/dmarzzz/swarm-lab/blob/{revision}/{relative}'
    if receipt.get('url')!=expected or receipt.get('source_hashes')!=common.hashes(): raise ValueError('stale_plan_binding')
    if not 0<=time.time()-receipt.get('page_verified_at',0)<3600: raise ValueError('stale_page_verification')
    raw=expected.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    markdown=getter(raw)
    digest=hashlib.sha256(markdown.encode()).hexdigest()
    if digest!=receipt.get('plan_sha256') or markdown!=(common.ROOT/'reviews'/f'{attempt}-pre.md').read_text(): raise ValueError('plan_content_mismatch')
    sections={m.group(1):m.group(2).strip() for m in re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',markdown,re.M|re.S)}
    if any(not sections.get(s) for s in ('TLDR','Question and prediction','Setup','Protocol','Metrics')): raise ValueError('plan_sections_missing')
    state=json.loads(getter('https://swarm-live.pages.dev/api/state'))
    experiment=next((e for e in state['experiments'] if e['id']==common.EXP),{})
    if experiment.get('url')!=expected or experiment.get('description')!=receipt.get('registered_tldr'): raise ValueError('public_registration_mismatch')
    if not receipt.get('registered_tldr','').startswith('TLDR: '): raise ValueError('missing_registered_tldr')
    return dict(receipt,launch_verified_at=time.time())
