"""Check snapshot completeness, source identity and local links without network access."""
import hashlib
import json
from pathlib import Path
import re
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
doc = json.loads((HERE/'assessments.json').read_text())
meta = doc['metadata']; records = doc['assessments']
ids = {r['id'] for r in records}
assert len(ids) == len(records) == 301
atlas = json.loads((ROOT/'researchers/dmarz/notes/question-atlas/candidates.json').read_text())
assert {r['id'] for r in records if r['kind']=='Atlas candidate'} == {r['id'] for r in atlas['candidates']}
for kind,path,key in [('VX extension','atlas-review/extensions.json','extensions'),('PX extension','priority-research-expansion/ideas.json','ideas')]:
 source=json.loads((ROOT/'researchers/vishesh/notes'/path).read_text())
 assert {r['id'] for r in records if r['kind']==kind} == {r['id'] for r in source[key]}
assert {r['id'][3:] for r in records if r['kind']=='Original brief'} == {p.stem for p in (ROOT/'researchers/vishesh/notes/project-briefs').glob('*.md') if p.name!='README.md'}
for p,digest in meta['input_sha256'].items():
 assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest, f'Snapshot changed: {p}'
for r in records:
 for key in ['id','title','kind','path','mechanism','promise','visual_value','assessment','visual_design','biological_connection','transfer_limit']:
  assert r[key],(r['id'],key)
 assert (ROOT/r['path']).is_file()
 assert set(r['related'])<=ids,(r['id'],set(r['related'])-ids)
 assert set(r['source_anchors'])<=doc['sources'].keys()
 assert set(r['briefs'])<={p.stem for p in (ROOT/'researchers/vishesh/notes/project-briefs').glob('*.md')}
for p in HERE.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('https://','http://','#')):continue
  assert (p.parent/target.split('#')[0]).exists(),(p.name,target)
 for ident in re.findall(r'\[\[([a-z0-9-]+)\]\]',p.read_text()):
  assert list((ROOT/'library').glob('*/'+ident+'.md')),(p.name,ident)
html=(HERE/'review.html').read_text()
embedded=re.search(r'<script id="review-data" type="application/json">(.*?)</script>',html,re.S).group(1)
assert json.loads(embedded)==doc,'HTML data differs from assessment data'
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)="https?://',html),'External asset dependency'
assert json.loads((HERE/'inventory.json').read_text())==meta
print('PASS: 301 unique records; all atlas, VX/PX and brief IDs covered; 26 input hashes; local links; canonical citations; embedded HTML data.')
