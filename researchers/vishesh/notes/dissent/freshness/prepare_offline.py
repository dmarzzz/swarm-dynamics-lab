"""Rebuild development evidence with offline transports; never dispatch or open credentials."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
from cases import BASE,build,reference,gate
from native_gates import prepare,validate_packet,validate_review,read,sources

def main():
    p=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(BASE/'tests'),'-v'],capture_output=True,text=True)
    if p.returncode:print(p.stdout+p.stderr);raise SystemExit(p.returncode)
    manifest=build();packet=prepare('F0');validate_packet(packet);validate_review(read(BASE/'DIAGNOSTIC-REVIEW.json'))
    out=BASE/'offline';out.mkdir(exist_ok=True)
    for name,value in [('manifest.json',manifest)]: (out/name).write_text(json.dumps(value,indent=2)+'\n')
    n=int(re.search(r'Ran (\d+) tests',p.stderr).group(1));a=manifest['assignments']
    record={'kind':'offline software evidence; synthetic transports, no native calls','tests_passed':n,'native_calls':0,'requests':len(a),'semantic_roots':len({x['root'] for x in a}),'task_age_cases':len({x['case'] for x in a}),
        'literal_reference_correct':sum(reference(x['request'])==x['expected'] for x in a),'gate_plus_literal_correct':sum((gate(x['request'])['action'] or reference(gate(x['request'])['request']))==x['expected'] for x in a),
        'gate_without_model_deferrals':sum(not gate(x['request'])['model_required'] for x in a),'maximum_request_bytes':max(len(json.dumps(x['request'],separators=(',',':')).encode()) for x in a),
        'source_hashes':sources(),'manifest_sha256':hashlib.sha256((out/'manifest.json').read_bytes()).hexdigest(),
        'boundary_corpus':'54 generated cases on a public test seed check inside/at/outside TTL, future, wrong scope/revision, stale contradiction/current conflict/missing evidence; separate private reserve created after freeze.',
        'original_ledger':'untouched by tests; synthetic disposable database only','scope':'Owning-agent verification, not independent audit or native qualification.'}
    (out/'validation.json').write_text(json.dumps(record,indent=2)+'\n');(out/'unit-tests.txt').write_text(p.stdout+p.stderr)
    print(json.dumps({k:v for k,v in record.items() if k!='source_hashes'},indent=2))
if __name__=='__main__':main()
