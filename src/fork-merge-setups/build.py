#!/usr/bin/env python3
"""Build the fork-merge setups report (one self-contained HTML page).

Inputs, all in this folder: cards/*.json (one setup card per library entry tagged fork-merge-security, written by
agent readers from the entry text), rigs.json (the nine rig profiles), prose.html (the page body with {{slots}}).
Citations written as [[library-id]] become links to the entry on GitHub.

    python3 src/fork-merge-setups/build.py out.html
"""
import glob, html, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GH = "https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/"
LIBRARY = "1-library"  # research-phase layout; the folder was library/ before the move (see scripts/lab.py)

def library_index():
    idx = {}
    for p in sorted(glob.glob(os.path.join(REPO, LIBRARY, "*", "*.md"))):
        i = os.path.basename(p)[:-3]
        if i in ("README", "INDEX"):
            continue
        t = re.search(r'^title:\s*"?(.*?)"?\s*$', open(p, encoding="utf-8").read(), re.M)
        idx[i] = (os.path.relpath(p, REPO).replace(os.sep, "/"), t.group(1) if t else i)
    return idx

LIB = library_index()
MISSING = set()

def esc(s):
    return html.escape(str(s), quote=True)

def cite(m):
    i = m.group(1)
    if i not in LIB:
        MISSING.add(i)
        return f'<span class="cite miss">{esc(i)}</span>'
    path, title = LIB[i]
    return f'<a class="cite" href="{GH}{path}" title="{esc(title)}">{esc(i)}</a>'

def cites(s):
    return re.sub(r"\[\[([a-z0-9-]+)\]\]", cite, s)

cards = []
for f in sorted(glob.glob(os.path.join(HERE, "cards", "*.json"))):
    cards += json.load(open(f))["entries"]
assert len({c["id"] for c in cards}) == len(cards), "duplicate card ids"
for c in cards:
    c["path"] = LIB.get(c["id"], ("", ""))[0]
rigs = json.load(open(os.path.join(HERE, "rigs.json")))

OPS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]
ADV = ["A1", "A2", "A3", "A4"]
MEAS = {"measured", "demonstration"}
meas = [c for c in cards if c["kind"] in MEAS]
cell = Counter()
for c in meas:
    for o in c.get("merge_ops") or []:
        for a in c.get("adversary") or []:
            cell[(o, a)] += 1
        if not c.get("adversary"):
            cell[(o, "-")] += 1
OPNAME = {"M1": "report into context", "M2": "summary, compaction", "M3": "memory, config write", "M4": "skill distillation",
          "M5": "weight merge", "M6": "distillation on outputs", "M7": "gradient aggregation", "M8": "vote, quorum"}
ADVNAME = {"A1": "content", "A2": "host", "A3": "channel", "A4": "common mode", "-": "none"}
peak = max(cell.values())

def matrix():
    h = ['<div class="tw"><table class="mx"><thead><tr><th></th>']
    for a in ADV + ["-"]:
        h.append(f'<th>{a}<br><span>{ADVNAME[a]}</span></th>')
    h.append("</tr></thead><tbody>")
    for o in OPS:
        h.append(f'<tr><th>{o} <span>{OPNAME[o]}</span></th>')
        for a in ADV + ["-"]:
            n = cell[(o, a)]
            alpha = 0 if n == 0 else 0.12 + 0.78 * n / peak
            h.append(f'<td data-op="{o}" data-adv="{a}" style="--a:{alpha:.2f}" class="{"z" if n == 0 else ""}">{n or "·"}</td>')
        h.append("</tr>")
    h.append('</tbody></table></div><p class="small">Column "none": the entry measures a merge with no adversary '
             '(benign error correlation, compaction erosion). Cell shade is proportional to count; "·" is zero.</p>')
    return "".join(h)

def rigs_html():
    out = []
    for r in rigs:
        keys = " ".join(f"[[{k}]]" for k in r["keys"])
        out.append(f'''<article class="rig" id="{r["id"]}">
<h3><span class="rid">{r["id"]}</span> {esc(r["name"])} <span class="tag">{esc(r["ops"])} · {esc(r["adv"])}</span></h3>
<dl>
<dt>Setup</dt><dd>{cites(esc(r["setup"]))}</dd>
<dt>Attacker</dt><dd>{cites(esc(r["attacker"]))}</dd>
<dt>Defender assumes</dt><dd>{cites(esc(r["defender"]))}</dd>
<dt>Numbers</dt><dd>{cites(esc(r["numbers"]))}</dd>
<dt>Cannot tell us</dt><dd>{cites(esc(r["misses"]))}</dd>
<dt>Entries</dt><dd class="keys">{cites(keys)}</dd>
</dl></article>''')
    return "\n".join(out)

DIAGRAM = '''<figure class="dia"><svg viewBox="0 0 760 300" role="img" aria-label="Parent P forks parts p1 to pn into domains; a merge operator folds them back into P prime; adversaries A1 to A4 attach at the domain, host, channel and shared base">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--ink2)"/></marker></defs>
<rect x="20" y="118" width="86" height="54" rx="6" class="n"/><text x="63" y="143" class="t">P</text><text x="63" y="160" class="s">parent</text>
<g class="e"><path d="M106,135 C150,80 170,62 216,62" marker-end="url(#ar)"/><path d="M106,145 L216,145" marker-end="url(#ar)"/><path d="M106,155 C150,210 170,228 216,228" marker-end="url(#ar)"/></g>
<text x="150" y="128" class="s">fork</text>
<rect x="218" y="40" width="70" height="40" rx="6" class="n"/><text x="253" y="65" class="t">p1</text>
<rect x="218" y="125" width="70" height="40" rx="6" class="n bad"/><text x="253" y="150" class="t">p2</text>
<rect x="218" y="208" width="70" height="40" rx="6" class="n"/><text x="253" y="233" class="t">pn</text>
<rect x="300" y="34" width="104" height="52" rx="4" class="d"/><text x="352" y="64" class="s">domain D1</text>
<rect x="300" y="119" width="104" height="52" rx="4" class="d"/><text x="352" y="149" class="s">domain D2</text>
<rect x="300" y="202" width="104" height="52" rx="4" class="d"/><text x="352" y="232" class="s">domain Dn</text>
<g class="e"><path d="M404,60 C470,60 480,120 548,136" marker-end="url(#ar)"/><path d="M404,145 L548,145" marker-end="url(#ar)" class="hot"/><path d="M404,228 C470,228 480,170 548,154" marker-end="url(#ar)"/></g>
<rect x="550" y="112" width="92" height="66" rx="6" class="m"/><text x="596" y="140" class="t">merge</text><text x="596" y="158" class="s">M1 … M8</text>
<path d="M642,145 L686,145" class="e2" marker-end="url(#ar)"/>
<rect x="688" y="118" width="56" height="54" rx="6" class="n"/><text x="716" y="150" class="t">P′</text>
<g class="adv"><circle cx="404" cy="112" r="11"/><text x="404" y="116">A1</text>
<circle cx="218" cy="122" r="11"/><text x="218" y="126">A2</text>
<circle cx="476" cy="145" r="11"/><text x="476" y="149">A3</text></g>
<rect x="218" y="270" width="186" height="22" rx="4" class="d"/><text x="311" y="285" class="s">shared base model, tools, init</text>
<g class="adv"><circle cx="418" cy="281" r="11"/><text x="418" y="285">A4</text></g>
<g class="e"><path d="M253,268 L253,250" class="dash"/></g>
</svg><figcaption>One part (p2) reads hostile content in its domain (A1), or runs on a hostile host (A2). Its return passes through a channel the attacker may control (A3) into the merge. A4 sits under every part at once, so the parts are correlated before any attacker acts.</figcaption></figure>'''

CSS = '''
:root{--surface:#fcfcfb;--panel:#f4f3ef;--ink:#0b0b0b;--ink2:#52514e;--muted:#8a8984;--grid:#e6e5e0;--acc:#2a78d6;--hot:#d0482a;--accrgb:42,120,214}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--surface:#1a1a19;--panel:#222220;--ink:#fff;--ink2:#c3c2b7;--muted:#8f8e86;--grid:#2e2e2c;--acc:#3987e5;--hot:#e2603f;--accrgb:57,135,229}}
:root[data-theme="dark"]{--surface:#1a1a19;--panel:#222220;--ink:#fff;--ink2:#c3c2b7;--muted:#8f8e86;--grid:#2e2e2c;--acc:#3987e5;--hot:#e2603f;--accrgb:57,135,229}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--surface);color:var(--ink);font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}
main{max-width:1080px;margin:0 auto;padding:32px 16px 80px;overflow-wrap:anywhere}
.two>div,.tw{min-width:0;max-width:100%}.cite{white-space:normal}
h1{font-size:21px;margin:0 0 4px;font-weight:600}.byline{color:var(--muted);font-size:12px;margin:0 0 28px}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink2);margin:44px 0 12px;font-weight:600;border-top:1px solid var(--grid);padding-top:18px}
h3{font-size:14px;margin:18px 0 8px;font-weight:600}
p,li{max-width:860px}p{margin:0 0 12px}ul,ol{padding-left:22px}li{margin:6px 0}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
code{font:inherit;color:var(--ink2)}
.small{font-size:12px;color:var(--muted)}
.status{font-size:12.5px;color:var(--ink2);border-left:2px solid var(--hot);padding-left:12px}
.cite{font-size:11.5px;color:var(--acc);white-space:nowrap}.cite::before{content:"["}.cite::after{content:"]"}.cite.miss{color:var(--muted)}
nav.toc{font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;gap:4px 16px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px 32px}@media(max-width:760px){.two{grid-template-columns:1fr}}
table{border-collapse:collapse}
.kv td{padding:4px 10px 4px 0;vertical-align:top;border-bottom:1px solid var(--grid);font-size:12.5px}.kv td:first-child{color:var(--acc);font-weight:600;white-space:nowrap}
.dia{margin:18px 0 22px}.dia svg{width:100%;max-width:760px;height:auto;display:block}
.dia .n{fill:var(--panel);stroke:var(--ink2);stroke-width:1}.dia .n.bad{stroke:var(--hot);stroke-width:1.6}
.dia .d{fill:none;stroke:var(--grid);stroke-width:1;stroke-dasharray:3 3}.dia .m{fill:none;stroke:var(--acc);stroke-width:1.6}
.dia .t{font-size:14px;fill:var(--ink);text-anchor:middle;font-weight:600}.dia .s{font-size:10.5px;fill:var(--muted);text-anchor:middle}
.dia .e path,.dia .e2{fill:none;stroke:var(--ink2);stroke-width:1}.dia .e .hot{stroke:var(--hot);stroke-width:1.6}.dia .dash{stroke-dasharray:2 3}
.dia .adv circle{fill:var(--surface);stroke:var(--hot);stroke-width:1.4}.dia .adv text{font-size:9.5px;fill:var(--hot);text-anchor:middle;font-weight:600}
figcaption{font-size:12px;color:var(--muted);max-width:760px;margin-top:6px}
.tw{overflow-x:auto}
.mx th,.mx td{padding:6px 10px;font-size:12px;border-bottom:1px solid var(--grid)}
.mx thead th{color:var(--ink2);font-weight:600;text-align:center}.mx thead th span,.mx tbody th span{display:block;font-weight:400;color:var(--muted);font-size:10.5px}
.mx tbody th{text-align:left;font-weight:600;white-space:nowrap}.mx tbody th span{display:inline;margin-left:4px}
.mx td{text-align:center;min-width:64px;background:rgba(var(--accrgb),var(--a));cursor:pointer;font-variant-numeric:tabular-nums}
.mx td.z{color:var(--muted);cursor:default}.mx td:not(.z):hover{outline:1px solid var(--ink)}
.rig{border-top:1px solid var(--grid);padding:6px 0 10px}
.rig h3{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px}.rid{color:var(--acc)}.tag{font-weight:400;font-size:11.5px;color:var(--muted)}
.rig dl{display:grid;grid-template-columns:140px 1fr;gap:6px 16px;margin:0;font-size:13px}
.rig dt{color:var(--muted);font-size:12px}.rig dd{margin:0;max-width:860px}.rig dd.keys{line-height:1.9}
@media(max-width:640px){.rig dl{grid-template-columns:1fr}.rig dt{margin-top:6px}}
.gaps li{margin:10px 0}
.spec th,.spec td{text-align:left;vertical-align:top;padding:7px 12px 7px 0;border-bottom:1px solid var(--grid);font-size:12.5px}.spec th{color:var(--ink2);font-weight:600}
.spec td:first-child{font-weight:600;white-space:nowrap}
.filters{display:flex;flex-wrap:wrap;gap:8px 12px;margin:10px 0 12px;align-items:center;font-size:12px}
.filters input,.filters select{font:inherit;font-size:12px;color:var(--ink);background:var(--surface);border:1px solid var(--grid);border-radius:4px;padding:5px 8px}
.filters input{flex:1;min-width:200px}
#count{color:var(--muted)}button.clr{font:inherit;font-size:12px;background:none;border:1px solid var(--grid);border-radius:4px;color:var(--ink2);padding:5px 8px;cursor:pointer}
#cards{width:100%;font-size:12px}#cards th{position:sticky;top:0;background:var(--surface);text-align:left;color:var(--ink2);font-weight:600;padding:6px 8px;border-bottom:1px solid var(--ink2);cursor:pointer;white-space:nowrap}
#cards td{padding:6px 8px;border-bottom:1px solid var(--grid);vertical-align:top}#cards tr.row{cursor:pointer}#cards tr.row:hover td{background:var(--panel)}
#cards td.id{white-space:nowrap}#cards .k{color:var(--muted)}
tr.det td{background:var(--panel);padding:10px 14px 14px}
.det dl{display:grid;grid-template-columns:150px 1fr;gap:4px 14px;margin:0}.det dt{color:var(--muted)}.det dd{margin:0}
@media(max-width:640px){.det dl{grid-template-columns:1fr}#cards .hide-s{display:none}}
'''

JS = r'''
const C=window.CARDS,tb=document.querySelector('#cards tbody'),q=document.getElementById('q'),fk=document.getElementById('fk'),fo=document.getElementById('fo'),fa=document.getElementById('fa'),fd=document.getElementById('fd'),cnt=document.getElementById('count');
const GH="https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/";
const e=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let sortK='relevance',sortD=-1,open=null;
function hay(c){return [c.id,c.title,c.setup,c.attacker_access,c.attacker_knowledge,c.defender_assumptions,c.headline,c.gaps,c.metric,c.attacker_goal].join(' ').toLowerCase()}
C.forEach(c=>c._h=hay(c));
function render(){
  const t=q.value.toLowerCase().trim(),k=fk.value,o=fo.value,a=fa.value,d=fd.value;
  let r=C.filter(c=>(!t||t.split(/\s+/).every(w=>c._h.includes(w)))&&(!k||c.kind===k)&&(!o||(c.merge_ops||[]).includes(o))&&(!a||(a==='-'?!(c.adversary||[]).length:(c.adversary||[]).includes(a)))&&(!d||c.read_depth===d));
  r.sort((x,y)=>{let p=x[sortK],q2=y[sortK];if(p==null)return 1;if(q2==null)return -1;return (p>q2?1:p<q2?-1:0)*sortD||x.id.localeCompare(y.id)});
  cnt.textContent=r.length+' of '+C.length;
  tb.innerHTML=r.map(c=>`<tr class="row" data-id="${e(c.id)}"><td class="id">${e(c.id)}</td><td>${e(c.title)}</td><td class="k">${e(c.kind)}</td><td class="k">${e((c.merge_ops||[]).join(' '))}</td><td class="k">${e((c.adversary||[]).join(' '))}</td><td class="k hide-s">${e(c.read_depth)}</td><td class="k hide-s">${e(c.relevance)}</td></tr>`+(open===c.id?det(c):'')).join('');
}
function det(c){const f=[['Setup',c.setup],['Attacker access',c.attacker_access],['Attacker knowledge',c.attacker_knowledge],['Attacker goal',c.attacker_goal],['Defender assumes',c.defender_assumptions],['Metric',c.metric],['Headline',c.headline],['Gap for fork-merge',c.gaps]];
  return `<tr class="det"><td colspan="7"><dl>${f.filter(x=>x[1]).map(x=>`<dt>${x[0]}</dt><dd>${e(x[1])}</dd>`).join('')}<dt>Entry</dt><dd><a href="${GH}${e(c.path)}">${e(c.path)}</a> · ${e(c.type)} · ${e(c.year)} · ${e(c.community)}</dd></dl></td></tr>`}
tb.addEventListener('click',ev=>{const tr=ev.target.closest('tr.row');if(!tr||ev.target.closest('a'))return;open=open===tr.dataset.id?null:tr.dataset.id;render()});
document.querySelectorAll('#cards th[data-k]').forEach(th=>th.addEventListener('click',()=>{const k=th.dataset.k;sortD=sortK===k?-sortD:(k==='relevance'||k==='year'?-1:1);sortK=k;render()}));
[q,fk,fo,fa,fd].forEach(x=>x.addEventListener('input',render));
document.getElementById('clr').addEventListener('click',()=>{q.value='';[fk,fo,fa,fd].forEach(s=>s.value='');render()});
document.querySelectorAll('.mx td:not(.z)').forEach(td=>td.addEventListener('click',()=>{fo.value=td.dataset.op;fa.value=td.dataset.adv;fk.value='';q.value='';open=null;render();document.getElementById('all').scrollIntoView({behavior:'smooth'})}));
render();
'''

def table_html():
    kinds = sorted(Counter(c["kind"] for c in cards).items(), key=lambda x: -x[1])
    opt = lambda vals: "".join(f'<option value="{esc(v)}">{esc(l)}</option>' for v, l in vals)
    return f'''<section id="all"><h2>All {len(cards)} setup cards</h2>
<p>One card per library entry tagged <code>fork-merge-security</code>. Click a row for its setup and threat model, and use the entry link to read the full library entry. The cards were written by AI agents from the entry text only; where an entry did not state a field, the card leaves it empty. The read-depth column is the entry's own claim about how much of the source was read.</p>
<div class="filters"><input id="q" placeholder="search setup, attacker, numbers…" aria-label="search">
<select id="fk" aria-label="kind"><option value="">all kinds</option>{opt((k, f"{k} ({n})") for k, n in kinds)}</select>
<select id="fo" aria-label="merge operator"><option value="">any merge op</option>{opt((o, f"{o} {OPNAME[o]}") for o in OPS)}</select>
<select id="fa" aria-label="adversary"><option value="">any adversary</option>{opt((a, f"{a} {ADVNAME[a]}") for a in ADV + ["-"])}</select>
<select id="fd" aria-label="read depth"><option value="">any depth</option>{opt((d, d) for d in ["full", "ran", "skim", "abstract"])}</select>
<button class="clr" id="clr">clear</button><span id="count"></span></div>
<div class="tw"><table id="cards"><thead><tr><th data-k="id">id</th><th data-k="title">title</th><th data-k="kind">kind</th><th>ops</th><th>adv</th><th data-k="read_depth" class="hide-s">depth</th><th data-k="relevance" class="hide-s">rel</th></tr></thead><tbody></tbody></table></div></section>'''

def main(out):
    date = "2026-10-03"
    body = open(os.path.join(HERE, "prose.html"), encoding="utf-8").read()
    body = (body.replace("{{N}}", str(len(cards))).replace("{{NMEAS}}", str(len(meas))).replace("{{DATE}}", date)
                .replace("{{DIAGRAM}}", DIAGRAM).replace("{{MATRIX}}", matrix()).replace("{{RIGS}}", rigs_html()))
    body = cites(body)
    slim = [{k: c.get(k) for k in ("id", "title", "year", "type", "read_depth", "relevance", "kind", "community", "merge_ops",
             "adversary", "attacker_access", "attacker_knowledge", "attacker_goal", "defender_assumptions", "setup", "metric",
             "headline", "gaps", "path")} for c in cards]
    data = json.dumps(slim, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fork-merge setups</title><style>{CSS}</style></head><body><main>
<h1>Fork-merge security: experimental setups and threat models</h1>
<p class="byline">swarm-lab · {len(cards)} library entries · built {date} by dmarz's agent from <code>src/fork-merge-setups/</code></p>
<nav class="toc"><a href="#what">what this is</a><a href="#model">scenario and terms</a><a href="#matrix">where the measurements sit</a><a href="#rigs">the nine rigs</a><a href="#assumptions">fixed assumptions</a><a href="#next">what a rig would need</a><a href="#all">all cards</a></nav>
{body}
{table_html()}
</main><script>window.CARDS={data};</script><script>{JS}</script></body></html>'''
    open(out, "w", encoding="utf-8").write(page)
    print(f"wrote {out}: {len(cards)} cards, {len(meas)} measured/demonstration, {len(page)//1024} KB")
    if MISSING:
        print("unresolved citations:", ", ".join(sorted(MISSING)))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fork-merge-setups.html"))
