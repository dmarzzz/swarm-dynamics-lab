"""Render the benchmark suitability review with source links beside each finding."""
from pathlib import Path
import json

base = Path(__file__).resolve().parents[1]
data = json.loads((base / 'review.json').read_text())
template = '''import { Stack, Row, H1, H2, Text, Table, Link, Button, useState, useHostTheme } from "cursor/canvas";
const data = __DATA__;
export default function EvalReview() {
 const theme = useHostTheme();
 const [selected, setSelected] = useState("BrowseComp-Plus");
 const c = data.candidates.find(x => x.name === selected)!;
 return <Stack gap={18} style={{padding:28,maxWidth:1150,margin:"0 auto",color:theme.text.primary}}>
   <Text style={{color:theme.text.secondary}}>SWARM LAB · EVALUATOR AUDIT · {data.date}</Text>
   <H1>{data.title}</H1>
   <Text weight="semibold">{data.decision}</Text>
   <Text>{data.scope}</Text>
   <Table headers={["Benchmark", "Fit", "Disposition"]}
     rows={data.candidates.map(x => [x.name, x.group, x.verdict])}/>
   <H2>Inspect the task and scorer</H2>
   <Row gap={8} wrap>{data.candidates.map(x => <Button key={x.name}
     variant={selected === x.name ? "primary" : "secondary"}
     onClick={() => setSelected(x.name)}>{x.name}</Button>)}</Row>
   <Stack gap={12} style={{padding:20,background:theme.fill.quaternary}}>
     <H2>{c.name}</H2><Text weight="semibold">{c.verdict}</Text>
     <Text><strong>Task: </strong>{c.task}</Text>
     <Text><strong>Score: </strong>{c.score}</Text>
     <Text><strong>What the audit found: </strong>{c.audit}</Text>
     <Text><strong>Required before use: </strong>{c.beforeUse}</Text>
     <Text><strong>Availability: </strong>{c.availability}</Text>
     <Row gap={12} wrap>{c.sources.map(s => <Link key={s.url} href={s.url}>{s.label}</Link>)}</Row>
   </Stack>
   <H2>Useful parts we already have</H2>
   <Table headers={["Instrument", "Reusable evidence", "Limit"]} rows={data.localComponents.map(x => [
     <Link key={x.name} href={x.source}>{x.name}</Link>, x.reuse, x.limit])}/>
   <H2>Recommendation and remaining decision</H2>
   <Text>{data.recommendation}</Text><Text>{data.openDecision}</Text>
   <Text style={{color:theme.text.secondary}}>{data.method}</Text>
   <Link href="/Users/halcyon/swarm-lab/researchers/dmarz/notes/eval-search-2026-10-04/fixture-audit.json">Reproducible fixed-fixture results</Link>
 </Stack>;
}
'''
out = Path('/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/evaluation-shortlist.canvas.tsx')
out.write_text(template.replace('__DATA__', json.dumps(data, ensure_ascii=False)))
print(out)
