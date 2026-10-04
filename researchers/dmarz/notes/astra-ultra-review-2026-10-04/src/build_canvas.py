#!/usr/bin/env python3
"""Render the source-backed review to a self-contained, offline Codex canvas."""
import json
import argparse
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=BASE / 'src/out/review.canvas.tsx')
OUTPUT = parser.parse_args().output
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
review = json.loads((BASE / 'evidence.json').read_text())
assert [f['rank'] for f in review['findings']] == list(range(1, 11))
for finding in review['findings']:
    for key in ['question', 'learning', 'agents', 'rounds', 'sample', 'time', 'caveat', 'sources']:
        assert finding[key], (finding['rank'], key)
    for source in finding['sources']:
        subprocess.run(['git', 'cat-file', '-e', review['snapshot'] + ':' + source], cwd=BASE, check=True, stdout=subprocess.DEVNULL)

TEMPLATE = '''import { useState, useHostTheme, Stack, Row, Grid, H1, H2, H3, Text, Button, Pill, Divider, Table, BarChart, Link, type ChartSeries } from "cursor/canvas";

type Finding = { rank: number; title: string; question: string; learning: string; agents: string; rounds: string; sample: string; time: string; time_short: string; caveat: string; strength: string; sources: string[]; chart?: { title: string; axis: string; categories: string[]; series: ChartSeries[] } };
type Review = { reviewer: string; title: string; snapshot: string; cutoff: string; method: string; units: string; findings: Finding[]; also_reviewed: string[] };
const REVIEW: Review = __DATA__;
const sourceUrl = (path: string) => `https://github.com/dmarzzz/swarm-lab/blob/${REVIEW.snapshot}/${path}`;

export default function SwarmResults() {
  const theme = useHostTheme();
  const [selected, setSelected] = useState(1);
  const [view, setView] = useState("findings");
  const item = REVIEW.findings[selected - 1];
  return <Stack gap={20} style={{ maxWidth: 1150, margin: "0 auto", padding: 26, color: theme.text.primary, background: theme.bg.editor }}>
    <Stack gap={8}>
      <Text size="small" tone="secondary">SWARM LAB · RESULTS REVIEW · {REVIEW.cutoff}</Text>
      <H1>{REVIEW.title}</H1>
      <Text size="small" tone="secondary">Review and ranking by {REVIEW.reviewer}. Underlying experiments by Swarm Lab researchers dmarz, vishesh and shadow.</Text>
      <Text>More agents, more checking and faster recovery often failed to improve the outcome that mattered. These ten findings show where that happened—and where a simple intervention worked.</Text>
      <Row gap={8} wrap><Pill>10 ranked findings</Pill><Pill>Existing evidence only</Pill><Pill>All exploratory</Pill></Row>
    </Stack>
    <Row gap={8} wrap>
      <Button variant={view === "findings" ? "primary" : "secondary"} onClick={() => setView("findings")}>Ranked findings</Button>
      <Button variant={view === "scale" ? "primary" : "secondary"} onClick={() => setView("scale")}>Agents, rounds and time</Button>
      <Button variant={view === "coverage" ? "primary" : "secondary"} onClick={() => setView("coverage")}>Coverage and limits</Button>
    </Row>
    <Divider />
    {view === "findings" && <Grid columns="minmax(220px, 0.85fr) minmax(0, 2fr)" gap={26} align="start">
      <Stack gap={0}>
        {REVIEW.findings.map(f => <button key={f.rank} onClick={() => setSelected(f.rank)} aria-pressed={selected === f.rank} style={{ textAlign: "left", cursor: "pointer", font: "inherit", lineHeight: 1.4, border: 0, borderBottom: `1px solid ${theme.stroke.tertiary}`, padding: "13px 12px", color: selected === f.rank ? theme.accent.primary : theme.text.secondary, background: selected === f.rank ? theme.fill.secondary : theme.bg.editor }}>
          <span style={{ display: "inline-block", minWidth: 24, fontVariantNumeric: "tabular-nums" }}>{String(f.rank).padStart(2, "0")}</span>{f.title}
        </button>)}
      </Stack>
      <Stack gap={18}>
        <Stack gap={7}><Text size="small" tone="secondary">#{item.rank} · {item.strength}</Text><H2>{item.title}</H2></Stack>
        <Stack gap={5}><H3>Question we studied</H3><Text>{item.question}</Text></Stack>
        <Stack gap={5}><H3>What we learned</H3><Text>{item.learning}</Text></Stack>
        {item.chart && <Stack gap={7} style={{ padding: 16, background: theme.fill.quaternary }}>
          <H3>{item.chart.title}</H3>
          <Text size="small" tone="secondary">{item.chart.axis}</Text>
          <BarChart categories={item.chart.categories} series={item.chart.series} height={230} showValues />
          <Text size="small" tone="tertiary">Source: <Link href={sourceUrl(item.sources[0])}>native study report</Link> · experiments reported 4 October 2026. Descriptive values; uncertainty and sampling limits are stated below.</Text>
        </Stack>}
        <Stack gap={7}><H3>Executed scale and duration</H3>
          <Table framed={false} headers={["Dimension", "What actually ran"]} rows={[["Agents", item.agents], ["Rounds / steps", item.rounds], ["Sample", item.sample], ["Time", item.time]]} />
        </Stack>
        <Stack gap={5} style={{ borderLeft: `2px solid ${theme.stroke.primary}`, paddingLeft: 14 }}><H3>How far the finding goes</H3><Text tone="secondary">{item.caveat}</Text></Stack>
        <Stack gap={5}><H3>Sources at the reviewed snapshot</H3>{item.sources.map((p, i) => <Text key={p} size="small"><Link href={sourceUrl(p)}>{i + 1}. {p.replace("researchers/", "")}</Link></Text>)}</Stack>
      </Stack>
    </Grid>}
    {view === "scale" && <Stack gap={14}>
      <H2>Executed scale, not planned scale</H2>
      <Text tone="secondary">{REVIEW.units}</Text>
      <Table headers={["Rank / finding", "Agents", "Rounds / steps", "Time"]} striped rows={REVIEW.findings.map(f => [<Link key={f.rank} href={sourceUrl(f.sources[0])}>{f.rank}. {f.title}</Link>, f.agents, f.rounds, f.time_short])} />
      <Text size="small" tone="secondary">Missing batch durations are not estimated from budgets, timestamps of publication or sums of overlapping world durations. Open each ranked finding for exact sample counts and full timing scope.</Text>
    </Stack>}
    {view === "coverage" && <Stack gap={16}>
      <H2>How this list was selected</H2><Text>{REVIEW.method}</Text>
      <Text>{REVIEW.units}</Text>
      <H3>Other evidence considered</H3>
      {REVIEW.also_reviewed.map((text, i) => <div key={i} style={{ display: "grid", gridTemplateColumns: "24px 1fr", gap: 8, paddingBottom: 12, borderBottom: `1px solid ${theme.stroke.tertiary}` }}><Text size="small" tone="tertiary">{i + 1}</Text><Text>{text}</Text></div>)}
      <Text size="small" tone="tertiary">Published repository snapshot: <Link href={`https://github.com/dmarzzz/swarm-lab/tree/${REVIEW.snapshot}`}>{REVIEW.snapshot.slice(0, 8)}</Link>. Sources are pinned to this snapshot and listed in the review’s provenance. Later unpublished runs are outside the cutoff.</Text>
    </Stack>}
  </Stack>;
}
'''
OUTPUT.write_text(TEMPLATE.replace('__DATA__', json.dumps(review, ensure_ascii=False, indent=2)))
print(OUTPUT)
