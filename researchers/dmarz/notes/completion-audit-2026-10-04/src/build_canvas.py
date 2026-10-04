"""Render the frozen completion audit as one offline Codex canvas.

Run build_audit.py first to refresh portfolio.json. This renderer makes no
network request, invokes no model, and changes no experimental evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
DEFAULT_OUTPUT = Path('/Users/halcyon/.cursor/projects/Users-halcyon-swarm-labs-agentops/canvases/completion-audit.canvas.tsx')

TEMPLATE = r'''import {
  useState, useMemo, useHostTheme, useCanvasAction,
  Stack, Row, Grid, H1, H2, H3, Text, Link, Button,
  Pill, Table, Divider, TextInput, Select, Card, CardHeader, CardBody,
} from "cursor/canvas";

type Attempt = {
  key: string; id: string; family: string; attempt: string;
  kind_group: string; model: string; backend?: string;
  counts: Record<string, number | null>; [key: string]: any;
};
type Portfolio = {
  source_freeze: string; cutoff_utc: string; inventory_rows: number;
  kind_counts: Record<string, number>; definitions: Record<string, string>;
  attempts: Attempt[];
};
const DATA: Portfolio = __PORTFOLIO__;
const ROOT = __ROOT__;
const REPORT = __REPORT__;
const PROVENANCE = __PROVENANCE__;
const COUNTS = ["planned", "started", "terminal", "valid", "completed", "incomplete", "refused", "errored", "missing"];
const LABELS: Record<string, string> = {
  planned: "Planned", started: "Started", terminal: "Terminal records",
  valid: "Structurally valid", completed: "Completed endpoint",
  incomplete: "Incomplete", refused: "Explicit refusal", errored: "Error / invalid",
  missing: "Missing endpoint at cutoff",
};
const human = (s: any): string => {
  if (s === null || s === undefined) return "Unknown / not applicable";
  if (typeof s === "string") return s.replace(/_/g, " ");
  if (typeof s === "number" || typeof s === "boolean") return String(s);
  return JSON.stringify(s);
};
const count = (n: any): string => typeof n === "number" ? n.toLocaleString() : "—";
const asList = (v: any): string[] => {
  if (!v) return [];
  if (typeof v === "string") return [v];
  if (Array.isArray(v)) return v.map(human);
  return Object.entries(v).map(([k, val]) => `${human(k)}: ${human(val)}`);
};

function Notes({ title, value }: { title: string; value: any }) {
  const items = asList(value);
  return items.length ? <Stack gap={5}>
    <H3>{title}</H3>
    {items.map((item, i) => <Text key={i} size="small" tone="secondary">{item}</Text>)}
  </Stack> : null;
}

function Sources({ rows }: { rows: any[] }) {
  const open = useCanvasAction();
  const [all, setAll] = useState(false);
  const unique = rows.filter((s, i) => rows.findIndex(t => (t.url || t.immutable_link || t.path) === (s.url || s.immutable_link || s.path)) === i);
  const visible = all ? unique : unique.slice(0, 8);
  return unique.length ? <Stack gap={6}>
    <H3>Evidence and source links</H3>
    {visible.map((s, i) => {
      const href = s.url || s.immutable_link || s.immutable_url;
      const path = s.path || s.file || "Retained evidence";
      const lines = s.lines ? ` · lines ${s.lines.join("–")}` : "";
      const label = `${path.split("/").slice(-3).join("/")}${lines}`;
      if (href && /^https?:/.test(href)) return <Text size="small" key={i}><Link href={href}>{label}</Link></Text>;
      const local = path.startsWith("/") || /^(researchers|data|tooling|docs|tasks)\//.test(path);
      return local ? <Row key={i}><Button variant="ghost" onClick={() => open({ type: "openFile", path: path.startsWith("/") ? path : `${ROOT}/${path}` })}>{label}</Button></Row>
        : <Text key={i} size="small" tone="tertiary">{label}</Text>;
    })}
    {unique.length > 8 && <Row><Button variant="ghost" onClick={() => setAll(!all)}>{all ? "Show fewer sources" : `Show all ${unique.length} sources`}</Button></Row>}
  </Stack> : null;
}

function Detail({ attempt: a }: { attempt: Attempt }) {
  const t = useHostTheme();
  const success = a.counts?.task_success ?? a.task_success ?? null;
  const coverage = a.evidence_coverage || a.evidencecoverage || a.coverage;
  const notes = a.count_overlap_notes || a.count_overlap || a.denominator_notes;
  return <Card>
    <CardHeader>{a.family} · {a.attempt}</CardHeader>
    <CardBody>
      <Stack gap={14}>
        <Row wrap gap={6}><Pill>{a.kind_group}</Pill><Pill>{human(a.qualification_label)}</Pill></Row>
        <Text weight="semibold">Unit: {a.count_unit || a.unit}</Text>
        <Text size="small" tone="secondary">{a.endpoint_definition}</Text>
        <Table
          headers={["Measure in the unit above", "Observed / planned count"]}
          rows={COUNTS.map(k => [LABELS[k], count(a.counts?.[k])]).concat([["Task success (separate criterion)", count(success)]])}
          columnAlign={["left", "right"]}
          framed={false}
        />
        <Text size="small" tone="tertiary">— means unknown or not applicable. Columns overlap. They are not parts of a single total.</Text>
        {a.task_success_definition && <Text size="small"><b>Task-success criterion:</b> {a.task_success_definition}</Text>}
        <Notes title="Count interpretation" value={notes} />
        <Notes title="Success components / additional endpoints" value={a.task_success_by_component || a.task_success_other_endpoints} />
        <Notes title="Model and backend" value={`${a.model} · ${a.backend || "backend not separately recorded"}`} />
        <Notes title="Qualification" value={a.qualification} />
        <Notes title="Observed behavior" value={a.stalling_behavior} />
        <Notes title="What these observations support" value={a.conclusions || a.scientific_conclusions || a.scientific_interpretation} />
        <Notes title="Independent unit" value={a.independent_unit} />
        <Notes title="Evidence coverage" value={coverage} />
        <Notes title="Cause confidence" value={a.causes} />
        <Notes title="Smallest diagnostic" value={a.smallest_diagnostic} />
        <Notes title="Falsifier" value={a.falsifier} />
        <Notes title="Acceptance criterion" value={a.acceptance} />
        <Sources key={a.key} rows={a.sources || []} />
        <Text size="small" style={{ color: t.text.tertiary }}>Attempt identity: {a.id}. Source record: {a.evidence_file || "compositional replay audit"}.</Text>
      </Stack>
    </CardBody>
  </Card>;
}

export default function CompletionAudit() {
  const t = useHostTheme();
  const open = useCanvasAction();
  const [query, setQuery] = useState("");
  const [family, setFamily] = useState("all");
  const [kind, setKind] = useState("all");
  const [selectedKey, setSelectedKey] = useState("compositional-safety/q0-004::q0-004");
  const families = useMemo(() => Array.from(new Set(DATA.attempts.map(a => a.family))).sort(), []);
  const filtered = useMemo(() => {
    const words = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
    return DATA.attempts.filter(a => (family === "all" || a.family === family) && (kind === "all" || a.kind_group === kind)
      && words.every(w => [a.family, a.attempt, a.id, a.model, a.backend, a.coverage, a.qualification_label, a.stalling_behavior].join(" ").toLowerCase().includes(w)));
  }, [query, family, kind]);
  const selected = filtered.find(a => a.key === selectedKey) || filtered[0];
  const focus = (targetFamily: string, targetAttempt: string) => {
    setFamily(targetFamily); setKind("model"); setQuery("");
    const a = DATA.attempts.find(x => x.family === targetFamily && x.attempt === targetAttempt);
    if (a) setSelectedKey(a.key);
  };
  const reset = () => { setQuery(""); setFamily("all"); setKind("all"); };
  const summaryRows = filtered.map(a => [
    <Stack gap={4} key={a.key}>
      <Text size="small" tone="tertiary">{a.family}</Text>
      <Button variant={selected?.key === a.key ? "primary" : "ghost"} onClick={() => setSelectedKey(a.key)}>{a.attempt}</Button>
    </Stack>,
    a.kind_group,
    <Stack gap={3} key="model"><Text size="small">{a.model}</Text>{a.backend && <Text size="small" tone="tertiary">{a.backend}</Text>}</Stack>,
    <Stack gap={3} key="counts"><Text size="small">{count(a.counts?.completed)} completed / {count(a.counts?.planned)} planned</Text><Text size="small" tone="tertiary">{a.count_unit || a.unit}</Text></Stack>,
    human(a.qualification_label),
    human(a.coverage),
  ]);
  return <Stack gap={22} style={{ padding: 24, maxWidth: 1600, margin: "0 auto" }}>
    <Stack gap={8}>
      <Text size="small" tone="tertiary">SWARM LABS · EVIDENCE REVIEW · 4 OCTOBER 2026</Text>
      <H1>Completion is not task success</H1>
      <Text>Two research families show directly observed prolonged nonprogress: compositional safety and Immune Response. This is a task-specific finding, not a portfolio failure rate. Ordinary baseline failures extend beyond those two families.</Text>
      <Text size="small" tone="tertiary">Source freeze {DATA.source_freeze.slice(0, 12)} · Hub cutoff: {DATA.cutoff_utc}</Text>
    </Stack>

    <Grid columns="repeat(auto-fit, minmax(min(100%, 310px), 1fr))" gap={28}>
      <Stack gap={9}>
        <H2>Latest compositional batch</H2>
        <Text><b>10 / 24 safely completed.</b> The remaining assignments include 12 valid but incomplete episodes and 2 explicit provider refusals.</Text>
        <Text size="small" tone="secondary">Ten trajectories inspect for all 40 turns despite available productive actions. Seven of the twelve incomplete episodes are benign controls. Neither a terminal record nor zero observed violations establishes competent safe completion.</Text>
        <Row><Button onClick={() => focus("compositional-safety", "q0-004")}>Inspect Q0-004 evidence</Button></Row>
      </Stack>
      <Stack gap={9}>
        <H2>A second nonprogress case</H2>
        <Text>Immune Response v3 returns valid actions while seven of nine incident trajectories wait through all six ticks and the service stays broken.</Text>
        <Text size="small" tone="secondary">Waiting is correct for the healthy control, so a generic “WAIT is failure” rule would be wrong. The solo control recovers incidents but introduces other failures.</Text>
        <Row><Button onClick={() => focus("immune-response-v3", "scenario-native-a2")}>Inspect incident trajectories</Button></Row>
      </Stack>
      <Stack gap={9}>
        <H2>Reporting can obscure the difference</H2>
        <Text>A done run can fail qualification. A failed run can contain complete, valid answers. A zero qualification field can mean “not applicable.”</Text>
        <Text size="small" tone="secondary">Failed starts, cancelled work, model refusals, valid abstentions and adverse scientific results stay separate here. No cross-row episode total is valid.</Text>
        <Row><Button onClick={() => open({ type: "openFile", path: REPORT })}>Read the full assessment</Button></Row>
      </Stack>
    </Grid>

    <Divider />
    <Stack gap={10}>
      <H2>Attempt inventory</H2>
      <Text size="small" tone="secondary">{DATA.inventory_rows} inventory entries include models, scripted rehearsals, diagnostics, repairs and unrun plans. Entries are not independent experiments. Select an attempt for all counts, endpoint definitions, qualification and evidence coverage.</Text>
      <Grid columns="repeat(auto-fit, minmax(min(100%, 190px), 1fr))" gap={12}>
        <Stack gap={4}><Text size="small" weight="semibold">Search evidence</Text><TextInput type="search" value={query} onChange={setQuery} placeholder="Attempt, model, status or behavior" /></Stack>
        <Stack gap={4}><Text size="small" weight="semibold">Research family / version</Text><Select value={family} onChange={setFamily} options={[{ value: "all", label: "All families and versions" }, ...families.map(f => ({ value: f, label: f }))]} /></Stack>
        <Stack gap={4}><Text size="small" weight="semibold">Execution kind</Text><Select value={kind} onChange={setKind} options={[{value:"all",label:"All kinds"},{value:"model",label:"Model executed / attempted"},{value:"scripted",label:"Scripted / engineering"},{value:"unrun",label:"Unrun plans"}]} /></Stack>
      </Grid>
      <Row justify="space-between" wrap><Text size="small" tone="tertiary">{filtered.length} matching entries · counts retain their own units</Text><Button variant="ghost" onClick={reset}>Reset filters</Button></Row>
    </Stack>

    {filtered.length > 0 && <Grid columns="minmax(0, 1fr)" gap={18}>
      <Table headers={["Family and attempt", "Kind", "Model / backend", "Execution endpoint", "Qualification", "Evidence coverage"]}
        rows={summaryRows} stickyHeader striped style={{ maxHeight: 520, overflow: "auto" }} />
      {selected && <Detail key={selected.key} attempt={selected} />}
    </Grid>}

    <Divider />
    <Stack gap={7}>
      <H2>How to read this audit</H2>
      <Text size="small" tone="secondary">Read each row’s unit before its counts. Completed usually means the planned protocol ended; some task-specific rows explicitly use functional completion. Task success is separately defined. Refusal requires explicit evidence; missing output, wrong answers and allowed abstention are not interchangeable with refusal.</Text>
      <Text size="small" tone="secondary">Evidence ranges from saved actor packets and responses to report-only history. Full serialized provider envelopes were not consistently retained. Unknowns remain unknown. Variants, retries, paired arms and engineering reruns do not create independent worlds.</Text>
      <Text size="small" tone="tertiary">Static, offline snapshot. No network or model calls occur in this view. Portfolio SHA-256: {PROVENANCE}.</Text>
      <Row><Button variant="ghost" onClick={() => open({ type: "openFile", path: `${ROOT}/researchers/dmarz/notes/completion-audit-2026-10-04/portfolio.json` })}>Open source inventory</Button></Row>
    </Stack>
  </Stack>;
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    source = HERE / 'portfolio.json'
    raw = source.read_bytes()
    data = json.loads(raw)
    assert data['attempts'], 'Do not generate an empty canvas'
    assert len({a['key'] for a in data['attempts']}) == len(data['attempts'])
    for a in data['attempts']:
        assert all(k in a['counts'] for k in ['planned', 'started', 'terminal', 'valid', 'completed', 'incomplete', 'refused', 'errored', 'missing']), a['key']
    text = TEMPLATE.replace('__PORTFOLIO__', json.dumps(data, ensure_ascii=True, separators=(',', ':')))
    text = text.replace('__ROOT__', json.dumps(str(ROOT)))
    text = text.replace('__REPORT__', json.dumps(str(HERE / 'README.md')))
    text = text.replace('__PROVENANCE__', json.dumps(hashlib.sha256(raw).hexdigest()))
    args.output.write_text(text)
    print(json.dumps({'canvas': str(args.output), 'inventory_rows': len(data['attempts']), 'portfolio_sha256': hashlib.sha256(raw).hexdigest(), 'canvas_sha256': hashlib.sha256(text.encode()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
