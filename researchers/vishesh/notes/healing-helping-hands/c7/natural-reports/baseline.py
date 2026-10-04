"""Visible-prose extraction and deterministic scope/vintage reconciliation; no network."""
import re
MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']
def extract(source):
 text=' '.join(source['excerpt'].split());date=source['published'];out=[]
 def add(period,value,metric,span):out.append({'period':period,'value':float(value.replace(',','')),'metric':metric,'published':date,'source_id':source['id'],'span':span,'geography':'US','publisher':source['publisher']})
 if source['publisher']=='BEA':
  m=re.search(r'Real gross domestic product \(GDP\) increased at an annual rate of ([0-9.]+) percent in the (first|second|third|fourth) quarter of (\d{4})',text)
  if m:add(f'{m[3]}-Q{("first","second","third","fourth").index(m[2])+1}',m[1],'real_gdp_qoq_annualized_percent',m[0])
 elif source['publisher']=='BLS':
  def period(month):
   i=MONTHS.index(month)+1;y=int(date[:4])-(i>int(date[5:7]));return f'{y}-{i:02}'
  m=re.search(r'Total nonfarm payroll employment rose by ([\d,]+) in (\w+)',text)
  if m:add(period(m[2]),m[1],'nonfarm_payroll_monthly_change_jobs',m[0])
  for m in re.finditer(r'change(?: in total nonfarm payroll employment)? for (\w+) was revised (?:up|down) by [\d,]+, from \+([\d,]+) to \+([\d,]+)',text):add(period(m[1]),m[3],'nonfarm_payroll_monthly_change_jobs',m[0])
 return out

def reconcile(query,sources):
 records=[r for s in sources if s['published']<=query['cutoff'] for r in extract(s) if all(r[k]==query[k] for k in ('publisher','metric','period','geography'))]
 if not records:return {'label':'UNCERTAIN','reason':'no applicable measurement in supplied packet','evidence':[]}
 latest=max(r['published'] for r in records);records=[r for r in records if r['published']==latest]
 values={r['value'] for r in records}
 if len(values)!=1:return {'label':'UNCERTAIN','reason':'same-vintage unresolved conflict','evidence':records}
 return {'label':'SUPPORT' if next(iter(values))==query['value'] else 'REFUTE','reason':'latest applicable supplied vintage','evidence':records}

def actor_input(case,sources):
 allowed=('id','publisher','published','url','excerpt')
 return {'instruction':'Evaluate the query using only supplied excerpts. Interpret latest as latest applicable supplied vintage at or before cutoff. A revision supersedes an earlier estimate; different scope is not contradiction. Return SUPPORT, REFUTE or UNCERTAIN with source IDs and verbatim evidence span. Do not infer absent measurements.','query':dict(case['query']),'sources':[{k:s[k] for k in allowed} for s in sources if s['id'] in case['source_ids']]}
