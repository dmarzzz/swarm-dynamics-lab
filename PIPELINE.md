# PIPELINE.md: collectors -> batches -> claimable issues

The problem this solves: every researcher's agents were re-discovering the same sources, and only some of us
can read X at all. This pipeline splits **finding** sources from **cataloguing** them. Anyone with an API key
runs a collector; the raw hits are deduplicated against the library and cut into small single-topic batches;
each batch becomes a GitHub issue; any agent on the team claims an issue and turns its items into library
entries to the normal AGENTS.md quality bar.

It feeds the `scan` phase. It does not replace the task board, the survey gate or anything else in
`AGENTS.md`. A batch issue is a unit of scan work, nothing more.

```
collect.py x-search / apify / seed      ->  data/candidates-raw/*.jsonl      (local, git-ignored)
collect.py links                        ->  blog/code/paper urls out of the posts
collect.py batch                        ->  candidates/<source>/<batch-id>.jsonl + candidates/SEEN.txt  (committed)
batches.py publish                      ->  one GitHub issue per batch, labels batch / source:* / topic:*
batches.py claim <n>                    ->  assignee + `claimed` label + comment
  your agent writes library entries, lab.py sync --every 180 pushes them to main
batches.py done <n> --entries ...       ->  comment + close
```

## 1. Collect (anyone with keys; shadow's agents run this on a loop)

Secrets never live in the repo. Put them in env (`X_BEARER_TOKEN`, `APIFY_TOKEN`) or in `data/secrets.json`
(`data/` is git-ignored): `{"x_bearer_token": "...", "apify_token": "..."}`.

```bash
# X search (recent = last 7 days; --archive = full archive, needs Pro access). One query per line in the file,
# `<topic-slug><TAB><query>`. --threads N also fetches the author's self-replies for the N strongest roots.
python3 scripts/collect.py x-search --queries candidates/queries/x-informal-2026-10-03.txt \
        --by shadow/sol-2 --max 40 --archive --threads 2

# Apify (metered, $5/month hard cap on the free plan). Checks spend before and after, refuses past --hard-cap.
python3 scripts/collect.py apify --actor apidojo/tweet-scraper --input data/apify-x.json --kind x \
        --by shadow/sol-2 --max-usd 0.50 --topic swarm-detection
python3 scripts/collect.py apify --actor apify/website-content-crawler --input data/apify-web.json --kind web \
        --by shadow/sol-2 --max-usd 0.50 --topic llm-agent-swarms

# Outbound links in the collected posts become blog/code/paper candidates
python3 scripts/collect.py links --by shadow/sol-2

# Hand-fed urls (a seed list from a task, a human's inbox): `<url> <note>` per line
python3 scripts/collect.py seed --urls data/blog-seeds.txt --topic llm-agent-swarms --by shadow/sol-2
```

Every raw row has: `id` (`x:<status-id>` or `url:<normalised url>`), `source` (`x | apify-x | blog | web | code | paper`),
`url`, `title`, `text`, `author`, `date`, `topic` (guessed from keywords, the batcher groups by it),
`likes`, `links`, `found_by`, `query`, `collected`. X API calls are logged to `data/x-api-calls.log`.

## 2. Batch

```bash
python3 scripts/collect.py batch --by shadow/sol-2 --size 10 --min-score 1
python3 scripts/collect.py status
```

`batch` reads everything in `data/candidates-raw/`, drops anything whose id or normalised url is already in
`library/` (same `norm_url` as `lab.py`), already in `candidates/SEEN.txt`, or scored below `--min-score`
(0 to 5: engagement, length, has links or thread, topic keyword hits, reply penalty). Survivors are grouped by
`(source, topic)`, sorted by score, cut into chunks of `--size` (default 10, tail merged if small), written to
`candidates/<source>/<source>-<topic>-<yyyymmdd>-<nn>.jsonl`, and appended to `SEEN.txt` so no later run
re-emits them. Groups smaller than `--min-batch` (3) stay in raw until more arrive.

Commit `candidates/` with the normal prefix: `[<agent-id>] candidates: 6 batches from x-search`.
`lab.py check` ignores `candidates/` (it only validates the documented folders).

## 3. Publish

```bash
python3 scripts/batches.py setup       # once: creates labels batch, claimed, needs-review, source:*, topic:* (idempotent)
python3 scripts/batches.py publish     # one issue per batch without one; records batch -> issue in candidates/ISSUES.tsv
python3 scripts/batches.py list --free
```

Issue title: `[batch] x/swarm-detection: 10 candidates (x-swarm-detection-20261003-01)`. Body: how to work it,
a checklist of items with url, snippet, author, date, score and outbound links, the target library dir, and
Done-when. Labels: `batch`, `source:<x|blog|web|code|paper>`, `topic:<slug>`.

## 4. Claim and work (every agent on the team)

```bash
python3 scripts/batches.py list --free
python3 scripts/batches.py claim 42 --agent vishesh/claude-2       # refuses if someone holds it and it is not stale
python3 scripts/lab.py sync --agent vishesh/claude-2 --every 180 >> /tmp/swarm-lab-sync.log 2>&1 &
```

Then for each item in the issue:

1. Open the source yourself. **No phantom sources**: if you cannot load it, skip it with a reason.
2. `python3 scripts/lab.py find "<url>"`. If it is already catalogued, append notes there instead.
3. `python3 scripts/lab.py new thread|blog|code|paper <id> --agent <id>` (id patterns in AGENTS.md) and fill every
   TODO. Threads: archive the full text (the batch jsonl carries `text` and, for strong roots, `thread_text`, but
   verify against the live page and copy the handle from the page). Blogs: fill Evidence quality honestly.
   `read_depth` must be true. Tag the batch topic plus any other that applies. Link related entries `[[id]]`.
4. Tick the checkbox on the issue. `python3 scripts/batches.py touch 42 --agent <id>` every 30 minutes.
5. When the list is done: `python3 scripts/batches.py done 42 --agent <id> --entries library/threads/x-....md ...`
   (`--skipped "3: dead link; 7: duplicate of [[x-...]]"`). Cannot finish: `release 42 --agent <id> --note "..."`.

Stale rule: a `claimed` issue with no comment, edit or ticked box for **90 minutes** may be reclaimed by anyone
(`batches.py stale` lists them). One batch at a time per agent. The entries you write count toward whichever
scan task covers that topic; mention the issue number in your commit message.

## Quality bar

Identical to AGENTS.md. A batch is not a licence to catalogue thin: 25-word original summary, numbers where the
source gives them, honest read depth, correct handles, archived thread text, evidence-quality section for blogs.
Ten good entries beat ten stubs; skipping an item with a reason is fine.

## Paste-in prompt for a researcher's agent

```text
Also work the candidate batches. In the swarm-lab repo read PIPELINE.md. Loop: `python3 scripts/batches.py list --free`,
claim one with `python3 scripts/batches.py claim <n> --agent <your-agent-id>`, write a library entry for every item to the
AGENTS.md bar (open each source yourself, no phantom entries, archive thread text, tag the batch topic), keep
`python3 scripts/lab.py sync --agent <id> --every 180` running, tick items on the issue, then
`python3 scripts/batches.py done <n> --agent <id> --entries <paths>`. Prefer batches whose topic matches my directives.
Still obey AGENTS.md and my researchers/<me>/README.md; batches are scan work, not a replacement for the task board.
```

## Files

```
candidates/
  queries/*.txt                 X query files (topic<TAB>query per line), committed so others can rerun or extend
  <source>/<batch-id>.jsonl     one candidate per line, committed, small
  SEEN.txt                      global ledger: id<TAB>batch<TAB>found_by; batch never re-emits an id listed here
  ISSUES.tsv                    batch-id -> issue number, url (written by batches.py publish)
data/candidates-raw/*.jsonl     raw collector output, git-ignored
data/x-api-calls.log            every X API call, git-ignored
scripts/collect.py              collectors + batcher
scripts/batches.py              issues: setup, publish, list, claim, touch, done, release, stale
.github/ISSUE_TEMPLATE/batch.md the issue shape, for hand-made batches
```

Budget notes: X search `recent` is 7 days; `all` needs Pro. Apify free plan is $5/month hard; `collect.py apify`
refuses a run that would push the month past `--hard-cap` (default $4) and reports cost after each run.
