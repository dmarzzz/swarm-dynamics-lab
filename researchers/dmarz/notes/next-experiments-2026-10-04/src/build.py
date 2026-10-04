"""Render the reviewed planning data as repository Markdown and a local Codex canvas."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
REV = '45390d685aedc535d8a3e5959df9270c5e6bb7e0'
GITHUB = f'https://github.com/dmarzzz/swarm-lab/blob/{REV}/'

def source_url(source):
    if source.startswith('https://'):
        return source
    assert (ROOT / source).is_file(), source
    return GITHUB + source

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--canvas', type=Path)
    args = ap.parse_args()
    plan = json.loads((HERE / 'plan.json').read_text())
    sections = [('reason','Why this follows'),('question','Question'),('comparison','Comparison'),
                ('scale','Proposed scale and sequence'),('unit','Independent unit'),
                ('primary','Primary measurement'),('decision','Proposed decision rule'),
                ('gate','Prerequisites'),('visual','Visualization')]
    md = [f"# {plan['title']}", plan['recommendation'],
          '**Status:** '+plan['status'], '**Evidence cutoff:** '+plan['snapshot'],
          'Prepared by dmarz/pi-next-experiments at the user’s request. Numerical sample sizes, resource regimes and useful-effect margins below are proposed planning choices, not established thresholds. The live snapshot is a timestamped observation, not a promise about current execution state.',
          '## First finish or reconcile existing work']
    for item in plan['active']:
        md += [f"### {item['study']}", item['state'], item['action'], f"[Existing protocol]({source_url(item['source'])})."]
    md += ['## Proposed successor experiments']
    for study in plan['studies']:
        md += [f"### {study['priority']} {study['name']}", f"Extends: {study['extends']}."]
        for key,label in sections:
            md += [f"**{label}.** {study[key]}"]
        md += ['Evidence: '+', '.join(f"[source {i+1}]({source_url(src)})" for i,src in enumerate(study['sources']))+'.']
    md += ['## Shared design and decision rules']
    md += [f'{i+1}. {item}' for i,item in enumerate(plan['methods'])]
    md += ['## Directions to retain without immediate broad expansion']+plan['deferred']
    md += ['## Recommended order']+plan['sequence']
    md += ['## Methods and prior work anchors',
           'These anchors inform the design and its limitations. They do not establish the novelty or effectiveness of the proposed successors.']
    md += [f'- [{src.rsplit("/",1)[-1]}]({source_url(src)})' for src in plan['method_sources']]
    md += ['## Reproduction and scope',
           'The adjacent `plan.json` is the structured source; `src/build.py` renders this document and an optional local interactive view. `live-evidence.json` retains a selected public experiment/run snapshot used for this plan. It excludes fleet, claim and infrastructure fields. No experiments were launched, task ownership reassigned, or model requests made in preparing the recommendations. The plan must be converted into owner-reviewed pre-run protocols before execution.']
    (HERE / 'README.md').write_text('\n\n'.join(md)+'\n')
    for study in plan['studies']:
        study['sources'] = [source_url(s) for s in study['sources']]
    for item in plan['active']:
        item['source']=source_url(item['source'])
    if args.canvas:
        tsx = '''import {Stack,Row,Grid,H1,H2,Text,Table,Button,Link,useState,useHostTheme} from "cursor/canvas";
const plan = PLAN_DATA;
const labels = FIELD_LABELS;
export default function NextExperiments(){
 const theme=useHostTheme();
 const [selected,setSelected]=useState(plan.studies[0].id);
 const current=plan.studies.find(s=>s.id===selected)||plan.studies[0];
 return <Stack gap={20} style={{padding:24,maxWidth:1200,margin:"0 auto",color:theme.text.primary,background:theme.bg.editor}}>
  <H1>{plan.title}</H1>
  <Text>{plan.recommendation}</Text>
  <Text tone="secondary">{plan.status} {plan.snapshot}</Text>
  <Grid columns="repeat(auto-fit,minmax(220px,1fr))" gap={20}>
   <Stack gap={6}><H2>First complete</H2><Text>Use the current V3, Sybil scale, receipt-verification and repair results before launching successors.</Text></Stack>
   <Stack gap={6}><H2>Then discriminate</H2><Text>Test memory safeguards, selective continuity, fixed attacker resources and imperfect receipts.</Text></Stack>
   <Stack gap={6}><H2>Scale the right axis</H2><Text>More agents, more independent tasks, longer horizons and more compute answer different questions.</Text></Stack>
  </Grid>
  <H2>Recommended portfolio</H2>
  <Table headers={["Priority","Study — select for details","Builds on"]} rows={plan.studies.map(s=>[s.priority,<Button key={s.id} variant={s.id===selected?"primary":"ghost"} onClick={()=>setSelected(s.id)}>{s.name}</Button>,s.extends])}/>
  <Stack gap={14} style={{padding:20,background:theme.fill.quaternary,borderTop:`1px solid ${theme.stroke.primary}`}}>
   <H2>{current.name}</H2>
   {labels.map(([key,label])=><Text key={key}><strong>{label}. </strong>{current[key as keyof typeof current] as string}</Text>)}
   <Row gap={14} wrap>{current.sources.map((s,i)=><Link key={s} href={s}>Evidence {i+1}</Link>)}</Row>
  </Stack>
  <H2>Existing work to finish first</H2>
  <Table headers={["Study","Observed state at cutoff","Next action"]} rows={plan.active.map(s=>[<Link href={s.source}>{s.study}</Link>,s.state,s.action])}/>
  <H2>Shared design and stopping rules</H2>
  {plan.methods.map((m,i)=><Text key={m}><strong>{i+1}. </strong>{m}</Text>)}
  <H2>Recommended order</H2>
  {plan.sequence.map(s=><Text key={s}>{s}</Text>)}
  <H2>Retained directions</H2>
  {plan.deferred.map(s=><Text key={s}>{s}</Text>)}
  <Link href="https://github.com/dmarzzz/swarm-lab/blob/main/researchers/dmarz/notes/next-experiments-2026-10-04/README.md">Full plan on GitHub</Link>
 </Stack>;
}
'''.replace('PLAN_DATA',json.dumps(plan,ensure_ascii=False)).replace('FIELD_LABELS',json.dumps(sections))
        args.canvas.write_text(tsx)
    print(f'Rendered {len(plan["studies"])} successor designs and {len(plan["active"])} current-work dependencies.')

if __name__=='__main__':
    main()
