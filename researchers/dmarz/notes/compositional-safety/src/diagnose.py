"""Paired, fixed one-decision probes on retained failures, never qualification."""
import argparse
import hashlib
import json
import random
import time
import urllib.request
from PIL import Image, ImageDraw
import common
from contract import clarify
from provider import Anthropic, CallFailure, Ledger
from render import font


def cases():
    path = common.ROOT/'results/q0-004'
    hashes = json.loads((path/'artifact-hashes.json').read_text())
    assert hashlib.sha256((path/'episodes.jsonl').read_bytes()).hexdigest() == hashes['episodes.jsonl']
    rows = {r['episode_id']: r for r in map(json.loads, (path/'episodes.jsonl').read_text().splitlines())}
    selected = common.design()['diagnostics']['i0-003']['cases']
    result = []
    for index, item in enumerate(selected):
        row = rows[item['episode']]
        observation = row['trace'][item['step']]['observation']
        allowed = observation['actions']
        expected = item.get('expected') or [a for a in allowed if a not in ('inspect', 'wait', 'message')]
        assert expected and set(expected) <= set(allowed)
        result.append(dict(case=index, source_episode=item['episode'], step=item['step'], arm=row['arm'], packet=observation, expected=expected))
    return result


def picture(rows, items):
    im = Image.new('RGB',(1600,900),'#101823'); draw = ImageDraw.Draw(im)
    draw.text((45,30),'INTERFACE DIAGNOSTIC / ONE DECISION PER CELL',font=font(29),fill='#edf4ff')
    draw.text((45,85),'Original packet vs explicit execution contract; same model, policy and action menu',font=font(22),fill='#bdccdf')
    draw.text((45,125),'Blue: advancing action | Gray: no progress | Red: invalid/refused | Blank: not called yet',font=font(19),fill='#bdccdf')
    for j,condition in enumerate(('original','clarified')):
        draw.text((540+j*500,170),condition,font=font(23),fill='#edf4ff')
    for item in items:
        y=220+item['case']*69
        label=item['source_episode'].replace('q0-004/','')+' / turn '+str(item['step'])
        draw.text((45,y+10),label,font=font(20),fill='#edf4ff')
        for j,condition in enumerate(('original','clarified')):
            r=next((r for r in rows if r['case']==item['case'] and r['condition']==condition),None)
            color='#273341' if r is None else '#d95364' if not r['valid'] else '#397dbe' if r['advancing'] else '#546778'
            x=540+j*500;draw.rounded_rectangle((x,y,x+470,y+51),radius=4,fill=color)
            if r:
                label=r.get('answer',{}).get('action',r.get('reason','unknown'))
                draw.text((x+10,y+14),label[:42],font=font(17),fill='white')
    draw.text((45,830),'Reused development observations. No episode is executed and no qualification pass is claimed.',font=font(20),fill='#bdccdf')
    return im


def execute(attempt):
    import swarm_report as sr
    if attempt != 'i0-003': raise ValueError('unregistered_diagnostic')
    commit=common.frozen(attempt);items=cases()
    out=common.ROOT/'results'/attempt;out.mkdir(parents=True,exist_ok=False)
    assigned=[dict(case=i['case'],condition=c) for i in items for c in ('original','clarified')]
    random.Random('i0-003-paired-order').shuffle(assigned)
    common.dump(out/'manifest.json',dict(attempt=attempt,stage='I0',parent_attempt='q0-004',commit=commit,hashes=common.hashes(),assignments=assigned,cases=items))
    ledger=Ledger(common.ROOT/'accounting/study.jsonl');before=ledger.transact();rows=[];frames=[picture([],items)];started=time.monotonic()
    with sr.start(common.EXP,params=dict(stage='I0',kind='interface-diagnostic',attempt=attempt),run=f'{common.EXP}/{attempt}-diagnostic') as run:
        for assignment in assigned:
            item=items[assignment['case']];condition=assignment['condition']
            packet=item['packet'] if condition=='original' else clarify(item['packet'],item['arm'])
            call_id=f"{attempt}/{item['case']}/{condition}"
            def capture(req, timeout):
                common.dump(out/f"request-{item['case']}-{condition}.json",json.loads(req.data))
                return urllib.request.urlopen(req,timeout=timeout)
            try:
                if time.monotonic()-started>1800: raise CallFailure('diagnostic_time_limit')
                answer,usage=Anthropic(ledger,opener=capture).call(packet,call_id)
                row=dict(**assignment,valid=True,answer=answer,usage=usage,advancing=answer['action'] in item['expected'])
            except CallFailure as exc:
                row=dict(**assignment,valid=False,reason=exc.category,usage=exc.accounting,advancing=False)
            rows.append(row);common.dump(out/'results.json',rows)
            frames.append(picture(rows,items));frames[-1].save(out/'live.png');run.artifact(out/'live.png','live.png')
            current=ledger.transact()
            run.progress(len(rows),len(assigned),model_calls=current['attempted_calls']-before['attempted_calls'],api_cost_usd=current['actual_usd']-before['actual_usd'])
        after=ledger.transact()
        summary={c:dict(assigned=len(items),valid=sum(r['valid'] for r in rows if r['condition']==c),advancing=sum(r['advancing'] for r in rows if r['condition']==c)) for c in ('original','clarified')}
        summary.update(qualification_pass=False,diagnostic_pass=summary['clarified']['valid']==len(items) and summary['clarified']['advancing']==len(items),accounting={k:after[k]-before[k] for k in after},study_accounting=after,elapsed_seconds=time.monotonic()-started)
        common.dump(out/'summary.json',summary)
        frames[-1].save(out/'final_frame.png');frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=600,loop=0)
        common.dump(out/'artifact-hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()})
        for path in sorted(out.iterdir()): run.artifact(path,path.name)
        run.done(model_calls=summary['accounting']['attempted_calls'],api_cost_usd=summary['accounting']['actual_usd'],message=f"Paired interface diagnostic complete; diagnostic_pass={summary['diagnostic_pass']}; not qualification.")
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('attempt');execute(parser.parse_args().attempt)
