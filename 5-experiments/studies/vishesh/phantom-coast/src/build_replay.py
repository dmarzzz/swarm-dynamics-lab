"""Build labelled local software-fixture replay, never a model experiment."""
import json
from pathlib import Path
from instrument import fixtures

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'visualization'
OUT.mkdir(exist_ok=True)
data={'normal':fixtures(), 'missing':fixtures(fail=True)}
(OUT/'fixture.json').write_text(json.dumps(data,indent=2)+'\n')
template=(Path(__file__).parent/'replay-template.html').read_text()
(OUT/'index.html').write_text(template.replace('__FIXTURE_DATA__',json.dumps(data).replace('<','\\u003c')))
print('Created labelled fixture replay; zero model calls.')
