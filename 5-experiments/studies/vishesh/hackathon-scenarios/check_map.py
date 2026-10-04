"""Validate authored mapping coverage and frozen research identity, without network access."""
from pathlib import Path
import json,hashlib,re,collections
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
doc=json.loads((HERE/'scenario-map.json').read_text());rows=doc['mappings'];meta=doc['metadata'];ids={r['id'] for r in rows}
assert len(rows)==len(ids)==301
atlas=json.loads((ROOT/'researchers/dmarz/notes/question-atlas/candidates.json').read_text());a={r['id']:r for r in atlas['candidates']}
assert {r['id'] for r in rows if r['kind']=='Atlas candidate'}==set(a)
prior=json.loads((HERE.parent/'biology-visual-review/assessments.json').read_text())
assert ids=={r['id'] for r in prior['assessments']}
for path,digest in meta['input_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Snapshot changed',path)
assert not meta['registered_hypotheses']
assert len(doc['scenarios'])==19
for r in rows:
 picks=r['ranked_scenarios'];assert 1<=len(picks)<=3
 assert [x['rank'] for x in picks]==list(range(1,len(picks)+1))
 assert len({x['scenario'] for x in picks})==len(picks)
 assert (ROOT/r['path']).is_file()
 for x in picks:assert x['scenario'] in doc['scenarios'] and len(x['candidate_specific_use'])>35
 if r['id'] in a:
  src=a[r['id']]
  assert r['original_question']==src['question'] and r['original_comparison']==src['test']
  assert r['original_metrics']==src['metrics'] and r['original_falsifier']==src['falsifier']
for s in doc['scenarios'].values():assert all(s[k] for k in ['task','minimum_fixture','scoring','baseline','scope_cut','interpretation_risk'])
for p in HERE.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('https://','http://','#')):continue
  dest=p.parent/target.split('#')[0];assert dest.exists(),(p.name,target)
  if '#' in target:assert 'id="'+target.split('#',1)[1]+'"' in dest.read_text(),(p.name,target)
html=(HERE/'review.html').read_text();embedded=re.search(r'<script id="map-data" type="application/json">(.*?)</script>',html,re.S).group(1);assert json.loads(embedded)==doc
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)="https?://',html)
assert json.loads((HERE/'inventory.json').read_text())==meta
atlasrows=[r for r in rows if r['kind']=='Atlas candidate'];counts=collections.Counter(r['ranked_scenarios'][0]['scenario'] for r in atlasrows)
assert sum(counts[k] for k in ['API','RESULT','RESEARCH'])==47
assert sum(any(p['scenario'] in ['API','RESULT','RESEARCH'] for p in r['ranked_scenarios']) for r in atlasrows)==80
assert len(re.findall(r'^## ',(HERE/'ranked-map.md').read_text(),re.M))==301
print('PASS: 214 atlas + 87 related records; 1–3 distinct ranked scenarios each; 19 complete contracts; source hashes; original tests/metrics/falsifiers; local links and anchors; HTML parity; coverage counts.')
