"""Measured charts and observation-time replays, without raw receipt content."""
import json,math,statistics
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from policies import ARMS,MODES,estimate,initial,choose
BG='#0d1424';FG='#eef4ff';MUTED='#9cacc6';COLORS=['#50d9c6','#f2bd60','#9992ff']
def font(n):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
        try:return ImageFont.truetype(p,n)
        except OSError:pass
    return ImageFont.load_default()
def canvas(title,subtitle):
    im=Image.new('RGB',(1600,960),BG);d=ImageDraw.Draw(im);d.text((50,28),title,font=font(38),fill=FG);d.text((50,86),subtitle,font=font(21),fill=MUTED);return im,d
def write(d,xy,t,n=22,c=FG):d.text(xy,t,font=font(n),fill=c)
def summary(blocks):
    return {arm:{k:sum(b['arms'][arm]['metrics'][k] for b in blocks)/len(blocks) for k in ['quality','regret','checks','utility_at_002','within_2pp_oracle']}|{'n':len(blocks),'total_exact_n':sum(b['arms'][arm]['metrics']['total_field_exact'] is not None for b in blocks),'total_exact':sum(b['arms'][arm]['metrics']['total_field_exact'] is True for b in blocks),'logical_calls':sum(b['arms'][arm]['logical_calls'] for b in blocks)} for arm in ARMS}
def render_overview(blocks,out,stage):
    s=summary(blocks);(out/'summary.json').write_text(json.dumps(s,indent=2))
    im,d=canvas('Antsy | does verification earn its cost?',f'{stage}: {len(blocks)} paired real receipts | annotated-token recall | ideal regional QA, at most two checks')
    write(d,(50,145),'Policy',24);write(d,(390,145),'Mean quality (0-100%)',24);write(d,(940,145),'Oracle gap',24);write(d,(1190,145),'QA checks / receipt',24)
    for j,arm in enumerate(ARMS):
        y=213+j*77;a=s[arm];write(d,(50,y),arm)
        d.rounded_rectangle((390,y,890,y+27),radius=5,fill='#1d2a41');d.rounded_rectangle((390,y,390+500*a['quality'],y+27),radius=5,fill=COLORS[0] if 'swarm' not in arm else COLORS[2]);write(d,(400,y+31),f"{100*a['quality']:.1f}%",18)
        write(d,(950,y),f"{100*a['regret']:.1f} pp");write(d,(1210,y),f"{a['checks']:.2f}")
    write(d,(50,806),'What this tests: selecting useful checks and deciding when to stop.',25)
    write(d,(50,855),'All configurations were actually run; the agents never see hidden scores before committing.',21,MUTED)
    write(d,(50,893),'One checkpoint per backend, five role prompts; votes are not independent evidence. CORD / CC BY 4.0.',20,MUTED)
    im.save(out/'final_frame.png')
    im,d=canvas('Antsy | how much room is there to improve?',f'{stage}: each dot is one receipt; all three configurations run on the same image')
    x0,y0,w,h=145,180,720,610
    d.line((x0,y0,x0,y0+h,x0+w,y0+h),fill=MUTED,width=2)
    for q in [0,.25,.5,.75,1]:
        y=y0+h*(1-q);d.line((x0,y,x0+w,y),fill='#263249');write(d,(70,y-12),f'{q:.2f}',18,MUTED);write(d,(x0+w*q-15,y0+h+15),f'{q:.2f}',18,MUTED)
    d.line((x0,y0+h,x0+w,y0),fill=MUTED,width=2)
    for b in blocks:
        x=b['arms']['best-fixed']['metrics']['quality'];y=max(b['mode_scores'].values());d.ellipse((x0+w*x-5,y0+h*(1-y)-5,x0+w*x+5,y0+h*(1-y)+5),fill=COLORS[0])
    write(d,(260,853),'Best fixed configuration: actual recall');write(d,(50,130),'Oracle recall',20)
    oracle=sum(max(b['mode_scores'].values()) for b in blocks)/len(blocks)
    write(d,(930,205),f'Oracle mean: {oracle:.1%}',27)
    write(d,(930,260),'Above diagonal = routing opportunity',22)
    write(d,(930,310),'The oracle sees every hidden score.',21,MUTED)
    write(d,(930,348),'It is a ceiling, not a usable agent.',21,MUTED)
    for j,arm in enumerate(['confidence-only','decision-focused','single-agent','swarm-adaptive']):
        wins=sum(b['arms'][arm]['metrics']['quality']>b['arms']['best-fixed']['metrics']['quality']+1e-9 for b in blocks)
        loses=sum(b['arms'][arm]['metrics']['quality']<b['arms']['best-fixed']['metrics']['quality']-1e-9 for b in blocks)
        write(d,(930,435+j*75),arm,23);write(d,(930,465+j*75),f'{wins} better / {loses} worse than fixed',20,MUTED)
    im.save(out/'routing_headroom.png')

def replay(block,arm,out):
    result=block['arms'][arm];frames=[];events=result['events']
    for index in range(len(events)+1):
        final=index==len(events)
        if final:
            if not events:continue
            board=dict(events[-1]['before']);board['checks']=events[-1]['after_checks']
        else:board=events[index]['before']
        im,d=canvas(f"Antsy | receipt {block['id']:03} | {arm}", 'COMMITTED: evaluator truth now revealed' if final else f'Decision {index+1}: only observed confidence and purchased checks are visible')
        for j,m in enumerate(MODES):
            y=180+j*135;est=estimate(board,m);write(d,(55,y),f'Configuration {m}',26)
            d.rounded_rectangle((365,y,965,y+34),radius=5,fill='#1d2a41');d.rectangle((365,y,365+600*est,y+34),fill=COLORS[j]);write(d,(365,y+42),f'Estimated quality {est:.2f}',22)
            if final:write(d,(1040,y),f"Actual {block['mode_scores'][m]:.2f}",28,COLORS[j])
            else:write(d,(1040,y),'Actual: hidden',24,MUTED)
        write(d,(55,602),f"Paid checks used: {len(board['checks'])}/2 | current leader: {choose(board)}",26)
        for j,c in enumerate(board['checks']):
            q='no target text' if c['quality'] is None else f"recall {c['quality']:.2f}"
            write(d,(55,652+j*39),f"QA: {c['mode']}, region {c['region']} -> {q}",23)
        if final:write(d,(55,755),f"Selected {result['choice']} | oracle gap {100*result['metrics']['regret']:.1f} pp",29)
        else:write(d,(55,755),'Votes this step: '+', '.join(events[index]['votes']),25)
        write(d,(55,824),'Regions: top / middle / bottom thirds. QA returns reference-based recall for one region.',21,MUTED)
        write(d,(55,865),'Estimates average region scores; this approximation can misrank whole receipts.',21,MUTED)
        write(d,(55,906),'Measured events only. This replay shows decisions, not model internal reasoning.',20,MUTED)
        frames.append(im)
    if frames:frames[0].save(out/f"receipt-{block['id']:03}-{arm}.gif",save_all=True,append_images=frames[1:],duration=[1600]*len(frames),loop=0)

def render_all(blocks,out,stage):
    render_overview(blocks,out,stage)
    for b in blocks[:3]:
        for arm in ['single-agent','swarm-adaptive']:replay(b,arm,out)
