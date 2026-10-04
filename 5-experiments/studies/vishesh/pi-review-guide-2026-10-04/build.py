#!/usr/bin/env python3
"""Build the self-contained dark PI guide from a compact guide and frozen review."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote


HERE = Path(__file__).resolve().parent
FROZEN = HERE.parent / "pi-review-2026-10-04"
SOURCE = FROZEN / "review-2026-10-04"
COMMIT = "baaccc040b0716b4074f6446580c380c72be456b"
GITHUB = f"https://github.com/dmarzzz/swarm-lab/blob/{COMMIT}/"
PUBLIC = "researchers/vishesh/notes/pi-review-2026-10-04/"
LABELS = {"idea": "Idea", "evidence": "Evidence", "scenarios": "Scenarios", "controls": "Controls"}
STATUSES = {"green": "Green · Sound", "yellow": "Yellow · Improve", "red": "Red · Blocked", "gray": "Gray · Unrun"}
MATRIX_STATUS = {"green": "Sound", "yellow": "Improve", "red": "Blocked", "gray": "Unrun"}


def esc(value):
    return escape(str(value), quote=True)


def label(value):
    return value.replace("_", " ").capitalize()


def badge(status, text, explanation=None):
    attributes = f' title="{esc(explanation)}" aria-label="{esc(explanation)}"' if explanation else ""
    return f'<span class="badge {esc(status)}"{attributes}><span class="dot" aria-hidden="true"></span>{esc(text)}</span>'


def source_html(item, source_map):
    path = item.get("path", "")
    candidate = (FROZEN / path).resolve()
    url, note = None, None
    if path and candidate.is_relative_to(FROZEN.resolve()) and candidate.is_file():
        url = GITHUB + quote(PUBLIC + path, safe="/")
        if isinstance(item.get("line"), int):
            url += "#L" + str(item["line"])
        note = "Archived review source"
    elif path in source_map and source_map[path].get("reference_url"):
        url = source_map[path]["reference_url"]
        note = source_map[path].get("availability", "Source-map reference")
    pointer = f'<a href="{esc(url)}">{esc(path)}</a>' if url else f'<code>{esc(path)}</code>'
    if not url:
        note = 'Evidence pointer retained; <a href="' + GITHUB + PUBLIC + 'review-2026-10-04/source-map.html">source availability map</a>'
    else:
        note = esc(note)
    line_note = f' · reviewed line {esc(item["line"])}' if "line" in item else ''
    rest = [f'<p class="source-note">{note}{line_note}</p>']
    for key, value in item.items():
        if key not in {"path", "line"}:
            rest.append(f'<p>{esc(value)}</p>')
    return '<li class="source-item">' + pointer + "".join(rest) + '</li>'


def render(value, source_map, field=None, level=4):
    """Preserve all source fields, including nested scenarios and parameter tables."""
    if field in {"sources", "evidence"} and isinstance(value, list) and all(isinstance(item, dict) and "path" in item for item in value):
        return '<ul class="source-list">' + "\n".join(source_html(item, source_map) for item in value) + '</ul>'
    if isinstance(value, dict):
        parts = []
        for key, child in value.items():
            if key == "id":
                parts.append(f'<p class="record-id">Record: {esc(child)}</p>')
            else:
                heading = min(level, 6)
                parts.append(f'<section class="evidence-field"><h{heading}>{esc(label(key))}</h{heading}>\n{render(child, source_map, key, level + 1)}</section>')
        return "\n".join(parts)
    if isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            return '<ul>' + "\n".join(f'<li>{esc(item)}</li>' for item in value) + '</ul>'
        return '<div class="evidence-items">' + "\n".join('<div class="evidence-item">' + render(item, source_map, level=level) + '</div>' for item in value) + '</div>'
    return f'<p>{esc(value)}</p>'


def audit_review(source_map):
    findings = json.loads((SOURCE / "findings.json").read_text())
    summary = json.loads((HERE / "project-quality.json").read_text())
    rows = []
    for item in summary:
        refs = " · ".join(f'<a href="#{esc(fid)}">{esc(fid)}</a>' for fid in item["finding_ids"])
        rows.append(f'<tr><th scope="row">{esc(item["area"])}</th><td>{badge(item["status"], {"green":"Sound", "yellow":"Improve", "red":"Blocked"}[item["status"]])}</td><td>{esc(item["assessment"])}</td><td>{esc(item["next_step"])}<small>{refs}</small></td></tr>')
    records = []
    for finding in findings:
        body = {key: value for key, value in finding.items() if key not in {"id", "title"}}
        records.append(f'<details class="full-record" id="{esc(finding["id"])}"><summary><span class="record-title">{esc(finding["id"])} · {esc(finding["title"])}</span><span class="record-deck">Priority {esc(finding["severity"])} · {esc(finding.get("status", "See assessment for scope"))}</span></summary><div class="record-body">{render(body, source_map)}</div></details>')
    return f'''<section id="audit"><div class="section-title"><span class="eyebrow">PROJECT-WIDE QUALITY</span><h2>What works across the project—and what to fix</h2></div>
<div class="quality-table table-scroll" tabindex="0" role="region" aria-label="Project-wide assessment table"><table><thead><tr><th scope="col">Area</th><th scope="col">Assessment</th><th scope="col">Finding</th><th scope="col">Next step</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="library-note">These are the original review findings, including their dated resolution notes. P1–P3 are repair priorities, not experiment outcomes. Later repairs are outside this snapshot.</p>
<details class="full-record"><summary>All {len(findings)} findings: bugs, design gaps and writing improvements</summary><div class="record-body">{"".join(records)}</div></details>
<p class="library-note"><a href="{GITHUB + PUBLIC}review-2026-10-04/coverage.json">Coverage ledger: 1,331 files</a> · <a href="{GITHUB + PUBLIC}review-2026-10-04/index.html">Original audit and verification record</a></p></section>'''


def full_review(data, source_map):
    reviews = []
    for review in data["reviews"]:
        heading = review.get("decision", review.get("evidence_class", ""))
        body = {key: value for key, value in review.items() if key not in {"id", "name"}}
        reviews.append(f'''<details class="full-record" id="{esc(review['id'])}">
<summary><span class="record-title">{esc(review['name'])}</span><span class="record-deck">{esc(heading)}</span></summary>
<div class="record-body">{render(body, source_map)}</div>
</details>''')
    proposals = []
    for proposal in data["original_proposals"]:
        body = {key: value for key, value in proposal.items() if key not in {"id", "name"}}
        proposals.append(f'''<details class="full-record" id="{esc(proposal['id'])}">
<summary><span class="record-title">{esc(proposal['name'])}</span><span class="record-deck">{esc(proposal.get('decision', proposal.get('question', '')))}</span></summary>
<div class="record-body">{render(body, source_map)}</div></details>''')
    scenario_count = sum(len(review.get("scenarios", [])) for review in data["reviews"])
    return f'''<details class="full-library" id="full-review">
<summary><span><span class="eyebrow">THE COMPLETE REVIEW</span><strong>The full PI review</strong></span><span class="full-count">{len(reviews)} reviews · {scenario_count} scenarios · {len(proposals)} proposals · 57 findings</span></summary>
<div class="library-body">
<p class="library-note">The complete dated review: project-wide findings, scientific assessments, research areas and proposals. Open a record for evidence, reasoning and next steps.</p>
<nav class="library-nav" aria-label="Full review sections"><a href="#audit">Project-wide quality</a><a href="#studies">Study reviews</a><a href="#areas">Research areas</a><a href="#portfolio">Original proposals</a><a href="#scope">Scope & provenance</a></nav>
{audit_review(source_map)}
<section id="studies"><div class="section-title"><span class="eyebrow">01 / STUDIES</span><h2>All {len(reviews)} study and version reviews</h2></div>{''.join(reviews)}</section>
<section id="areas"><div class="section-title"><span class="eyebrow">02 / RESEARCH AREAS</span><h2>{len(data['focus_areas'])} connecting questions</h2></div>{render(data['focus_areas'], source_map)}</section>
<section id="portfolio"><div class="section-title"><span class="eyebrow">03 / PROPOSALS</span><h2>All {len(proposals)} original proposals</h2></div>{''.join(proposals)}</section>
<section id="scope"><div class="section-title"><span class="eyebrow">04 / PROVENANCE</span><h2>Scope of this assessment</h2></div><p>{esc(data['scope'])}</p><details class="full-record"><summary>Original experiment grouping</summary><div class="record-body">{render(data['groups'], source_map)}</div></details>
<p>Review source: <a href="{GITHUB + PUBLIC}review-2026-10-04/scientific-review.json">immutable scientific-review.json</a>. <a href="{GITHUB + PUBLIC}review-2026-10-04/source-map.html">Source availability and provenance map</a>.</p></section>
</div></details>'''


def build():
    guide = json.loads((HERE / "review-guide.json").read_text())
    data = json.loads((SOURCE / "scientific-review.json").read_text())
    source_map = {row["workspace_path"]: row for row in json.loads((SOURCE / "source-map.json").read_text())}
    projects = guide["projects"]
    if len(projects) != 10 or len({project["id"] for project in projects}) != len(projects):
        raise ValueError("guide requires ten uniquely identified projects")
    review_ids = {review["id"] for review in data["reviews"]}
    rows = []
    for project in projects:
        if not set(project["review_ids"]).issubset(review_ids):
            raise ValueError("unknown full-review reference")
        if not re.fullmatch(r"[a-z0-9-]+", project["id"]):
            raise ValueError("invalid project id")
        if len(project["options"]) != 3 or sum(bool(item["recommended"]) for item in project["options"]) != 1:
            raise ValueError("each project requires three options and one recommendation")
        cells = []
        for field in LABELS:
            assessment = project["assessments"][field]
            if assessment["status"] not in STATUSES:
                raise ValueError("unknown assessment status")
            explanation = LABELS[field] + ": " + assessment["label"] + ". " + assessment["why"]
            cells.append(f'<td>{badge(assessment["status"], MATRIX_STATUS[assessment["status"]], explanation)}</td>')
        rows.append(f'<tr data-project="{esc(project["id"])}"><th scope="row"><button type="button" class="project-select" data-select="{esc(project["id"])}" aria-pressed="false">{esc(project["name"])}<span aria-hidden="true">↗</span></button></th>{"".join(cells)}</tr>')
    legend = guide.get("legend", {})
    legend_html = []
    for status, default in STATUSES.items():
        value = legend.get(status, default) if isinstance(legend, dict) else default
        if isinstance(value, dict):
            value = value.get("label", default)
        legend_html.append('<span title="' + esc(value) + '">' + badge(status, default) + '</span>')
    serialized = json.dumps(guide, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("&", "\\u0026")
    css = (HERE / "guide.css").read_text()
    js = (HERE / "guide.js").read_text()
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark">
<meta name="description" content="A clear visual guide to the Swarm Lab PI review: ten experiment families, four assessments, and concrete next choices.">
<title>Swarm Lab · PI review guide</title><style>\n{css}\n</style></head>
<body><a class="skip-link" href="#project-detail">Skip to selected project</a>
<div class="page"><header class="masthead"><a class="wordmark" href="#overview"><span class="brand-mark" aria-hidden="true">◈</span> SWARM LAB <span>/ PI REVIEW</span></a><a class="audit-shortcut" href="#audit">Project-wide quality</a><button type="button" id="open-full" class="quiet-button">Full review <span aria-hidden="true">↗</span></button></header>
<main><section class="hero" id="overview"><p class="eyebrow">RESEARCH QUALITY, AT A GLANCE</p><h1>{esc(guide.get('title', 'PI review at a glance'))}</h1><p class="hero-deck">{esc(guide.get('subtitle', 'Ten projects. Four judgments. Three next-step options.'))}</p>
<div class="snapshot"><span class="snapshot-dot" aria-hidden="true"></span><p>{esc(guide.get('snapshot_note', 'Dated review snapshot · 4 October 2026. These assessments describe the reviewed evidence, not live experiment readiness.'))} <a href="https://github.com/dmarzzz/swarm-lab/blob/main/researchers/vishesh/notes/pi-direct-launch-trace-cycle-2026-10-04/README.md">Latest runs, trace reviews and repairs →</a> · <a href="https://github.com/dmarzzz/swarm-lab/blob/main/experiments/EVIDENCE.md">Later evidence →</a></p></div>
<div class="legend" id="criteria"><span class="legend-label">Assessment guide</span>{''.join(legend_html)}<span class="legend-note">Scoped judgments, never launch approval. A promising idea can have weak evidence.</span></div></section>
<section class="workspace" aria-label="Experiment overview and selected project"><div class="overview-panel"><div class="panel-heading"><div><p class="eyebrow">THE PORTFOLIO</p><h2>Where each project stands</h2></div><span id="project-count" class="count" role="status">10 projects</span></div>
<div class="filters"><label class="search-label"><span class="sr-only">Find a project, issue or next step</span><span aria-hidden="true">⌕</span><input id="project-search" type="search" placeholder="Find a project, issue or next step" autocomplete="off"></label><label class="filter-label"><span class="sr-only">Filter by an assessment color</span><select id="status-filter"><option value="all">All assessments</option><option value="red">Has a major gap</option><option value="yellow">Has a needs-work rating</option><option value="green">Has a strong point</option><option value="gray">Has an untested dimension</option></select></label><button id="reset-filters" type="button" class="reset-button">Reset</button></div>
<p class="table-hint">Select a project to see the reasoning and next choices.</p><div class="table-scroll" tabindex="0" role="region" aria-label="Project assessment table; scroll horizontally on small screens"><table><thead><tr><th scope="col">Project</th>{''.join('<th scope="col">' + title + '</th>' for title in LABELS.values())}</tr></thead><tbody id="project-rows">{''.join(rows)}</tbody></table></div>
<div id="empty-results" class="empty-state" hidden><strong>No matching projects.</strong><p>Try another phrase or clear the filters.</p><button type="button" class="quiet-button" data-reset>Show all projects</button></div>
<p class="table-foot">Review judgments, not a leaderboard or probability of success. The complete review remains available below.</p></div>
<aside id="project-detail" class="detail-panel" tabindex="-1" aria-label="Selected project"></aside></section>
{full_review(data, source_map)}
<footer><span>SWARM LAB · RESEARCH NOTES</span><p>Options are recommendations, not completed work.</p></footer></main></div>
<script id="guide-data" type="application/json">{serialized}</script><script>\n{js}\n</script></body></html>\n'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if index.html differs from generated output")
    args = parser.parse_args()
    output = build()
    target = HERE / "index.html"
    if args.check:
        if not target.is_file() or target.read_text() != output:
            raise SystemExit("Guide is stale: run build.py")
        print("Guide matches its source data and styles.")
    else:
        target.write_text(output)
        print("Built self-contained index.html")


if __name__ == "__main__":
    main()
