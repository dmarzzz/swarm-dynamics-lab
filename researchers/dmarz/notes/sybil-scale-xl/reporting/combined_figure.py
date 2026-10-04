"""Combined scaling figure: parent Haiku cohort (N=36-972) and this study's Opus cohort (N=972-8,748).

Coverage selection, visible badges. Cohorts are drawn as separate series and never pooled.
Usage: python combined_figure.py <s1-a2 results-summary.json> <output.png>
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
PARENT = ROOT.parent / 'sybil-scale-api' / 'results-cells.csv'


def parent_series(rate, fixed):
    rows = [r for r in csv.DictReader(PARENT.open()) if r['arm'] == 'coverage' and r['visibility'] == 'visible'
            and float(r['attacker_pass']) == rate]
    out = []
    for n in (36, 108, 324, 972):
        checks = 4 if fixed else n // 9
        r = next(r for r in rows if int(r['n']) == n and int(r['checks']) == checks)
        out.append((n, float(r['rare_accuracy']), float(r['scripted_accuracy']), int(r['valid']), int(r['assigned'])))
    return out


def xl_series(summary, rate, fixed):
    out = []
    for n in (972, 2916, 8748):
        checks = 4 if fixed else n // 9
        c = next(c for c in summary['cells'] if c['n'] == n and c['arm'] == 'coverage' and c['checks'] == checks
                 and c['attacker_pass'] == rate and c['visibility'] == 'visible')
        out.append((n, c['metrics']['rare_accuracy']['mean'], c['scripted_accuracy'], c['valid'], c['assigned']))
    return out


def main():
    summary = json.loads(Path(sys.argv[1]).read_text())
    plt.rcParams.update({'font.family': 'DejaVu Sans Mono', 'font.size': 13})
    ink, muted, haiku, opus = '#1d232b', '#7a8591', '#c2701f', '#1f6f8b'
    fig, axes = plt.subplots(1, 2, figsize=(16, 7.2), dpi=125, sharey=True)
    for ax, rate, title in ((axes[0], .1, 'Informative checks (attackers pass 10%)'),
                            (axes[1], .9, 'Uninformative checks (attackers pass 90%)')):
        for fixed, style, label in ((False, '-', 'N/9 checks'), (True, '--', '4 checks')):
            p = parent_series(rate, fixed)
            x = xl_series(summary, rate, fixed)
            ax.plot([r[0] for r in p], [r[1] for r in p], style, color=haiku, lw=2.4, marker='o', ms=6,
                    label=f'Haiku 4.5, {label} (24/24 worlds)')
            ax.plot([r[0] for r in x], [r[1] for r in x], style, color=opus, lw=2.4, marker='s', ms=6,
                    label=f'Opus 5.5, {label}')
            for n, v, _, valid, assigned in x:
                ax.annotate(f'{valid}/{assigned}', (n, v), textcoords='offset points',
                            xytext=(0, 9 if fixed else -17), ha='center', fontsize=10, color=opus)
            if not fixed:
                ax.scatter([r[0] for r in p + x], [r[2] for r in p + x], marker='x', color=muted, s=36, zorder=3,
                           label='Plurality vote on the same packet (N/9 checks)')
        ax.set_xscale('log')
        ax.set_xticks([36, 108, 324, 972, 2916, 8748])
        ax.set_xticklabels(['36', '108', '324', '972', '2,916', '8,748'])
        ax.set_ylim(-0.04, 1.06)
        ax.set_yticks([0, .25, .5, .75, 1])
        ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])
        ax.set_title(title, loc='left', color=ink, fontsize=14)
        ax.set_xlabel('Simulated identities (log scale)', color=muted)
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        ax.grid(axis='y', color='#e3e6ea', lw=0.8)
    axes[0].set_ylabel('Specialist facts answered correctly', color=muted)
    handles, labels = axes[0].get_legend_handles_labels()
    seen = {}
    for h, l in zip(handles, labels):
        seen.setdefault(l, h)
    order = sorted(seen, key=lambda l: (l.startswith('Plurality'), not l.startswith('Haiku'), '4 checks' in l))
    fig.legend([seen[l] for l in order], order, loc='lower center', ncol=2, frameon=False, fontsize=11)
    fig.suptitle('Sybil defense as the swarm grows: coverage checking, visible badges', x=0.06, ha='left',
                 fontsize=17, color=ink)
    fig.text(0.06, 0.885, 'Haiku cohort: sybil-scale-api S1, 24/24 worlds per point. Opus cohort: sybil-scale-xl s1-a2, '
             'stopped at 481 of 576 calls during an account credit outage;\nlabels give valid/assigned worlds per Opus point. '
             'Cohorts are separate and never pooled. Opus at 4 checks mostly abstains (null) rather than guessing.',
             fontsize=10.5, color=muted, linespacing=1.5)
    fig.subplots_adjust(left=0.06, right=0.985, top=0.8, bottom=0.25, wspace=0.06)
    fig.savefig(sys.argv[2], facecolor='white')


if __name__ == '__main__':
    main()
