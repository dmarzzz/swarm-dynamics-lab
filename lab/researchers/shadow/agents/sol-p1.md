---
agent: shadow/sol-p1
tool: claude-code
state: done  # working | idle | blocked | done
task: null
doing: finished paper batches #57-#68 (sybil-resistance), 77 entries pushed to main
updated: 2026-10-03T22:06Z
---

## Notes

Anything the next agent picking up this lane should know.

- Worked paper batches #57 through #68 (sybil-resistance, dmarz's OpenAlex-sourced lists). 77 new `library/papers/*.md` entries, all `lab.py verify` clean. swarm-detection batches #52-#56 were already taken by other writers when this lane started.
- Metadata path that works from shad0wbot: Crossref REST (`api.crossref.org/works/<doi>`) plus Unpaywall for OA links, arXiv export API for arXiv ids, Exa search for PDF mirrors and abstracts. OpenAlex rate-limits after a handful of calls; Semantic Scholar 429s; dblp bot-walls. Helper scripts live in `~/.moltbot/projects/swarm-hackathon/` (`cr_meta.py`, `arxiv_meta.py`, `exa_find.py`, `exa_text.py`).
- `lab.py verify` title check compares against Crossref, which sometimes stores only the short title (e.g. "SecureArray", "Exploiting KAD"). Use the Crossref title in the `title:` field and put the full title in the Summary body.
- ACM `10.5555/...` DL ids are not Crossref DOIs; set `doi: null` and keep the DL link in the cite.
- Watch for conference/journal twins in the batch lists (Funnel NOMS/TNSM, Sargeant DASC with two DOIs, Ito 2004/2005): catalogue one, note the other as skipped.
- Content flag: Todo, Iwasaki, Yokoo, Sakurai (AAMAS 2009, `todo-2009-characterizing`) show GM-SMA (`yokoo-2006-false`) is NOT false-name-proof. The 2006 entry carries that caveat; do not cite GM-SMA as a working mechanism.
- Spine of the sybil-resistance material as catalogued: (1) mechanism-design line from Sakurai 1999 through Yokoo 2000/2003/2005/2006, Todo 2009/2011, Iwasaki 2010, with the "tolerate Sybils in VCG" counterpoint in Alkalay-Houlihan 2014 and Gafni 2020, voting in Wagman 2008 / Bachrach 2008 / Conitzer 2010; (2) P2P overlay line Urdaneta 2011 survey, Steiner 2007, Puttaswamy 2009, Lesniewski-Laas 2008, SybilShield 2013, Eisenbarth 2022 measurements; (3) physical-layer identity line Sheng 2008, Yang 2013, SecureArray 2013, Liu 2014 CSI, Wang 2013 beamforming attack, Gil 2015, Renganathan 2022; (4) economics line Friedman 2006 / Kash 2009 / 2012 scrip, Resnick 2009, Margolin 2007 Informant, BitTorrent trio; (5) credential/attestation line Abdolmaleki 2026 tACT, Mir 2023, Hanzlik 2021, zkSENSE 2021, Scrappy 2024.
- GitHub API had two 503/timeout windows during the evening (~21:47Z and ~22:01Z). `batches.py done` hangs silently when that happens; check `curl api.github.com/rate_limit` before assuming the script is stuck.
