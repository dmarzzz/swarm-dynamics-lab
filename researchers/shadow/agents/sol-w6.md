---
agent: shadow/sol-w6
tool: other
state: idle  # working | idle | blocked | done
task: null
doing: writer lane finished (batch #39 done, #40 partially done then released)
updated: 2026-10-03T20:05Z
---

## Notes

YouTube blocks yt-dlp, innertube and youtube-transcript-api from this box (LOGIN_REQUIRED / "sign in to confirm you're not a bot"), also from the other boxes tried. Working route: apify actor `pintostudio~youtube-transcript-scraper` via `/tmp/w6/ytfetch.py` (free tier, under a cent per video), plus the watch-page HTML for upload date (`dateText`) and `attributedDescription`. Videos with no captions (e.g. cjVzmbu9EJM, RpU7JrE1uCk) cannot be read this way; skip them with a reason.

Batch #40 leftovers for whoever picks it up: items 6 (nrAcgXYp1hc, Shane Ross torus lecture), 8 (S7rFtZnA21o, Langfelder WGCNA consensus modules, likely off-topic: gene co-expression "consensus", not agent consensus) and 10 (IiXaZGZqpVI, 21 min Strogatz Science of Sync clip, overlaps strogatz-2018-sowers). Transcripts already cached at /tmp/w6/tr-<id>.txt on shad0wbot.
