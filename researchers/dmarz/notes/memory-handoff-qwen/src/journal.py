"""Durable append-only journal and the source-to-successor replay page.

Copied from discussion-dose bench_v3 (swarm-lab commit ce2c87fe): `Journal` and `read_events` from
src/bench_v3/journal.py (hash-chained events, fsync per event; a lock is added because four calls
are in flight), and the self-contained replay page from src/bench_v3/replay_view.py, with the
stages of this study: what the sources really say, the predecessor's notes, what the handoff
added, the successor's answer, the score. Untrusted model strings are never written as HTML.
"""
import copy
import hashlib
import json
import os
import threading


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class Journal:
    def __init__(self, path=None):
        self.events = []
        self.handle = open(path, 'x', encoding='utf-8') if path is not None else None
        self.lock = threading.Lock()

    def emit(self, kind, **data):
        with self.lock:
            event = {'seq': len(self.events), 'previous': self.events[-1]['hash'] if self.events else '0' * 64,
                     'kind': kind, **copy.deepcopy(data)}
            event['hash'] = digest(event)
            if self.handle:
                self.handle.write(json.dumps(event, sort_keys=True) + '\n')
                self.handle.flush(); os.fsync(self.handle.fileno())
            self.events.append(event)
            return event

    def close(self):
        if self.handle: self.handle.close()


def read_events(lines):
    """Parse and check a journal: sequence numbers, the hash chain and each event's own hash."""
    events = []; previous = '0' * 64
    for line in lines:
        if not line.strip(): continue
        event = json.loads(line)
        if event.get('seq') != len(events) or event.get('previous') != previous:
            raise ValueError('journal sequence mismatch')
        if digest({k: v for k, v in event.items() if k != 'hash'}) != event.get('hash'):
            raise ValueError('journal hash mismatch')
        events.append(event); previous = event['hash']
    return events


def call_ledger_complete(events):
    """Every call that started has exactly one terminal event (a response or a provider failure)."""
    starts = [e['call_id'] for e in events if e['kind'] == 'call_start']
    ends = [e['call_id'] for e in events if e['kind'] in ('call_response', 'provider_failure')]
    return len(starts) == len(set(starts)) and sorted(starts) == sorted(ends)


PAGE = '''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Memory handoff: source-to-successor replay</title>
<style>body{font:15px ui-monospace,SFMono-Regular,Menlo,monospace;margin:24px auto;max-width:1100px;padding:0 16px;background:#f5f4ef;color:#1d2126}h1{font-size:20px}select,button{font:inherit;padding:6px;margin:6px 6px 6px 0}input{width:100%}#visual{background:#fff;padding:18px;border:1px solid #d8d8d0;margin:12px 0;overflow:auto}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:6px 10px;border-bottom:1px solid #e4e4dc;vertical-align:top}th{color:#5a6068;font-weight:600}h2{margin-top:0;font-size:16px}p.note{color:#5a6068}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>
<h1>Memory handoff: source-to-successor replay</h1><p class="note">LABEL One assignment at a time: what the sources really say, what the predecessor noted, what the handoff added, what the successor answered, how it was scored. Evaluator labels shown here never enter a successor's message.</p>
<label>Assignment <select id="unit"></select></label><button id="back">Previous</button><button id="next">Next</button><button id="play">Play</button><input id="cursor" type="range" aria-label="Replay position" min="0" max="4" step="1" value="0"><p id="summary"></p><section id="visual"></section>
<script id="data" type="application/json">PAYLOAD</script><script>
const data=JSON.parse(document.getElementById('data').textContent),select=document.getElementById('unit'),slider=document.getElementById('cursor');
const names=['1 Sources (evaluator view)','2 Predecessor notes','3 Handoff','4 Successor answer','5 Score'];let timer=null;
for(const u of data.units){const o=document.createElement('option');o.value=u.id;o.textContent=u.id+' ['+u.status+']';select.append(o)}
function add(tag,text,parent){const n=document.createElement(tag);n.textContent=text;(parent||document.getElementById('visual')).append(n);return n}
function table(headers,rows){const t=document.createElement('table');document.getElementById('visual').append(t);const h=document.createElement('tr');t.append(h);headers.forEach(x=>add('th',x,h));rows.forEach(r=>{const tr=document.createElement('tr');t.append(tr);r.forEach(v=>add('td',v===null||v===undefined?'-':typeof v==='object'?JSON.stringify(v):String(v),tr))})}
function show(){const u=data.units.find(x=>x.id===select.value),step=Number(slider.value),v=document.getElementById('visual');v.replaceChildren();if(!u)return;
document.getElementById('summary').textContent=names[step]+' / root '+u.root+' / '+u.family+' / memory: '+u.state+' / handoff: '+u.policy;
if(step===0){add('h2','What the source records really hold');add('p','Hidden truth for '+u.key+': '+u.truth+' (answer '+u.truth_answer+'). The successor never sees this line.');table(['Record','Origin','Version','States'],u.store.map(r=>[r.id,r.origin,r.version,r.facts]))}
else if(step===1){add('h2','What the predecessor wrote down');table(['Fact','Claimed value','Cites'],u.notes.map(n=>[n.key,n.value,n.sources.join(', ')]))}
else if(step===2){add('h2','What the handoff put in the successor\\'s message');add('p','Notes passed on: '+u.packet.inherited_memory.length+'. Registry lookups: '+u.retrieval.registry_lookups+'. Records retrieved: '+u.retrieval.records_retrieved+'. Bytes added: '+u.retrieval.bytes+'. Lookup time: '+(u.retrieval.seconds===undefined?'not measured':(u.retrieval.seconds*1000).toFixed(3)+' ms')+'.');if(u.packet.source_registry.length)table(['Registry entry','Origin','Version','Current version'],u.packet.source_registry.map(e=>[e.id,e.origin,e.version,e.current_version]));if(u.packet.retrieved_records.length)table(['Retrieved record','Origin','Version','States'],u.packet.retrieved_records.map(r=>[r.id,r.origin,r.version,r.facts]));if(!u.packet.inherited_memory.length)add('p','Nothing was inherited and nothing was looked up.')}
else if(step===3){add('h2','What the successor answered');if(u.status==='completed'){add('p','Value: '+(u.answer.value===null?'null (unresolved)':u.answer.value));add('p','Cited: '+(u.answer.sources.length?u.answer.sources.join(', '):'nothing'))}else if(u.status==='failed'){add('p','No valid answer: '+u.error+'. The call stays in its cell with unknown outcome.')}else{add('p','Not started. The assignment stays in its cell with unknown outcome.')}}
else{add('h2','Score');if(u.status==='completed'){table(['Measure','Value'],[['Outcome',u.evaluation.outcome],['Reference answer (from the visible message only)',u.reference.value===null?'null':u.reference.value],['Hidden-truth answer',u.truth_answer],['Supported by the message',u.evaluation.supported],['Correct against hidden truth',u.evaluation.correct],['Inherited error',u.evaluation.inherited_error],['Citations valid',u.evaluation.citation_valid]])}else add('p','Unknown outcome: bounded between 0 and 1 in every analysis.')}}
function move(d){slider.value=Math.min(4,Math.max(0,Number(slider.value)+d));show()}
select.onchange=()=>{slider.value=0;show()};slider.oninput=show;document.getElementById('back').onclick=()=>move(-1);document.getElementById('next').onclick=()=>move(1);
document.getElementById('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;document.getElementById('play').textContent='Play'}else{if(slider.value==='4')slider.value=0;show();timer=setInterval(()=>{move(1);if(slider.value==='4'){clearInterval(timer);timer=null;document.getElementById('play').textContent='Play'}},1200);document.getElementById('play').textContent='Pause'}};show();
</script>'''


def replay_html(units, destination, scripted):
    """`units`: one dict per assignment with id, root, family, state, policy, key, truth, truth_answer,
    store, notes, packet, retrieval, status, answer, evaluation, reference, error."""
    payload = json.dumps({'units': units}, sort_keys=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    label = 'SCRIPTED - NOT MODEL EVIDENCE.' if scripted else 'Recorded model answers.'
    destination.write_text(PAGE.replace('LABEL', label).replace('PAYLOAD', payload), encoding='utf-8')
