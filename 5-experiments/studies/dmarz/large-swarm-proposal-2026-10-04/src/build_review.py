"""Render the corrected evaluation disposition, omitting withdrawn budgets."""
from pathlib import Path
import json

base = Path(__file__).resolve().parents[1]
plan = json.loads((base / 'proposal.json').read_text())['plan']
template = """import { Stack, H1, H2, Text, Table, Link, useHostTheme } from "cursor/canvas";
const p = __PLAN__;
export default function EvalDisposition() {
  const theme = useHostTheme();
  return <Stack gap={18} style={{padding:28,maxWidth:1100,margin:"0 auto",color:theme.text.primary}}>
    <Text style={{color:theme.text.secondary}}>SWARM LAB · CORRECTED DISPOSITION · 4 OCTOBER 2026</Text>
    <H1>{p.title}</H1>
    <Text weight="semibold">{p.recommendation}</Text>
    <Text>{p.correction}</Text>
    <H2>What remains undefined</H2>
    <Table headers={["Evaluation question", "Evidence required — all unresolved"]}
      rows={p.evaluationBlockers.map(x => [x.gap, x.required])}/>
    <H2>The next decision</H2>
    <Text>{p.nextAction}</Text>
    <H2>Previous recommendation</H2>
    <Text>{p.retracted}</Text>
    <Text style={{color:theme.text.secondary}}>{p.executionStatus}</Text>
    <Stack gap={6}>{p.sources.map(s => <Link key={s.url} href={s.url}>{s.label}</Link>)}</Stack>
  </Stack>;
}
"""
out = Path('/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/large-swarm-experiment.canvas.tsx')
out.write_text(template.replace('__PLAN__', json.dumps(plan, ensure_ascii=False)))
print(out)
