"""Saved-data reconciliation, transparent grid and qualification gate; no network."""
import hashlib
import html
import json
import os
from pathlib import Path
from cases import build, digest, score, CONDITIONS
from native_gates import wire, sha, read, require, SNAPSHOT


def save(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:
        json.dump(value, f, indent=2, allow_nan=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)
    fd = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


class Events:
    def __init__(self, path):
        self.path = Path(path); self.seq = 0; self.prev = '0'*64
        self.file = self.path.open('x')

    def add(self, kind, **fields):
        row = dict(seq=self.seq, prev=self.prev, kind=kind, **fields)
        row['sha256'] = digest(row)
        self.file.write(json.dumps(row,allow_nan=False)+'\n'); self.file.flush(); os.fsync(self.file.fileno())
        self.seq += 1; self.prev = row['sha256']
        return row

    def close(self): self.file.close()


def check_events(path):
    rows = []; prev = '0'*64
    for i,line in enumerate(Path(path).read_text().splitlines()):
        row = json.loads(line); expected = row.pop('sha256')
        require(row['seq'] == i and row['prev'] == prev and digest(row) == expected, 'event_chain')
        row['sha256'] = expected; prev = expected; rows.append(row)
    return rows


def inventory(directory):
    return {p.name: sha(p) for p in sorted(Path(directory).iterdir())
            if p.is_file() and p.name != 'bundle.json' and not p.name.endswith('.tmp')}


def reconcile(packet, rows):
    manifest=build()
    require(wire(packet['assignments'])==wire([a for a in manifest['assignments'] if a['stage']==packet['stage']]),'scoring_assignment_binding')
    scored = score(manifest,rows,packet['stage'])
    require(len(rows) == len(packet['assignments']), 'all_assigned_required')
    observed = {r['id']:r for r in rows}
    require([r['id'] for r in rows] == [a['id'] for a in packet['assignments']], 'outcome_order')
    from native_budget import validate
    for a in packet['assignments']:
        r = observed[a['id']]
        if r['status'] == 'completed':
            checked = validate(r['visible_response'], a['request'], SNAPSHOT)
            require(checked == r['checked'] and checked['action'] == r['action']
                    and checked['input_tokens'] <= 32000 and 0 <= r['settled_nano'] <= 1_344_000
                    and r['settled_nano'] == __import__('math').ceil(checked['cost_usd']*1e9), 'response_binding')
    return scored


def render(packet, rows, directory, label):
    directory = Path(directory)
    esc = lambda x: html.escape(str(x))
    observed = {r['id']:r for r in rows}
    body = ['<!doctype html><meta charset="utf-8"><title>RD7 decision grid</title>',
        '<style>body{font:15px system-ui;margin:32px;color:#182b3b;background:#f7fafb}table{border-collapse:collapse;width:100%;margin:24px 0}td,th{padding:9px;border:1px solid #ced6df;text-align:left}.correct{background:#d1efdc}.wrong{background:#ffe0c0}.invalid,.failed{background:#ffdce3}.unstarted{background:#e7ebf0}pre{white-space:pre-wrap}details{margin:12px 0}</style>',
        '<h1>RD7 '+esc(packet['stage'])+' decision grid</h1><p><b>'+esc(label)+'</b></p>',
        '<p>Green: observed correct; orange: observed wrong; pink: invalid/failed; gray: unstarted. Expected labels are evaluator-only. Repeated slots are dependent observations, not independent cases.</p>',
        '<table id="grid"><tr><th>Case</th>']
    columns = [(c,0) for c in CONDITIONS]
    body += ['<th>'+esc(c)+' / '+str(r+1)+'</th>' for c,r in columns]; body.append('</tr>')
    for case in sorted({a['case'] for a in packet['assignments']}):
        body.append('<tr><th>'+esc(case)+'</th>')
        for c,r in columns:
            a = next((a for a in packet['assignments'] if (a['case'],a['condition'],a['repeat'])==(case,c,r)),None)
            if a is None: body.append('<td>Not assigned</td>'); continue
            out=observed[a['id']]; status=out['status']; color=status
            if status=='completed': color='correct' if out['action']==a['expected'] else 'wrong'
            body.append('<td class="'+color+'" data-id="'+esc(a['id'])+'"><a href="#'+esc(a['id'])+'">'+esc(out['action'] or status)+'</a><br>expected '+esc(a['expected'])+'</td>')
        body.append('</tr>')
    body.append('</table><h2>Dispatch order and cost</h2><table id="dispatch"><tr><th>Slot</th><th>Request</th><th>Status</th><th>Latency (s)</th><th>Settled nanodollars</th><th>Reservation state</th></tr>')
    for i,a in enumerate(packet['assignments']):
        r=observed[a['id']]
        body.append('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in (i+1,a['id'],r['status'],r.get('latency_seconds','unknown'),r.get('settled_nano','unknown'),r.get('reservation','none')) )+'</tr>')
    body.append('</table><h2>Exact inputs and visible responses</h2>')
    for a in packet['assignments']:
        body.append('<details id="'+esc(a['id'])+'"><summary>'+esc(a['id'])+'</summary><pre>'+esc(json.dumps({'actor_request':a['request'],'outcome':observed[a['id']]},indent=2))+'</pre></details>')
    (directory/'replay.html').write_text('\n'.join(body)+'\n')


def finish_bundle(directory, packet, rows, execution, *, mode):
    require(mode in ('native','synthetic-offline'), 'bundle_mode')
    directory = Path(directory)
    save(directory/'outcomes.json',rows)
    scored = reconcile(packet,rows)
    save(directory/'summary.json',scored)
    save(directory/'execution.json',dict(execution,mode=mode,scientific_review='required',qualification='unreviewed',
                                       cost_status='relay_reconciliation_required',allocation_release='not_verified'))
    render(packet,rows,directory,'NATIVE RESPONSES — provenance requires relay reconciliation' if mode=='native' else 'SYNTHETIC OFFLINE TEST — NO NATIVE EVIDENCE')
    files = inventory(directory)
    save(directory/'bundle.json',{'schema':'rd7-bundle-v1','files':files,'sha256':digest(files)})
    return scored


def audit_bundle(directory, expected):
    directory=Path(directory); bundle=read(directory/'bundle.json')
    require(bundle['sha256']==expected and inventory(directory)==bundle['files'] and digest(bundle['files'])==expected, 'bundle_integrity')
    packet=read(directory/'packet.json'); rows=read(directory/'outcomes.json')
    require(reconcile(packet,rows)==read(directory/'summary.json'), 'score_replay')
    events=check_events(directory/'events.jsonl')
    require(events and events[0]['kind']=='assignment' and events[0]['packet_sha256']==digest(packet), 'event_packet')
    terminal=[e for e in events if e['kind']=='terminal']
    require(len(terminal)==len(rows) and [e['id'] for e in terminal]==[r['id'] for r in rows]
            and all(e['outcome_sha256']==digest(r) for e,r in zip(terminal,rows)), 'terminal_reconciliation')
    return packet, rows


def reconcile_accounting(packet, rows, accounting, relay_events):
    """Cross-check worker evidence against the original relay export, without retry."""
    require(accounting['packet_sha256']==digest(packet),'accounting_packet')
    calls={c['id']:c for c in accounting['calls']}
    allowed={a['id']:a for a in packet['assignments']}
    require(len(calls)==len(accounting['calls']) and set(calls)<=set(allowed),'accounting_identity')
    events=check_events(relay_events)
    require(events and events[0]['kind']=='relay_start' and events[0]['packet_sha256']==digest(packet), 'relay_event_packet')
    reservations=[e for e in events if e['kind']=='reservation']
    require([e['id'] for e in reservations]==list(calls), 'reservation_event_reconciliation')
    unresolved=[];worker_response_missing=[]
    for r in rows:
        c=calls.get(r['id'])
        if r['status']=='completed':
            require(c is not None and c['status']=='completed' and c['response']['checked']==r['checked']
                    and c['response']['visible_response']==r['visible_response']
                    and c['actual_nano']==r['settled_nano'], 'worker_relay_mismatch')
        if r['status']=='unstarted': require(c is None,'unstarted_was_dispatched')
        if c and c['actual_nano'] is None: unresolved.append(r['id'])
        if c and c['status']=='completed' and r['status']!='completed':worker_response_missing.append(r['id'])
    return {'ledger_calls':len(calls),'assigned':len(rows),
        'stage_committed_nano':sum(c['actual_nano'] if c['actual_nano'] is not None else c['reserved_nano'] for c in calls.values()),
        'unresolved_reservations':unresolved,'relay_response_missing_from_worker':worker_response_missing,
        'cumulative':accounting['cumulative'],'model_calls':0,
        'note':'Known relay-only answers remain separate from worker scoring; no replayed answer is a new request.'}

