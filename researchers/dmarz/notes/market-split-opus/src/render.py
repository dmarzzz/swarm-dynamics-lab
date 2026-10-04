"""Pure trace renderer. Uses no policy inputs, network calls or simulation RNG."""
from __future__ import annotations
import io
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

LABELS = {'neutral_dynamic': 'Neutral agent / firms available', 'neutral_locked': 'Neutral agent / one firm', 'merged': 'Scripted competence reference'}
BG = '#10191c'; FG = '#e3eeee'; MUTED = '#9fafb5'; TEAL = '#6cdbb5'; GOLD = '#f6ba77'


def frame(records, step=None, width=1800):
    first = records[0]; total = first['cfg']['rounds']; step = total if step is None else step
    fig = plt.figure(figsize=(15, 10), dpi=width/15, facecolor=BG)
    fig.text(.04, .953, 'ONE OWNER / MANY FIRMS', color=FG, size=21, weight='bold')
    fig.text(.04, .918, f"{('MODEL PILOT' if first.get('backend')=='anthropic' else 'OFFLINE REHEARSAL')}  ·  {first['world'].upper()} REGULATOR  ·  threshold {first['dose']:.2f}  ·  registration {first['cfg']['registration_fee']:,.0f} credits", color=TEAL, size=11)
    fig.text(.96, .953, f'ROUND {step:02d} / {total:02d}', ha='right', color=FG, size=16, family='monospace')
    fig.text(.04, .880, 'Firm boundaries separate legal entities; teal firms share one owner. Ownership is an evaluator overlay.', color=MUTED, size=10)
    grid = fig.add_gridspec(len(records), 2, left=.05, right=.96, bottom=.10, top=.82, wspace=.16, hspace=.65, width_ratios=[1, 1.25])
    maxq = max(sum(first['market']['capacity'][g:g+1]) + sum(v[g] for v in first['market']['rival_capacities']) for g in range(2))
    for row, rec in enumerate(records):
        ax = fig.add_subplot(grid[row,0]); line = fig.add_subplot(grid[row,1])
        for a in (ax,line):
            a.set_facecolor(BG); a.tick_params(colors=MUTED, labelsize=8)
            for spine in a.spines.values(): spine.set_color('#33464b')
        history = [f for f in rec['trace'] if f['round'] <= step]
        f = history[-1] if history else None
        title = LABELS.get(rec['arm'], rec['arm'])
        if rec.get('backend')=='mock':title=title.replace('Neutral agent','Mock response')
        status = '' if rec['validity']['ok'] else (' · PENDING' if rec['validity'].get('reason') == 'pending' else ' · INVALID')
        ax.set_title(title + status, color=FG, loc='left', size=13, pad=9)
        ax.set_xlim(0,maxq); ax.set_ylim(-.6,1.65); ax.set_yticks([0,1], ['Product A','Product B'])
        ax.set_xlabel('Output (units)', color=MUTED, size=8)
        if f:
            for g in range(2):
                left = 0
                for firm in f['firms']:
                    q = firm['q'][g]; owner = firm['owner']
                    ax.barh(g,q,left=left,height=.45,color=TEAL if owner == 'P' else ('#657c86' if owner == 'R1' else '#9cafb7'),edgecolor=BG,linewidth=2)
                    if q > 2: ax.text(left+q/2,g,firm['id'],ha='center',va='center',color=BG,size=8,weight='bold')
                    left += q
            ax.text(0,1.48,f"{f['firm_count']} owned firms   |   net {f['owner_profit']:,.0f}   |   fines {f['owner_fines']:,.0f} credits",color=FG,size=9)
            if not rec['validity']['ok'] and rec['validity'].get('reason') != 'pending':
                ax.text(.01,.02,f"Stopped after round {len(rec['trace'])}: {rec['validity'].get('reason')}",transform=ax.transAxes,color=GOLD,size=8)
        else:
            ax.text(.05,.45,'No completed observations',transform=ax.transAxes,color=MUTED,size=10)
        line.set_xlim(1,max(2,total));line.set_ylim(0,1)
        line.set_xlabel('Completed round (logical time)',color=MUTED,size=8)
        line.set_ylabel('Concentration (HHI, 0–1)',color=MUTED,size=8)
        line.grid(axis='y',color='#25373d',lw=.5)
        line.axhline(rec['dose'],color=MUTED,ls=':',lw=1)
        for g,color in enumerate((TEAL,GOLD)):
            for field,style in [('firm_hhi','-'),('owner_hhi','--')]:
                ys=[v[field][g] if v[field][g] is not None else float('nan') for v in history]
                line.plot([v['round'] for v in history],ys,style,color=color,lw=1.5,
                          label=f"{'Firm' if field=='firm_hhi' else 'Owner'} {'AB'[g]}")
        for v in history:
            if v['operation']=='register':
                line.axvline(v['round'],color=FG,alpha=.3,lw=.8)
                line.plot(v['round'],.97,marker='v',color=FG,ms=4)
        line.axvline(step,color=FG,alpha=.35,lw=.7)
        if row==0: line.legend(loc='upper right',ncol=2,fontsize=7,facecolor=BG,edgecolor='none',labelcolor=FG)
    fig.text(.04,.045,f"Recorded trace · task {first['task_id']}, seed {first['seed']} · all episodes retained separately · exploratory, not confirmatory",color=MUTED,size=9)
    buf=io.BytesIO();fig.savefig(buf,format='png',facecolor=BG);plt.close(fig);buf.seek(0)
    return Image.open(buf).convert('RGB')


def save_bundle(records, directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    total=records[0]['cfg']['rounds']
    if total > 24: raise ValueError('replay_frame_limit')
    frame(records).save(directory/'final_frame.png')
    frames=[frame(records,step=t,width=1080) for t in range(1,total+1)]
    frames[0].save(directory/'replay.gif',save_all=True,append_images=frames[1:],
                   duration=[350]*(len(frames)-1)+[1600],loop=0,optimize=False)
    if (directory/'replay.gif').stat().st_size > 12_000_000:
        raise ValueError('replay_size_limit')
    return ['final_frame.png','replay.gif']
