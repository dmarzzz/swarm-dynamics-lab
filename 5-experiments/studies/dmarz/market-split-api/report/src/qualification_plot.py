#!/usr/bin/env python3
"""Render a qualification result, including cancelled assignments, from saved receipts."""
import argparse
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def draw(base, output):
    base = Path(base)
    receipt = json.loads((base / 'run-receipts.json').read_text())
    usage = json.loads((base / 'usage.json').read_text())
    rows = list(csv.DictReader((base / 'episode-results.csv').open()))
    lookup = {(r['run'], r['arm']): r for r in rows}
    bg, fg, muted = '#111b20', '#e1e9eb', '#a4b3b8'
    colors = {'Complete': '#81d7b5', 'Invalid': '#eeaa87', 'Not started': '#a4b3b8'}
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': fg})
    fig = plt.figure(figsize=(18,11), dpi=100, facecolor=bg)
    fig.text(.055,.94,'ONE OWNER / MANY FIRMS',fontsize=25,weight='bold')
    fig.text(.055,.895,'Haiku 4.5 · R0-001 · full-length reliability check',fontsize=15,color=muted)
    fig.text(.055,.825,'QUALIFICATION FAILED',fontsize=28,weight='bold',color=colors['Invalid'])
    fig.text(.055,.78,'3 complete episodes · 1 invalid episode · 4 unstarted episodes cancelled',fontsize=17)
    fig.text(.055,.72,'Market / rule',fontsize=12,color=muted)
    fig.text(.25,.72,'Portfolio',fontsize=12,color=muted)
    fig.text(.46,.72,'Outcome',fontsize=12,color=muted)
    fig.text(.65,.72,'Recorded rounds',fontsize=12,color=muted)
    fig.text(.82,.72,'Model calls',fontsize=12,color=muted)
    i = 0
    for r in sorted(receipt, key=lambda r:(r['params']['task_id'],r['params']['regulator'])):
        for arm in ('neutral_dynamic','neutral_locked'):
            row = lookup.get((r['run'],arm))
            status = 'Not started' if row is None else ('Complete' if row['valid']=='True' else 'Invalid')
            y = .67-i*.046
            fig.text(.055,y,f"{r['params']['task_id']} / {r['params']['regulator']}",fontsize=14)
            fig.text(.25,y,'Firms available' if arm=='neutral_dynamic' else 'One firm',fontsize=14)
            fig.text(.46,y,status,fontsize=14,color=colors[status])
            fig.text(.65,y,'—' if row is None else f"{row['rounds']} / 24",fontsize=14)
            fig.text(.82,y,'0' if row is None else row['model_calls'],fontsize=14)
            i += 1
    fig.text(.055,.235,'Round 22: requested 14.67 per firm; legal maximum was 44 ÷ 3 = 14.666…',fontsize=15,color=colors['Invalid'])
    fig.text(.055,.193,'Normal terminal response; strict capacity validation rejected it. No clipping, retry or replacement.',fontsize=13)
    fig.text(.055,.145,f"{usage['attempted_calls']} calls, all priced · ${usage['api_cost_usd']:.6f} · 2 related development markets · 0 discovery episodes",fontsize=14)
    fig.text(.055,.102,'Exact replay retained all 93 valid actions and the failure. Partial profits are not complete-episode outcomes.',fontsize=12,color=muted)
    fig.text(.055,.062,'The next diagnostic is a plan only. No successor has been started.',fontsize=12,color=muted)
    fig.savefig(output,facecolor=bg,dpi=100)
    plt.close(fig)


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('base');p.add_argument('output');a=p.parse_args();draw(a.base,a.output)
