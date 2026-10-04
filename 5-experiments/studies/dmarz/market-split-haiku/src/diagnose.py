#!/usr/bin/env python3
"""Two bounded output-headroom diagnostics on preserved failed observations."""
import argparse,json,os
from PIL import Image,ImageDraw,ImageFont
from matplotlib import font_manager
import common
from provider import Anthropic,Ledger,CallFailure

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--attempt',required=True);a=ap.parse_args();common.frozen(a.attempt)
    import swarm_report as sr
    if any(r['params'].get('attempt_id')==a.attempt for r in sr.runs(common.EXP,limit=500)):raise ValueError('duplicate_attempt')
    fixtures=json.loads((common.ROOT/'src/truncation-fixtures.json').read_text());assert len(fixtures)==2
    out=common.ROOT/'results'/a.attempt;out.mkdir(parents=True,exist_ok=False)
    client=Anthropic(Ledger('/srv/swarm/market-split-haiku/accounting/ledger.jsonl'));rows=[]
    params={'stage':'D0','kind':'diagnostic','attempt_id':a.attempt,'parent_attempt':'s1-001','model':common.design()['model'],'code':common.git('rev-parse','HEAD'),**common.hashes()}
    with sr.start(common.EXP,common.EXP+'/'+a.attempt,params=params) as run:
        for i,fixture in enumerate(fixtures):
            row={**fixture,'call_id':f'{a.attempt}:truncation-{i}'}
            try:
                action,account=client.call(row['observation'],row['call_id']);row.update(action=action,accounting=account,status='ok')
            except CallFailure as e:row.update(accounting=e.accounting,status=e.category)
            rows.append(row)
            with (out/'calls.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
            run.progress(i+1,len(fixtures),force=True,valid=sum(x['status']=='ok' for x in rows))
        m={'model_calls':sum(x['accounting'].get('attempted',False) for x in rows),'valid':sum(x['status']=='ok' for x in rows),'unpriced_calls':sum(x['accounting'].get('attempted',False) and not x['accounting'].get('usage_reported',False) for x in rows),'api_cost_usd':sum(x['accounting'].get('actual_usd',0) for x in rows)}
        m['diagnostic_pass']=int(m['valid']==2 and not m['unpriced_calls'])
        common.dump(out/'summary.json',{'params':params,'metrics':m,'ledger':client.ledger.transact()})
        im=Image.new('RGB',(1800,1000),'#111b20');draw=ImageDraw.Draw(im);path=font_manager.findfont('DejaVu Sans');title=ImageFont.truetype(path,40);font=ImageFont.truetype(path,29)
        draw.text((70,70),'MARKET SPLIT / OUTPUT HEADROOM DIAGNOSTIC',font=title,fill='#e1e9eb')
        draw.text((70,145),'Preserved failed observations. No discovery or generalization claim.',font=font,fill='#99aaaf')
        for i,row in enumerate(rows):
            ac=row['accounting'];y=300+i*180
            draw.text((70,y),row['source_call_id'],font=font,fill='#e1e9eb')
            draw.text((70,y+60),f"{row['status']} | stop {ac.get('stop_reason','missing')} | output {ac.get('output_tokens','missing')}/8192 | ${ac.get('actual_usd',0):.6f}",font=font,fill='#81d7b5' if row['status']=='ok' else '#e2be75')
        im.save(out/'final_frame.png');receipts={}
        for name in ('calls.jsonl','summary.json','final_frame.png'):
            r=run.artifact(out/name,name)
            if not r or r.get('spooled'):raise RuntimeError('unconfirmed_upload')
            receipts[name]=r['sha256']
        common.dump(out/'upload-receipts.json',receipts)
        if not m['diagnostic_pass']:
            run.fail('Output-headroom diagnostic failed; broader qualification blocked.',**m);raise RuntimeError('diagnostic_failed')
        run.done('Both preserved observations returned legal final actions; fresh qualification still required.',**m)
if __name__=='__main__':main()
