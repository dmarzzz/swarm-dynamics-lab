"""Render the offline review from the frozen, human-authored assessment data."""
import json
from pathlib import Path
here = Path(__file__).resolve().parent
payload = json.dumps(json.loads((here/'assessments.json').read_text()), ensure_ascii=False).replace('<', '\\u003c')
template = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Biology and visual promise — Swarm Lab review</title>
<style>
:root{color-scheme:dark;font:16px/1.55 system-ui,sans-serif;background:#101820;color:#e6eef4}*{box-sizing:border-box}body{margin:0}header,main{max-width:1280px;margin:auto;padding:28px}h1{font-size:clamp(1.8rem,4vw,3rem);line-height:1.12;max-width:800px;margin:12px 0}h2{font-size:1.3rem}a{color:#86d6ef;text-underline-offset:3px}p{max-width:84ch}small,.muted{color:#b4c3d0}.eyebrow{font-size:.8rem;text-transform:uppercase;letter-spacing:.15em;color:#a4d8c5}.notice{border-left:3px solid #d7b976;padding:12px 18px;background:#1c252b;max-width:950px}.nav{display:flex;flex-wrap:wrap;gap:18px}.stats{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}.stat{border:1px solid #354653;border-radius:10px;padding:12px 18px;min-width:140px}.stat b{display:block;font-size:1.65rem;color:#a4d8c5}.controls{background:#18242d;padding:18px;border-radius:12px;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:14px}label{font-size:.85rem;color:#c9d8e3}input,select,button{font:inherit;color:inherit;background:#101820;border:1px solid #597181;border-radius:6px;padding:10px;width:100%;margin-top:5px}button{cursor:pointer;width:auto;padding:8px 16px}input:focus,select:focus,button:focus,a:focus,summary:focus{outline:3px solid #e5c88b;outline-offset:3px}.toolbar{display:flex;gap:16px;align-items:center;justify-content:space-between;margin:16px 0}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.card{border:1px solid #354653;border-radius:12px;padding:22px;background:#15212a;min-width:0}.cards:has(>.card:only-child){grid-template-columns:minmax(0,850px)}.card:target{border-color:#e5c88b}.card h2{margin:10px 0}.card p{margin:12px 0;overflow-wrap:anywhere}.badges{display:flex;flex-wrap:wrap;gap:7px}.badge{font-size:.75rem;padding:3px 8px;background:#2a3b46;border-radius:4px;color:#d8e9f2}.visual{padding:12px 14px;background:#213c3e;border-left:3px solid #9ed9c5;border-radius:3px}.boundary{color:#dcc8a2}.card details{border-top:1px solid #354653;margin-top:15px;padding-top:12px}.card summary{cursor:pointer;color:#9cd2e6}.card ul{padding-left:20px}.card dt{font-weight:650;margin-top:12px}.card dd{margin:3px 0;color:#bdcdd7}.links{display:flex;flex-wrap:wrap;gap:12px;font-size:.9rem}.empty{padding:36px;border:1px dashed #597181}.method-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.method{background:#1c2b34;border-radius:8px;padding:14px}.method b{display:block}.counts{font-size:.85rem;color:#b4c3d0}footer{padding:28px;color:#b4c3d0}#count{font-weight:650}#methods{margin:22px 0}noscript{display:block;padding:24px}@media(max-width:800px){.controls{grid-template-columns:1fr 1fr}.cards{grid-template-columns:1fr}.method-grid{grid-template-columns:1fr 1fr}}@media(max-width:480px){header,main{padding:18px}.controls,.method-grid{grid-template-columns:1fr}.stat{min-width:110px;padding:10px}.toolbar{align-items:flex-start}h1{font-size:2rem}}
</style>
<header><div class="eyebrow">Swarm Lab · Vishesh · research screening</div><h1>Biological precedent.<br>Visuals that explain a mechanism.</h1><p>A review of the current ideas, original project briefs and experimental designs. Scientific value and visualization value are separate judgments.</p><div class="notice">These are proposed comparisons and visual specifications—not measured results, accepted hypotheses or live experiments. Biology supplies possible mechanisms and useful limits; resemblance alone is not evidence.</div><div class="stats"><div class="stat"><b>301</b>review records</div><div class="stat"><b>214</b>atlas candidates</div><div class="stat"><b>16</b>original briefs</div><div class="stat"><b>0</b>registered hypotheses</div></div><nav class="nav"><a href="synthesis.md">Shortlist and corrections</a><a href="sources.md">Primary source ledger</a><a href="README.md">Scope and rubric</a><a href="assessment-bank.md">Full written review</a><a href="assessments.json">Structured data</a></nav><p class="muted">Records overlap: briefs, designs and extensions can investigate the same mechanism. Counts describe coverage, not independent discoveries. Snapshot: 2026-10-03.</p></header>
<main><details id="methods"><summary>Explore the mechanism families</summary><p class="muted">Family counts summarize these editorial assessments, not biological measurements. Use a family to filter the review.</p><div class="method-grid" id="families"></div></details><section class="controls" aria-label="Review filters"><label>Search IDs, ideas or project briefs<input id="search" type="search" placeholder="e.g. immune, SOC-07, regrowth" autocomplete="off"></label><label>Record type<select id="kind"><option value="">All record types</option></select></label><label>Scientific category<select id="promise"><option value="">All categories</option><option>Prioritize</option><option>Develop</option><option>Foundation</option><option>Defer</option></select></label><label>Mechanism<select id="mechanism"><option value="">All mechanisms</option></select></label></section><div class="toolbar"><div><span id="count" role="status" aria-live="polite"></span><br><small>High visual value means an informative view is specified; no result is implied.</small></div><button id="reset" type="button">Clear filters</button></div><div class="cards" id="cards"></div><noscript>JavaScript is needed for filtering. The <a href="assessment-bank.md">written assessment bank</a> contains every record.</noscript></main><footer>vishesh/codex-methods · Owned exploratory notes · Full reading and lab review gates still apply.</footer>
<script id="review-data" type="application/json">__DATA__</script>
<script>
'use strict';
const data=JSON.parse(document.getElementById('review-data').textContent);
const byId=id=>document.getElementById(id), controls=['search','kind','promise','mechanism'];
function el(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
function link(text,url){const n=el('a',text);n.href=url;return n;}
function para(parent,label,text,cls){if(!text)return;const p=el('p',undefined,cls);p.append(el('strong',label+' '),document.createTextNode(text));parent.append(p);}
function option(select,value,text){const o=el('option',text);o.value=value;select.append(o);}
for(const kind of Object.keys(data.metadata.counts))option(byId('kind'),kind,kind);
for(const [key,m]of Object.entries(data.mechanisms)){
 option(byId('mechanism'),key,m.title);
 const count=data.assessments.filter(r=>r.mechanism===key).length;
 const box=el('div',undefined,'method');box.append(el('b',m.title),el('div',count+' review records','counts'));
 const button=el('button','Filter');button.type='button';button.setAttribute('aria-label','Filter '+m.title);button.onclick=()=>{byId('mechanism').value=key;render();byId('count').scrollIntoView({block:'center'});};box.append(button);byId('families').append(box);
}
const repository='https://github.com/dmarzzz/swarm-lab/blob/'+data.metadata.source_commit+'/';
function card(r){
 const c=el('article',undefined,'card');c.id=r.id;
 const badges=el('div',undefined,'badges');for(const t of [r.id,r.kind,r.promise,'Visual: '+r.visual_value])badges.append(el('span',t,'badge'));c.append(badges,el('h2',r.title),el('p',r.assessment));
 para(c,'Visual specification:',r.visual_design,'visual');
 para(c,'Connection:',data.mechanisms[r.mechanism].title+'. '+r.biological_connection);
 para(c,'Transfer limit:',r.transfer_limit,'boundary');
 if(r.briefs.length)para(c,'Original briefs:',r.briefs.join(', '));
 const links=el('div',undefined,'links');links.append(link('Original item',repository+r.path),link('Permalink','#'+r.id));c.append(links);
 const d=el('details');d.append(el('summary','Sources, controls and connected items'));
 para(d,'Question:',r.question);para(d,'Original comparison:',r.comparison);para(d,'Controls and confounds:',r.confounds);para(d,'Original falsifier:',r.falsifier);para(d,'Feasibility / scope:',r.feasibility);
 if(r.related.length)para(d,'Related items:',r.related.join(', '));
 if(r.source_anchors.length){const ul=el('ul');for(const id of r.source_anchors){const s=data.sources[id],li=el('li');li.append(link(s.title,s.url),el('p',s.access));ul.append(li);}d.append(el('strong','Freshly read primary anchors'),ul);}else d.append(el('p','No strong freshly verified biological anchor. Use the original computational/methodological prior work.'));
 if(r.prior.length){d.append(el('strong','Original prior-work metadata (not newly reread here)'));const ul=el('ul');for(const p of r.prior){const id=typeof p==='string'?p:p.id;const li=el('li',id+(typeof p==='object'&&p.relation?' — '+p.relation:''));ul.append(li);}d.append(ul);}
 c.append(d);return c;
}
function render(){const q=byId('search').value.trim().toLowerCase();const matches=data.assessments.filter(r=>(!q||JSON.stringify(r).toLowerCase().includes(q))&&['kind','promise','mechanism'].every(k=>!byId(k).value||r[k]===byId(k).value));byId('count').textContent=matches.length+' of '+data.assessments.length+' records';const frag=document.createDocumentFragment();for(const r of matches)frag.append(card(r));if(!matches.length)frag.append(el('div','No matching records. Clear a filter or try a shorter search.','empty'));byId('cards').replaceChildren(frag);}
for(const id of controls)byId(id).addEventListener(id==='search'?'input':'change',render);
byId('reset').onclick=()=>{for(const id of controls)byId(id).value='';history.replaceState(null,'',location.pathname+location.search);render();};
function focusHash(){const id=decodeURIComponent(location.hash.slice(1));if(!data.assessments.some(r=>r.id===id))return;for(const key of controls)byId(key).value='';byId('search').value=id;render();const target=byId(id);if(target)target.scrollIntoView({block:'start'});}
render();focusHash();window.addEventListener('hashchange',focusHash);
</script></html>'''
(here/'review.html').write_text(template.replace('__DATA__',payload))
print('Rendered offline review for',len(json.loads(payload)['assessments']),'records')
