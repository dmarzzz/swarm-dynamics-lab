# fm gap-2: Q1 as an inspection / Stackelberg security game (dmarz/fm, 2026-10-03)

Brief: the library had 0 hits for inspection games, audit games or Tambe, and only passing Stackelberg mentions. Goal: catalogue the game-theory literature that says how much to randomise which child is audited or merged, at what budget, and when an observing attacker defeats hiding.

## Rounds

| Round | Query / API | Results | New entries |
|---|---|---|---|
| 1 | Crossref by DOI and bibliographic query: Avenhaus 2002, Tambe 2011, Becker 1968, Holmstrom 1982, Jajodia 2011 MTD, FlipIt, Conitzer 2006, Korzhyk 2011, Audit games, Laffont & Martimort | 10 queries, all resolved | 0 (metadata only) |
| 2 | Direct PDFs: LSE preprint of Inspection Games, arXiv 1401.3888, arXiv 1303.0356, IACR ePrint 2012/103, Conitzer EC06 PDF, SIGecom Exchanges 8(2) Pita, NBER Becker reprint | 7 opened | 7 |
| 3 | Publisher pages: Cambridge Core (Tambe), Princeton UP (Laffont & Martimort), AAAI OJS (An 2012, Blocki 2015), IJCAI 2018 PDF (Sinha) | 5 opened; Springer (Jajodia MTD) and JSTOR (Holmstrom) blocked | 5 |
| 4 | Semantic Scholar /citations of Korzhyk 2011 (294 citing) and FlipIt (291 citing), filtered for LLM/agent/AI/audit; Audit Games arXiv id not found in S2 | 2 seeds chased | 2 (Gans & Holden 2026, Damera & Baras 2026) |
| 5 | WebSearch for FlipThem; found Threshold FlipThem (ePrint 2015/784) | 2 opened | 2 |

Total new entries: 16. Semantic Scholar 429s on search; OpenAlex daily budget exhausted ("$0 remaining"); arXiv export API returned empty bodies, so arXiv abs/HTML pages were scraped directly.

## Found, not added

- Holmstrom 1982 "Moral Hazard in Teams" (Bell J Econ 13(2) 324-340): JSTOR page would not load, S2 abstract elided by publisher. Only secondary lecture notes (Georgiadis, Kellogg Ec515 Module 8) were opened; not catalogued as a primary source.
- Jajodia et al. 2011 Moving Target Defense (Springer, DOI 10.1007/978-1-4614-0977-9): Springer page blocked. MTD is already covered by cho-2020-toward and sengupta-2020-survey.
- Pita et al. 2008 ARMOR (AAMAS industry track): not reached; pita-2009-security used instead.
- Alchian & Demsetz 1972 team production: not opened.
- FlipNet (networked FlipIt, 2017), "Optimal Timing of Moving Target Defense: A Stackelberg Game Model" (arXiv 1905.13293), coalitional security games (Guo et al. 2016): seen in citation lists only.

## Contagion stubs (quality fix)

The 18 fm-contagion stubs were abandoned (untouched since 18:21Z). I identified all 18 arXiv ids and recreated scaffolds, but another dmarz/fm session was filling them in parallel, so I left the filling to it to avoid clobbering. At 19:4xZ no TODO stubs remain and the full library check is clean.

## Thin

- No game-theoretic paper models an LLM parent forking and merging children; the mapping (children = targets, pre-merge audit = defender resource, k-of-n merge = threshold FlipThem) is inferred.
- Multi-attacker and coalitional security games read only through the Sinha 2018 survey.
- Moral hazard in teams (attribution of a corrupted joint output) is only at description level (Laffont & Martimort page).
