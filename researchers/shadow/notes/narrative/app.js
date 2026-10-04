'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const colors={dmarz:'#e7bd76',vishesh:'#93b8d0',shadow:'#dca99b'};
const names={dmarz:'dmarz',vishesh:'vishesh',shadow:'shadow / Sol'};
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtTime=s=>new Date(s).toLocaleString('en-GB',{timeZone:'UTC',day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'})+' UTC';
const pct=v=>(v*100).toFixed(0)+'%';
const short=(s,n=38)=>s.length>n?s.slice(0,n-1)+'…':s;
const safeLink=(url,label)=>`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`;
let D, selected, hours=24, allStudies=false, ledgerAll=false, owners=new Set(Object.keys(names)), weights, nodeMap;
function statusBadge(n){return `<span class="badge ${esc(n.status)}">${esc(n.status)}</span>`}
function renderMomentum(){
 $('#momentum').innerHTML=D.researchers.map(r=>`<div class="momentum-item" style="--owner-color:${colors[r.id]}"><h3>${esc(r.name)}</h3><strong>${r.commits[String(hours)]}</strong> <span class="quiet mono">commits / ${hours}h</span><p>${r.commits_per_hour[String(hours)]}/h · ${hours===3?r.active_threads_3h:r.active_threads_12h} active lanes${hours===24?' in 12h':''}</p><p class="mono">${r.checked_cohorts.length} cohorts with external arithmetic checks</p></div>`).join('');
}
function renderTimeline(){
 const W=1160,left=120,right=1125,start=Date.parse(D.as_of)-hours*3600000,end=Date.parse(D.as_of),x=t=>left+(Date.parse(t)-start)/(end-start)*(right-left);
 let svg=`<title>Attributed commit activity during the last ${hours} hours</title>`;
 const ticks=hours===3?6:hours===12?6:8;
 for(let i=0;i<=ticks;i++){
  const t=start+(end-start)*i/ticks,xx=left+(right-left)*i/ticks;
  const label=new Date(t).toLocaleTimeString('en-GB',{timeZone:'UTC',hour:'2-digit',minute:'2-digit'});
  svg+=`<line x1="${xx}" x2="${xx}" y1="26" y2="288" stroke="#2a352d"/><text x="${xx}" y="15" text-anchor="middle" font-size="9">${label}</text>`;
 }
 Object.keys(names).forEach((owner,index)=>{
  const top=42+index*86;
  svg+=`<text x="0" y="${top+29}" style="fill:${colors[owner]}" font-size="11">${esc(names[owner])}</text>`;
  const commits=D.commits.filter(c=>c.owner===owner&&Date.parse(c.time)>=start);
  // One event per dot; deterministic vertical jitter reveals dense periods without fake sample sizes.
  commits.forEach(c=>{const yy=top+60+parseInt(c.sha.slice(0,2),16)%12;svg+=`<circle cx="${x(c.time)}" cy="${yy}" r="1.6" fill="${colors[owner]}" opacity=".55"><title>${esc(c.subject)} · ${esc(c.time)}</title></circle>`});
  const threads=D.threads.filter(t=>t.owner===owner&&Date.parse(t.last)>=start).sort((a,b)=>b.commits_3h-a.commits_3h||b.commits_12h-a.commits_12h).slice(0,3);
  threads.forEach((t,j)=>{
   const xx=Math.max(left,x(t.first)),xe=Math.max(xx+3,x(t.last)),yy=top+j*18;
   svg+=`<a href="${esc(t.latest.url)}" target="_blank"><title>${esc(t.agent)}: ${esc(t.latest.subject)}</title><line x1="${xx}" y1="${yy+8}" x2="${xe}" y2="${yy+8}" stroke="${colors[owner]}" stroke-width="2" opacity=".55"/><circle cx="${xe}" cy="${yy+8}" r="3" fill="${colors[owner]}"/><rect x="${Math.min(xx+4,right-190)}" y="${yy-2}" width="188" height="14" fill="#111714" opacity=".9"/><text x="${Math.min(xx+6,right-188)}" y="${yy+8}" font-size="8.5" style="fill:${colors[owner]}">${esc(short(t.agent.split('/')[1],29))}</text></a>`;
  });
 });
 $('#timeline').innerHTML=svg;
 renderMomentum();
}
function visibleNodes(){return D.findings.filter(n=>owners.has(n.owner)&&(allStudies||n.featured||n.hub?.active_runs>0))}
function renderMap(){
 const centers={identity:[205,155],provenance:[540,155],memory:[840,345],verification:[465,440],metascience:[180,460]};
 const nodes=visibleNodes(), positions={}, groups={};
 D.themes.forEach(t=>groups[t.id]=nodes.filter(n=>n.themes[0]===t.id));
 Object.entries(groups).forEach(([theme,ns])=>{
  const [cx,cy]=centers[theme];
  ns.forEach((n,i)=>{const ring=Math.floor(i/14),count=Math.min(ns.length-ring*14,14),angle=(i%14)/count*Math.PI*2-Math.PI*.55,radius=78+ring*24;
   positions[n.id]=[cx+Math.cos(angle)*radius,cy+Math.sin(angle)*radius];
  });
 });
 let svg='<title>Themes and their evidence, colored by researcher and sized by evidence tier</title><defs><pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".65" fill="#384338"/></pattern></defs><rect width="1020" height="640" fill="url(#dots)" opacity=".4"/>';
 for(const n of nodes){const [nx,ny]=positions[n.id];for(const tid of n.themes){const [cx,cy]=centers[tid];svg+=`<line class="theme-link" x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}" opacity="${tid===n.themes[0]?.toString()?'.8':'.3'}"/>`}}
 D.transfers.forEach(e=>{if(positions[e.from]&&positions[e.to]){const [x,y]=positions[e.from],[xx,yy]=positions[e.to];svg+=`<path class="cross-link" d="M ${x} ${y} Q ${(x+xx)/2} ${(y+yy)/2-85} ${xx} ${yy}"><title>${esc(e.kind)}: ${esc(e.note)}</title></path>`}});
 D.themes.forEach((t,i)=>{const [cx,cy]=centers[t.id];svg+=`<g><circle cx="${cx}" cy="${cy}" r="44" fill="#172019" stroke="#475444"/><text x="${cx}" y="${cy+8}" text-anchor="middle" font-family="Doto" font-size="27" style="fill:#c5d5a9">0${i+1}</text><rect x="${cx-130}" y="${cy+113}" width="260" height="42" fill="#111714" opacity=".93"/><text class="theme-name" x="${cx}" y="${cy+129}" text-anchor="middle">${esc(t.label)}</text><text class="theme-question" x="${cx}" y="${cy+147}" text-anchor="middle">${esc(t.question)}</text></g>`});
 nodes.forEach(n=>{const [x,y]=positions[n.id],r=4+n.strength*10,isSelected=selected===n.id;
  const label=n.featured?short(n.label,26):'';
  svg+=`<g class="satellite" role="button" tabindex="0" data-node="${esc(n.id)}" aria-label="${esc(n.label)}, ${esc(names[n.owner])}, ${esc(n.strength_label)}"><title>${esc(n.label)} / ${esc(n.strength_label)}</title>${isSelected?`<circle cx="${x}" cy="${y}" r="${r+5}" fill="none" stroke="${colors[n.owner]}"/>`:''}<circle cx="${x}" cy="${y}" r="${r}" fill="${n.strength?colors[n.owner]:'#111714'}" stroke="${colors[n.owner]}" stroke-width="1.5"/>${label?`<text class="sat-label" x="${x}" y="${y+r+15}" text-anchor="middle">${esc(label)}</text>`:''}</g>`;
 });
 $('#theme-map').innerHTML=svg;
 $('#graph-count').textContent=`${nodes.length} / ${D.findings.length} study, review & lane nodes · ${D.themes.length} themes`;
 $('#show-all').textContent=allStudies?'Show focused map':'Show every node';
 $$('#theme-map [data-node]').forEach(g=>{const go=()=>selectNode(g.dataset.node);g.addEventListener('click',go);g.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();go()}})});
}
function selectNode(id,scroll=false){
 selected=id;const n=nodeMap.get(id);if(!n)return;
 $('#inspector').innerHTML=`<p class="eyebrow" style="color:${colors[n.owner]}">${esc(names[n.owner])} / ${esc(n.type)}</p><h3>${esc(n.label)}</h3><div>${statusBadge(n)} <span class="evidence-tier">${esc(n.strength_label)}</span></div><p class="claim">${esc(n.claim)}</p><div><span class="label">Units, not activity</span><p>${esc(n.sample)}</p></div><div><span class="label">Keep the limits attached</span><p class="limit">${esc(n.limits)}</p></div>${n.audit?`<div><span class="label">External arithmetic check</span><p class="limit">${esc(n.audit.scope)}</p>${safeLink(n.audit.url,'Read the check')}</div>`:''}<div><span class="label">Source at this snapshot</span><p>${safeLink(n.source.url,'Open study')}</p>${n.support.slice(0,2).map(p=>safeLink(p.url,short(p.path.split('/').slice(-2).join('/'),30))).join('<br>')}<p class="caption">Assessment: ${esc(n.assessment_date||'source-specific')}. Hub: ${n.hub?`${n.hub.active_runs} active runs${n.hub.stale_active_runs?' ('+n.hub.stale_active_runs+' stale)':''}. Execution only.`:'unavailable / not matched.'}</p></div>`;
 renderMap();if(scroll)$('#map-section').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});
}
function calculate(h){
 const values=Object.values(h.owner_strengths).filter(x=>x>0),ev=values.length?values.reduce((a,b)=>a+b,0)/values.length:0;
 const components={evidence:ev,brief_fit:h.brief_fit,coverage:values.length/3,readiness:h.readiness*h.evidence_present.length/h.evidence_ids.length};
 let score=100;for(const [k,v] of Object.entries(components))score*=v**weights[k];return {...h,components,score};
}
function renderScores(){
 const hs=D.headlines.map(calculate).sort((a,b)=>b.score-a.score),best=hs[0];
 $('#lead-title').textContent=best.short;
 $('#lead-description').textContent=best.title;
 $('#scorecards').innerHTML=hs.map((h,i)=>`<article class="scorecard ${i===0?'best':''}"><div class="score-rank">0${i+1}</div><div><h3>${esc(h.title)}</h3><div class="components">${Object.entries(h.components).map(([k,v])=>`<div class="component">${esc(k.replace('_',' '))}<b>${v.toFixed(2)}</b><div class="track"><span style="width:${pct(v)}"></span></div></div>`).join('')}</div><div class="evidence-links">${h.evidence_present.map(id=>{const n=nodeMap.get(id);return `<button data-evidence="${esc(id)}" style="--owner-color:${colors[n.owner]}">${esc(n.label)}</button>`}).join('')}</div><details class="score-details"><summary>Evidence, gaps & what needs to land</summary><div class="score-detail-grid"><div><h4>WHY THIS PACKAGE</h4><p>${esc(h.fit_reason)}</p><p>${esc(h.readiness_reason)}</p><h4>EVIDENCE BALANCE</h4>${Object.entries(h.owner_strengths).map(([owner,val])=>`<p>${esc(names[owner])}: ${val.toFixed(2)} strongest selected tier</p>`).join('')}${h.missing_evidence.length?`<p>Missing artifacts: ${esc(h.missing_evidence.join(', '))}</p>`:''}</div><div><h4>WHAT IT DOES NOT ESTABLISH</h4><ul>${h.gaps.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><h4>BEFORE 23:00 UTC</h4><ul>${h.land_by_23.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div></div></details></div><div class="score-value">${h.score.toFixed(1)}<small>/ 100<br>editorial score</small></div></article>`).join('');
 $$('[data-evidence]').forEach(b=>b.addEventListener('click',()=>{owners.add(nodeMap.get(b.dataset.evidence).owner);renderFilters();selectNode(b.dataset.evidence,true)}));
}
function renderFilters(){
 $('#owner-filters').innerHTML=Object.keys(names).map(o=>`<button aria-pressed="${owners.has(o)}" data-owner="${o}" style="--owner-color:${colors[o]}"><span class="swatch"></span>${esc(names[o])}</button>`).join('');
 $$('[data-owner]').forEach(b=>b.addEventListener('click',()=>{const o=b.dataset.owner;if(owners.has(o)){if(owners.size===1)return;owners.delete(o)}else owners.add(o);renderFilters();renderMap()}));
}
function renderDirections(){
 $('#researchers').innerHTML=D.researchers.map(r=>{
  const threads=D.threads.filter(t=>t.owner===r.id).sort((a,b)=>b.commits_3h-a.commits_3h||b.commits_12h-a.commits_12h);
  return `<article class="direction" style="--owner-color:${colors[r.id]}"><div><h3>${esc(r.name)}</h3><p class="meta">${r.active_threads_3h} active lanes / 3h<br>${r.active_threads_12h} active lanes / 12h</p></div><div><p>${esc(r.direction)}</p><div class="source-links">${r.sources.map((s,i)=>safeLink(s.url,`${String(i+1).padStart(2,'0')} / ${short(s.path.split('/').slice(-2).join('/'),36)}`)).join('')}</div><details class="thread-details"><summary>Inspect ${threads.length} recent lanes & their latest receipts</summary><div class="thread-list">${threads.map(t=>`<div class="thread-row"><div>${safeLink(t.latest.url,t.label)}<small>${esc(t.agent)} · ${esc(short(t.latest.subject,130))}</small>${t.blockers.map(b=>`<p>${esc(b)}</p>`).join('')}${t.stale_claim?'<small>Claim update is older than 3h. Not proof of an active worker.</small>':''}</div><span class="mono">${t.commits_3h} / 3h<br>${t.commits_12h} / 12h</span></div>`).join('')}</div></details><p class="caption">${esc(r.direction_kind)}</p></div></article>`;
 }).join('');
}
function renderLedger(){
 const term=$('#search').value.toLowerCase().trim();
 const matches=D.findings.filter(n=>n.type!=='thread'&&[n.id,n.title,n.owner,n.claim,...n.themes].join(' ').toLowerCase().includes(term)).sort((a,b)=>b.strength-a.strength||a.owner.localeCompare(b.owner));
 const ns=term||ledgerAll?matches:matches.slice(0,15);
 $('#ledger-toggle').hidden=Boolean(term)||matches.length<=15;
 $('#ledger-toggle').textContent=ledgerAll?'Show first 15':'Show all '+matches.length+' studies & reviews';
 $('#ledger').innerHTML=ns.length?ns.map(n=>`<div class="ledger-row" style="--owner-color:${colors[n.owner]}"><span class="owner">${esc(names[n.owner])}</span><div>${safeLink(n.source.url,n.title)}<br>${statusBadge(n)}</div><div class="sample">${esc(n.sample)}</div><div class="tier">${esc(n.strength_label)}<br>${n.evidence_score!=null?`registry ${n.evidence_score}/4`:'not a registry score'}</div></div>`).join(''):'<p class="ledger-empty">No matching studies. Try a researcher, theme or study name.</p>';
}
async function init(){
 try{
  const response=await fetch('narrative.json',{cache:'no-store'});if(!response.ok)throw new Error(`Snapshot returned HTTP ${response.status}`);D=await response.json();
  nodeMap=new Map(D.findings.map(n=>[n.id,n]));weights={...D.weights};
  $('#snapshot-sha').textContent=D.source_commit.slice(0,8);$('#snapshot-sha').href='https://github.com/dmarzzz/swarm-lab/tree/'+D.source_commit;
  $('#snapshot-time').textContent=fmtTime(D.as_of);
  const age=(Date.now()-Date.parse(D.as_of))/3600000,closed=Date.now()>Date.parse(D.deadline);
  $('#freshness').textContent=closed?'Archive snapshot · refresh window ended at 23:00 UTC.':age>1.25?'Snapshot older than 75 min. Read source receipts before acting.':'Refresh target / every 45 min · final cutoff 23:00 UTC';
  if(age>1.25&&!closed)$('#freshness').classList.add('stale');
  $('#formula').textContent=D.method.score_formula;$('#score-warning').textContent=D.method.warning;
  $('#weights').innerHTML=Object.keys(weights).map(k=>`<label>${esc(k.replace('_',' '))}<input type="number" min="0" max="3" step="0.25" value="${weights[k]}" data-weight="${k}" aria-label="${esc(k.replace('_',' '))} weight"></label>`).join('');
  $$('[data-weight]').forEach(input=>input.addEventListener('input',()=>{const v=Number(input.value);if(input.value!==''&&Number.isFinite(v)&&v>=0&&v<=3){weights[input.dataset.weight]=v;renderScores()}}));
  $('#reset-weights').addEventListener('click',()=>{weights={...D.weights};$$('[data-weight]').forEach(i=>i.value=weights[i.dataset.weight]);renderScores()});
  $('#rubric').innerHTML=Object.entries(D.method.strength_rubric).map(([k,v])=>`<span>${esc(k)} = ${v.toFixed(2)}</span>`).join('');
  $('#transfers').innerHTML=D.transfers.map(t=>`<div class="transfer-item">${safeLink(t.url,t.kind)}<p>${esc(t.note)}</p></div>`).join('');
  $('#builder-link').href='https://github.com/dmarzzz/swarm-lab/blob/'+D.source_commit+'/researchers/shadow/notes/narrative/README.md';
  $('#footer-provenance').textContent=`${Object.keys(D.provenance.files).length} hashed inputs · ${D.provenance.model_calls} model calls`;
  $$('[data-hours]').forEach(b=>b.addEventListener('click',()=>{hours=Number(b.dataset.hours);$$('[data-hours]').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b))});renderTimeline()}));
  $('#show-all').addEventListener('click',()=>{allStudies=!allStudies;renderMap()});$('#search').addEventListener('input',renderLedger);$('#ledger-toggle').addEventListener('click',()=>{ledgerAll=!ledgerAll;renderLedger()});
  renderFilters();renderTimeline();renderScores();renderDirections();renderLedger();selectNode(nodeMap.has('sybil-split-opus')?'sybil-split-opus':D.findings[0].id);
  window.narrativeReady=true;window.narrativeScores=D.headlines.map(calculate);
 }catch(error){$('#load-error').hidden=false;$('#load-error').textContent='The evidence snapshot could not be loaded. '+error.message+'. The repository remains the source of truth.';$('#lead-title').textContent='Evidence unavailable.'}
}
init();
