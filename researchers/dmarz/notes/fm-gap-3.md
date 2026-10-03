# fm-gap-3: pre-AI analogues (counterintelligence, memory science, identity)

Agent: dmarz/fm. Date: 2026-10-03. Gap brief from the completeness critic: the library had 0 hits for
counterintelligence, double agent, source monitoring, reconsolidation, Loftus, coercive persuasion and Parfit.

## Search rounds

| Round | Query / source | API | Results seen | New entries |
|---|---|---|---|---|
| 0 | lab.py find for counterintelligence, double agent, double-cross, source monitoring, reconsolidation, Loftus, coercive persuasion, Parfit, Heuer, thought reform, misinformation, Admiralty, Bell-LaPadula, Lindelauf, covert network, Curveball, memory conformity, social contagion, Roediger, Gabbert, false memory, personal identity, corroboration, brainwash, intelligence analysis | local | 0 relevant hits (only torpmann-hagen-2026-memetic, aureli-2008-fission, de-marzo-2026-conformity nearby) | 0 |
| 1 | Seed metadata: Johnson 1993, Loftus 2005, Nader 2000, Heuer 1999, Masterman 1972, Schein 1961, Lifton 1961, Parfit 1984 | Crossref | 24 | 0 (metadata only) |
| 2 | Open full text for seeds: Loftus (WSU mirror PDF), Johnson (Yale memlab scanned PDF, read as images), Nader (PubMed abstract), Heuer (cia.gov PDF) | eutils, curl, WebSearch | 4 | 4 |
| 3 | Reconsolidation and social memory: Hupbach 2007, Chan 2009 RES, Gabbert 2003, Roediger 2001 | Crossref, PubMed eutils | 9 abstracts | 5 (hupbach, roediger, meade-2002, numbers-2014, wulff-2025) |
| 4 | Admiralty code / source grading: Irwin and Mandel 2019 (paywalled), found Kelly et al. 2025 (open) | WebSearch, Crossref, WebFetch | 10 | 1 (kelly-2025-effect) |
| 5 | Double-Cross System: Masterman book restricted on Internet Archive; DTIC ADA420278 (organisational, not used); CIA Studies in Intelligence OSS double-agent article | archive.org advancedsearch, WebSearch | 10 | 1 (cowden-2014-pioneering) |
| 6 | Corroboration failures: WMD Commission 2005 Curveball section | WebSearch, curl | 1 | 1 (wmd-commission-2005-report) |
| 7 | Compartmentation and covert network structure: Lindelauf 2009, Baker and Faulkner 1993, Enders and Su 2007 | Crossref, econpapers, Tilburg repository | 4 | 1 (lindelauf-2009-influence) |
| 8 | Parfit fission: SEP Personal Identity (Olson 2023) | curl | 1 | 1 (olson-2023-personal) |
| 9 | Coercive persuasion: Schein 1956/1961, Lifton 1956/1957/1961 (PubMed records, PMC PDF behind a bot challenge, books restricted); CIA 1956 "Brainwashing from a Psychological Viewpoint" | eutils, archive.org | 25 | 1 (cia-1956-brainwashing) |
| 10 | LLM bridges: arXiv abs:"misinformation effect", "source monitoring", "false memories", "double agent", "memory reconsolidation", "suggestibility", conformity+memory | arXiv API | about 30 | 4 (akkil-2026-emergence, cao-2025-analyzing, cuadros-2026-governed, xiao-2026-playing) |
| 11 | Semantic Scholar search "social contagion of memory language model agents" (second query 429) | S2 | 10 | 2 (hu-2026-dissociative, perrier-2025-position) |
| 12 | CI tradecraft: Studies in Intelligence search | WebSearch, curl | 9 | 1 (olson-2001-ten) |

Total new entries: 22 (4 full, 7 skim, 11 abstract). Full reads: loftus-2005-planting, cowden-2014-pioneering, lindelauf-2009-influence, olson-2001-ten.

## Found but not added

- Masterman 1972, The Double-Cross System: restricted on the Internet Archive; not opened.
- Schein 1961 Coercive Persuasion, Lifton 1961 Thought Reform: restricted; unrestricted uploads look like unauthorised copies, not used. Schein 1956 (Psychiatry 19:149-172) and Lifton 1956/1957: PubMed records only, no abstract text; PMC PDF blocked by a bot challenge.
- Parfit 1971 "Personal Identity" and Reasons and Persons (1984, fusion discussion): not opened.
- Gabbert, Memon and Allan 2003 memory conformity; Chan, Thomas and Bulevich 2009 reversed testing effect: Crossref metadata only, no abstract reached.
- Irwin and Mandel 2019 (Admiralty Code critique): paywalled.
- NATO STANAG 2511 / AJP-2.1 text: not opened; its scales are described in kelly-2025-effect.
- Baker and Faulkner 1993, Enders and Su 2007: Crossref metadata only.
- DTIC ADA420278 (Double Cross lessons for HUMINT organisation): opened metadata, judged off-topic.
- arXiv 2408.04681 (LLM chatbots amplify false memories in witness interviews): human-subject study of AI as misinformation source; relevant but not added for time.

## What is thin

- No source on fusion (merging two persons into one) in philosophy; only fission.
- Human memory results are mostly at abstract depth (Nader, Hupbach, Roediger, Meade, Numbers, Wulff).
- No primary text from Masterman, Schein or Lifton; the double-agent and coercive-persuasion lanes rest on a CIA article and a CIA study.
- No study tests post-event misinformation, source monitoring or social contagion on LLM agents with persistent memory. That is a concrete, cheap experiment for the Q3 lane.

## Quality items from the critic

Checked at 19:05Z: the three fm-sutton YAML errors, the 18 fm-contagion stubs and hanson-2016-age read_depth had already been fixed by other agents by the time this lane reached them, so no edits were made to those files.
At 19:25Z, 16 new untouched paper stubs (an-2012-security, avenhaus-2002-inspection, tambe-2011-security and others) carrying added_by dmarz/fm were created at about 19:23Z by a parallel agent using the same agent id; they were left alone as in-progress work.
