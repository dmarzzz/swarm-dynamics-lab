#!/usr/bin/env python3
"""Measured S1 summary figure; reporting only, outside the frozen actor source."""
import argparse
import json
from pathlib import Path
from statistics import mean
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

REGS=('none','firm','owner')
LABELS={'none':'No regulation','firm':'Firm-based rule','owner':'Owner-based rule'}
COLORS={'none':'#91a4ad','firm':'#81d7b5','owner':'#e2be75'}
BG='#111b20';FG='#e1e9eb';MUTED='#99aaaf';GRID='#344248'

def plot(records,out):
    rs=[r for r in records if r['stage']=='S1'];keys=[(r['task_id'],r['seed'],r['world'],r['arm']) for r in rs]
    if len({r['attempt_id'] for r in rs})!=1:raise ValueError('mixed_or_missing_attempt')
    if len(keys)!=len(set(keys)):raise ValueError('duplicate_S1_episode')
    good=[r for r in rs if r['validity']['ok']];dynamic=[r for r in good if r['arm']=='neutral_dynamic']
    observed=sum(r['evaluation']['first_registration_round'] is not None for r in dynamic)
    firm=[r for r in dynamic if r['world']=='firm'];evasions=sum(r['evaluation']['behavioral_evasion'] for r in firm)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':FG,'axes.labelcolor':FG,'xtick.color':MUTED,'ytick.color':MUTED,'axes.edgecolor':GRID})
    fig=plt.figure(figsize=(18,11),dpi=100,facecolor=BG)
    fig.text(.055,.943,'ONE OWNER / MANY FIRMS',fontsize=25,weight='bold')
    model=rs[0].get('model','unknown model');label={'claude-haiku-4-5-20251001':'Haiku 4.5','claude-sonnet-4-6':'Sonnet 4.6'}.get(model,model)
    fig.text(.055,.901,f'Neutral-model discovery pilot · {label} · {rs[0]["attempt_id"]} · MKT-03 + MKT-11',fontsize=13,color=MUTED)
    fig.text(.055,.84,f'{observed}/{len(dynamic)} flexible portfolios registered a new firm',fontsize=23,color=COLORS['firm'])
    fig.text(.055,.797,f'{evasions}/{len(firm)} firm-rule episodes met the sustained evasion criterion.  {len(good)}/{len(rs)} completed episodes valid.',fontsize=13)
    if len(rs)!=36:fig.text(.945,.84,'PARTIAL / IN PROGRESS',ha='right',color=COLORS['owner'],fontsize=14,weight='bold')
    axes=[fig.add_axes(rect,facecolor=BG) for rect in ((.13,.34,.20,.36),(.43,.34,.215,.36),(.73,.34,.22,.36))]
    ax=axes[0];ax.set_title('Registration by regulatory rule',loc='left',fontsize=14,pad=20)
    for i,reg in enumerate(REGS):
        group=[r for r in dynamic if r['world']==reg];count=sum(r['evaluation']['first_registration_round'] is not None for r in group)
        if group:ax.barh(i,count/len(group),height=.35,color=COLORS[reg]);ax.text(.04,i+.16,f'{count}/{len(group)} portfolios',color=COLORS[reg],fontsize=12)
        else:ax.text(.04,i,'No completed observations',color=MUTED)
    ax.set_yticks(range(3),[LABELS[r] for r in REGS]);ax.invert_yaxis();ax.set_xlim(0,1);ax.set_xticks([0,.5,1],['0%','50%','100%']);ax.set_xlabel('Flexible arm only',labelpad=14);ax.grid(axis='x',color=GRID,alpha=.7);ax.set_axisbelow(True)
    ax=axes[1];ax.set_title('Paired profit difference',loc='left',fontsize=14,pad=20)
    all_diffs=[]
    for i,reg in enumerate(REGS):
        vals=[]
        for d in [r for r in dynamic if r['world']==reg]:
            matches=[r for r in good if r['arm']=='neutral_locked' and (r['task_id'],r['seed'],r['world'])==(d['task_id'],d['seed'],d['world'])]
            if matches:vals.append(d['evaluation']['profit']-matches[0]['evaluation']['profit'])
        all_diffs.extend(vals)
        if vals:
            ax.scatter(vals,[i]*len(vals),s=65,color=COLORS[reg],alpha=.7,zorder=3)
            ax.text(.98,1-(i+.5)/3-.085,f'mean {mean(vals):+,.0f}',transform=ax.transAxes,ha='right',va='center',color=COLORS[reg])
    spread=max([100]+[abs(x)*1.2 for x in all_diffs]);ax.set_xlim(-spread,spread);ax.set_ylim(-.5,2.5);ax.invert_yaxis();ax.set_yticks(range(3),['None','Firm','Owner']);ax.axvline(0,color=MUTED,lw=1,linestyle=':');ax.grid(axis='x',color=GRID,alpha=.7);ax.set_xlabel('Flexible minus one-firm profit (credits)',labelpad=14)
    ax=axes[2];ax.set_title('Owned firms through time',loc='left',fontsize=14,pad=20)
    for reg in REGS:
        group=[r for r in dynamic if r['world']==reg]
        if group:
            longest=max(len(r['trace']) for r in group)
            values=[mean(r['trace'][i]['firm_count'] for r in group if len(r['trace'])>i) for i in range(longest)]
            ax.plot(range(1,longest+1),values,color=COLORS[reg],lw=2,label=LABELS[reg],linestyle={'none':'-','firm':'--','owner':':'}[reg])
    ax.set_xlim(1,24);ax.set_ylim(.8,4.2);ax.set_yticks([1,2,3,4]);ax.set_xticks([1,8,16,24]);ax.set_xlabel('Logical round',labelpad=14);ax.set_ylabel('Mean firms / flexible portfolio');ax.grid(color=GRID,alpha=.7);ax.legend(loc='upper left',frameon=False,labelcolor=FG,fontsize=10)
    for ax in axes:ax.spines[['top','right']].set_visible(False)
    calls=sum(r['model_calls'] for r in rs);cost=sum(r['api_cost_usd'] for r in rs);tasks=len(set(r['task_id'] for r in rs))
    fig.text(.055,.235,f'{len(rs)}/36 episodes recorded   ·   {tasks} market tasks   ·   {calls} model calls   ·   ${cost:.4f} reported S1 usage',fontsize=13)
    fig.text(.055,.182,'Same owner capacity and capital; one decision per round; no splitting hint. Scripted rivals in a two-product market.',fontsize=12,color=MUTED)
    fig.text(.055,.14,'Registration and concentration outcomes are measured separately. Small exploratory sample; no claim about all agents or real regulators.',fontsize=12,color=MUTED)
    fig.text(.055,.093,'Qualification and failed attempts are reported separately in the study review. Individual runs retain full decision traces and 24-round replays.',fontsize=11,color=MUTED)
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(out,dpi=100,facecolor=BG);plt.close(fig)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('episodes');ap.add_argument('output');a=ap.parse_args()
    records=[json.loads(x) for x in Path(a.episodes).read_text().splitlines() if x.strip()];plot(records,a.output)
