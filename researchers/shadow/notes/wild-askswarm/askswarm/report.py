"""Self-contained, escaped HTML. No source text is exported."""
import html
import json
from pathlib import Path


def esc(value):
    return html.escape(str(value), quote=True)


def display(value):
    if value is None:
        return "Unavailable"
    if isinstance(value, float):
        return f"{value:,.4f}"
    if isinstance(value, int):
        return f"{value:,}"
    return esc(value)


def table(headers, rows):
    return '<div class="scroll"><table><thead><tr>' + ''.join(f'<th>{esc(h)}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{display(v)}</td>' for v in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def lorenz_svg(results):
    colors = ['#8bd5ca', '#f5a97f', '#c6a0f6', '#91d7e3']
    svg = '<svg viewBox="0 0 800 410" role="img" aria-label="Participation Lorenz curves, missing identities excluded"><path d="M60 340 L760 340 M60 340 L60 30 M60 340 L760 30" stroke="#566" fill="none"/>'
    for i, result in enumerate(results):
        counts = sorted(result['participation_counts_descending'])
        if not counts:
            continue
        points, total, cumulative = ['60,340'], sum(counts), 0
        for index, value in enumerate(counts, 1):
            cumulative += value
            points.append(f'{60 + 700 * index / len(counts):.2f},{340 - 310 * cumulative / total:.2f}')
        color = colors[i % len(colors)]
        svg += f'<polyline points="{" ".join(points)}" stroke="{color}" stroke-width="3" fill="none"/>'
        svg += f'<text x="{60 + i * 225}" y="385" fill="{color}">{esc(result["name"])}</text>'
    return svg + '<text x="280" y="360" fill="#bcc">Share of observed identities</text></svg>'


def render(results, title="AskSwarm / same questions, three swarms"):
    metrics = [("Records", "records"), ("Observed identities", "identities"),
               ("Identity coverage", "identity_coverage"), ("Clock coverage", "time_coverage"),
               ("Lexical clusters", "clusters"), ("Multi-record clusters", "multi_record_clusters"),
               ("Multi-identity clusters", "multi_identity_clusters"), ("Participation Gini", "participation_gini"),
               ("Dissent marker fraction", "dissent_marker_fraction"), ("Revert marker fraction", "revert_marker_fraction")]
    body = '<p class="eyebrow">SWARM LAB / OFFLINE OBSERVATORY</p><h1>' + esc(title) + '</h1>'
    body += '<p class="lede">One measurement interface for public artifact corpora and our own research swarm. Missing identities and clocks stay missing. Lexical reuse is not proof of social influence.</p>'
    body += table(['Question'] + [r['name'] for r in results], [[label] + [r['summary'][key] for r in results] for label, key in metrics])
    body += '<h2>Participation concentration</h2><p>Equality is the diagonal. Only explicitly observed identities enter these curves; missing actors do not become fictional individuals.</p>' + lorenz_svg(results)
    for result in results:
        summary = result['summary']
        body += '<section><h2>' + esc(result['name']) + '</h2>'
        body += '<h3>Time to k observed identities</h3>'
        body += table(['k (includes first)', 'Reached', 'Not observed to reach', 'Eligible clusters', 'Median seconds, reached only'],
                      [[k, v['reached'], v['not_observed_to_reach'], v['at_risk_clusters'], v['seconds_among_reached']['median']] for k, v in summary['time_to_k'].items()])
        body += '<p>Zero eligible clusters means unavailable, not evidence of zero adoption. Not-observed-to-reach clusters are censored, not discarded successes.</p>'
        body += '<h3>Largest lexical clusters</h3>' + table(['Cluster', 'Records', 'Known identities', 'First observed identity / ties', 'First clock'],
                    [[c['cluster'], c['records'], c['identities'], ', '.join(c['first_movers'][:8]) or None, c['first_time']] for c in result['clusters'][:15]])
        body += '<h3>Near-term phrasing reuse credit</h3><p>Fractional credit for new cluster identities after prior observed posters within the configured step window. This is not causal influence or a quality ranking.</p>'
        body += table(['Observed identity', 'Fractional credit', 'Credit per record'], [[v['identity'], v['fractional_new_adopter_credit'], v['credit_per_record']] for v in result['influence'][:10]])
        body += '<h3>Observed identity span</h3>' + table(['Count with clock', 'Median seconds', '90th percentile seconds', 'Max seconds'], [[summary['identity_span_seconds'][k] for k in ('n', 'median', 'p90', 'max')]])
        body += '<h3>Record kinds</h3>' + table(['Kind', 'Records'], result['record_kinds'].items())
        body += '<details><summary>Provenance and configuration</summary><pre>' + esc(json.dumps({k: result.get(k) for k in ('schema_version', 'source', 'parameters', 'diagnostics')}, indent=2)) + '</pre></details></section>'
    limits = results[0]['limits'] if results else []
    body += '<h2>What this cannot establish</h2><ul>' + ''.join('<li>' + esc(item) + '</li>' for item in limits) + '</ul>'
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + esc(title) + '</title><style>body{background:#111719;color:#e6eeee;font:16px/1.6 system-ui,sans-serif;max-width:1180px;margin:auto;padding:40px 24px}h1{font-size:clamp(2rem,5vw,3.8rem);line-height:1.1;max-width:950px}h2{margin-top:44px;color:#8bd5ca}.eyebrow{font:12px monospace;letter-spacing:.16em;color:#f5a97f}.lede{max-width:850px;color:#bdcbcb;font-size:20px}table{border-collapse:collapse;width:100%;font:13px/1.5 monospace}th,td{text-align:left;border-bottom:1px solid #344244;padding:10px;vertical-align:top}th{color:#8bd5ca}.scroll{overflow-x:auto}svg{max-width:800px;width:100%}svg text{font:13px monospace}pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#bdcbcb}section{border-top:1px solid #344244;margin-top:35px}summary{cursor:pointer;color:#f5a97f}</style><main>' + body + '</main></html>'


def write_report(result, path):
    Path(path).write_text(render([result], result['name'] + ' / AskSwarm'), encoding='utf-8')
