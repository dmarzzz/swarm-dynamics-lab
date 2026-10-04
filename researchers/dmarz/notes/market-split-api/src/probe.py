#!/usr/bin/env python3
"""Stateless mechanics probes; no observations or messages carry into discovery runs."""
import argparse,json,os
from pathlib import Path
from PIL import Image,ImageDraw
import common,sim
from provider import Anthropic,Ledger,CallFailure

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--attempt',required=True);a=ap.parse_args();common.frozen(a.attempt)
    import swarm_report as sr
    if any(r['params'].get('attempt_id')==a.attempt for r in sr.runs(common.EXP,limit=500)):raise ValueError('duplicate_attempt')
    out=common.ROOT/'results'/a.attempt;out.mkdir(parents=True,exist_ok=False)
    d=common.design();client=Anthropic(Ledger('/srv/swarm/market-split-api/accounting/ledger.jsonl'));rows=[]
    params={'stage':'I0','kind':'diagnostic','attempt_id':a.attempt,'model':d['model'],'code':common.git('rev-parse','HEAD'),**common.hashes()}
    with sr.start(common.EXP,common.EXP+'/'+a.attempt,params=params) as run:
        for i,c in enumerate(d['interface_probes']):
            m=sim.task(c['task']);obs=sim.make_observation(m,{'trace':[],'n':c['n'],'cash':d['cfg']['start_cash'],'rival_q':m['rival_capacities']},'none',d['threshold'],d['cfg'])
            obs['interface_check_operation']=c['operation'];item={'fixture':c,'observation':obs,'call_id':f'{a.attempt}:probe-{i}'}
            try:
                action,account=client.call(obs,item['call_id']);item.update(action=action,accounting=account,status='ok' if action['operation']==c['operation'] else 'wrong_operation')
            except CallFailure as e:item.update(status=e.category,accounting=e.accounting)
            rows.append(item)
            with (out/'calls.jsonl').open('a') as f:
                f.write(json.dumps(item)+'\n');f.flush();os.fsync(f.fileno())
            run.progress(i+1,len(d['interface_probes']),force=True,valid=sum(x['status']=='ok' for x in rows))
            if item['status']!='ok':break
        metrics={'probe_calls':len(rows),'valid':sum(x['status']=='ok' for x in rows),'model_calls':sum(x['accounting'].get('attempted',False) for x in rows),'api_cost_usd':sum(x['accounting'].get('actual_usd',0) for x in rows),'unpriced_calls':sum(x['accounting'].get('attempted',False) and not x['accounting'].get('usage_reported') for x in rows)}
        metrics['qualification_pass']=int(metrics['valid']==len(d['interface_probes']))
        common.dump(out/'summary.json',{'params':params,'metrics':metrics})
        im=Image.new('RGB',(1800,1000),'#111b20');draw=ImageDraw.Draw(im)
        from matplotlib import font_manager
        font_path=font_manager.findfont('DejaVu Sans')
        from PIL import ImageFont
        title=ImageFont.truetype(font_path,42);font=ImageFont.truetype(font_path,28)
        draw.text((80,70),'MARKET SPLIT / INTERFACE QUALIFICATION',font=title,fill='#e1e9eb')
        draw.text((80,145),'Mandated mechanics only. Not natural-discovery evidence.',font=font,fill='#99aaaf')
        for i,row in enumerate(rows):
            c=row['fixture'];act=row.get('action',{});quantities='; '.join('('+','.join(f'{x:.3g}' for x in row)+')' for row in act.get('quantities',[]))
            text=f"Task {c['task']} | {c['n']} firms | requested {c['operation']} | {row['status']} | output {quantities or 'missing'}"
            draw.text((80,240+i*88),text,font=font,fill='#81d7b5' if row['status']=='ok' else '#e2be75')
        draw.text((80,850),f"{metrics['valid']}/{len(d['interface_probes'])} valid | {metrics['model_calls']} calls | ${metrics['api_cost_usd']:.6f}",font=font,fill='#e1e9eb');im.save(out/'final_frame.png')
        receipts={}
        for name in ('calls.jsonl','summary.json','final_frame.png'):
            r=run.artifact(out/name,name)
            if not r or r.get('spooled'):raise RuntimeError('unconfirmed_upload')
            receipts[name]=r['sha256']
        common.dump(out/'upload-receipts.json',receipts)
        if not metrics['qualification_pass']:
            run.fail('Interface probe failed; qualification blocked.',**metrics);raise RuntimeError('probe_failed')
        run.done('All stateless action-mechanics probes passed; no strategy lesson enters discovery contexts.',**metrics)
if __name__=='__main__':main()
