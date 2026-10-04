"""Export inspected fixture inputs and an expected-action preview. Never dispatch."""
import datetime
import hashlib
import html
import json
from pathlib import Path
import subprocess
import sys
from cases import BASE, CONDITIONS, build, digest, reference, score


def main():
    check=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(BASE/'tests'),'-v'],capture_output=True,text=True)
    if check.returncode:
        print(check.stdout+check.stderr)
        raise SystemExit(check.returncode)
    output=BASE/'offline';output.mkdir(exist_ok=True)
    manifest=build()
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2,allow_nan=False)+'\n')
    dependencies=[BASE/'PLAN.md',BASE/'cases.py',BASE/'prepare_offline.py',BASE/'next-run-plan.json',BASE/'DIAGNOSTIC-REVIEW.json',BASE/'STARTUP-REPAIR.md',BASE.parent/'rd5/src/rd5_core.py',BASE.parent/'rd5/src/common.py',BASE.parent/'src/jev.py'] + sorted(BASE.glob('native*.py')) + sorted((BASE/'tests').glob('test_*.py'))
    root=BASE.parents[4]
    checks={'kind':'offline known-answer and fault fixtures; no native execution','native_calls':0,
            'tests_passed':check.stderr.count(' ... ok'), 'assignments':len(manifest['assignments']),
            'Q0_requests':18,'D0_requests':144,'D0_cases':12,'D0_base_families':6,'semantic_grammars':3,
            'literal_reference_matches':sum(reference(a['request'])==a['expected'] for a in manifest['assignments']),
            'maximum_ordered_request_bytes':max(len(json.dumps(a['request'],separators=(',',':')).encode()) for a in manifest['assignments']),
            'manifest_sha256':hashlib.sha256((output/'manifest.json').read_bytes()).hexdigest(),
            'dependencies':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies},
            'review_boundary':'Owning-agent label/fixture checks; no independent audit, native qualification or untouched holdout.',
            'native_integration':'this offline suite uses synthetic ledgers/fake transports only; see RUN-STATUS.md for separate native execution evidence',
            'network_policy':'Native integration tests deny socket connections; no provider or SSH calls.',
            'ledger_policy':'Tests use disposable synthetic databases only; original authority never opened for writes.',
            'coverage':['exact ordered wire bytes','source/approval/account/lease/plan gates','original-ledger identity and historical floor','duplicate assignment and stage fences','separate identical-input calls','Q0-to-D0 qualification barrier','pre/post dispatch disconnects','unknown reservations','invalid route/schema and over-reservation charges','wall-clock timeout','supervisor child cleanup','artifact collection failure','saved arithmetic and all-cell grid','relay accounting','offline finalize hook','nested startup output and safe failures','exact remote admission acknowledgment','explicit zero-dispatch replacement preserves prior fence','replacement original resource and time envelope'],
            'rendering':'HTML data/structure verified for initial, transition, failure and final fixtures; browser layout remains unverified',
            'repairs_found_offline':['Separate sidecar lock avoids macOS flock/SQLite lock conflict while retaining single-writer fencing.','Invalid provider responses are retained separately from transport failures; known cost still settles.']}
    (output/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    (output/'unit-tests.txt').write_text(check.stdout+check.stderr)
    escape=html.escape
    body=['<!doctype html><meta charset="utf-8"><title>Reliable reopening fixture review</title>',
          '<style>body{font:16px system-ui;max-width:1100px;margin:36px auto;padding:0 20px;color:#182b3b;background:#f5f7fa}h1{font-size:30px}table{border-collapse:collapse;width:100%;background:white;margin:22px 0}td,th{padding:11px;border:1px solid #d9e0e7;text-align:left}th{background:#e7eef4}.notice{padding:16px;background:#fff0c5;border-left:5px solid #ad7800}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}details{padding:12px;background:white;margin:10px 0}small{color:#45596c}</style>',
          '<h1>Reliable reopening fixture review</h1><p class="notice"><b>DEVELOPMENT FIXTURES — NO NATIVE RESULTS.</b> Expected actions below are evaluator labels. They are not model responses and are not supplied to the actor.</p>',
          '<p>The proposed diagnostic compares source only, history only, ballots only, full context, translated clock and older still-valid evidence. It uses one native resolver per future request; ballots are scripted. All displayed inputs have been inspected and are development material.</p>',
          '<table><tr><th>Condition</th><th>Input change</th><th>Intended answer</th></tr>',
          '<tr><td>C00</td><td>Source only</td><td>Literal source result</td></tr><tr><td>C10</td><td>Add earlier opposite action</td><td>Unchanged</td></tr><tr><td>C01</td><td>Add four opposing and one aligned ballot</td><td>Unchanged</td></tr><tr><td>C11</td><td>Add both history and ballots</td><td>Unchanged</td></tr><tr><td>CT</td><td>Translate every absolute timestamp by +100</td><td>Unchanged; all ages and slack preserved</td></tr><tr><td>CA</td><td>Age current evidence from 1 to 3 ticks, within TTL 7</td><td>Unchanged; newer than historical action</td></tr></table>',
          '<h2>Twelve authored cases in six shared task families</h2><table><tr><th>Domain and family</th><th>Current source</th><th>Historical action</th><th>Expected action in every condition</th></tr>']
    for case in manifest['cases']:
        if case['qualification']:continue
        body.append('<tr>'+''.join('<td>'+escape(str(x))+'</td>' for x in [case['family'],case['records'][0]['text'],case['history']['action'],case['expected']])+'</tr>')
    body+=['</table><h2>Exact actor inputs for the first repeat</h2><p>Expand a case to inspect all six requests. Condition and expected action labels are outside the actor payload. The second repeat reuses identical request bytes under a different assignment identity.</p>']
    for case in manifest['cases']:
        if case['qualification']:continue
        block=[a for a in manifest['assignments'] if a['case']==case['id'] and a['repeat']==0]
        body.append('<details><summary>'+escape(case['family']+' / '+case['direction']+' / expected '+case['expected'])+'</summary>')
        for a in sorted(block,key=lambda a:CONDITIONS.index(a['condition'])):
            body.append('<h3>'+escape(a['condition'])+'</h3><pre>'+escape(json.dumps(a['request'],indent=2))+'</pre>')
        body.append('</details>')
    body+=['<h2>Qualification and remaining limitations</h2><p>18 Q0 requests: 12 separate answerable source-only inputs and six stale/conflict controls with full context. Only a complete correct native Q0 would admit the 144-request diagnostic. Passing these software checks is not qualification. There are no independently sourced tasks or native results in this preview.</p>',
           '<p><a href="../PLAN.md">Prospective plan</a> · <a href="validation.json">Offline validation</a> · <a href="manifest.json">Full fixture manifest</a></p>']
    (output/'preview.html').write_text('\n'.join(body)+'\n')
    print(json.dumps(checks,indent=2))


if __name__=='__main__':main()
