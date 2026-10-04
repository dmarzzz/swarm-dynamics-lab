---
id: kobak-2024-delving
type: paper
title: Delving into LLM-assisted writing in biomedical publications through excess vocabulary
authors:
- Dmitry Kobak
- Rita González-Márquez
- Emőke-Ágnes Horvát
- Jan Lause
year: 2024
venue: Science Advances 11(27), 2025
url: https://arxiv.org/html/2406.07016
doi: 10.1126/sciadv.adt3813
arxiv: '2406.07016'
cite: Kobak, D., González-Márquez, R., Horvát, E.-Á., & Lause, J. (2024). Delving into LLM-assisted writing in biomedical publications through excess vocabulary. Science Advances, 11(27), eadt3813 (published 2 Jul 2025). https://doi.org/10.1126/sciadv.adt3813. arXiv:2406.07016.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 239 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Borrows the excess-mortality idea: extrapolate each word's 2021-2022 frequency in 15.1 million PubMed abstracts (2010-2024) to a counterfactual 2024 value and look for words whose observed frequency exceeds it. In 2024 hundreds of mostly stylistic verbs and adjectives ("delves", "underscores", "showcasing", "potential", "crucial") jumped, unlike earlier content-word shifts such as Covid. The frequency gap for sets of these marker words gives a training-free lower bound of 13.5% of 2024 abstracts processed with an LLM, reaching 40% in some subcorpora.

## Contribution

A population-level estimator that needs no labelled human or LLM corpus and no assumption about which model or prompt was used, which avoids the reference-corpus bias of [[liang-2024-monitoring]]. It also puts the LLM shift in historical context: larger than the Covid vocabulary shock.

## Key results

- Measured: 454 excess words in 2024 versus at most 190 in any earlier year (2021, Covid); 379 of the 2024 excess words were style words, 66% verbs and 14% adjectives, whereas pre-2024 excess words were mostly content nouns.
- Measured: frequency gap for a 291-word rare-style set gave 13.6%, a 10-word common set (across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within) a similar value; average lower bound 13.5% of 2024 abstracts, i.e. at least about 200,000 papers per year.
- Measured heterogeneity: lower bound about 0.20 in computational fields, above 0.15 for China, South Korea and Taiwan versus below 0.05 for UK and Australia, 0.25 for the journal Sensors and 0.20 for Cureus, 0.21 for MDPI and 0.20 for Frontiers pooled, 0.07 for Nature/Science/Cell; local clusters above 0.40.
- For comparison, covid/pandemic/coronavirus/sars in 2021 gave a gap about half of the 2024 LLM gap.

## Methods and models

Binary word-occurrence matrix (15.1M x 273K) from cleaned PubMed abstracts (over 100 regexes to strip boilerplate). Counterfactual 2024 frequency = linear extrapolation from 2021 and 2022, floored at the 2022 value. Excess words defined by thresholds on frequency ratio and frequency gap; words hand-annotated as content or style blind to year. Subgroup analyses by field (39), country (50), journal (100), inferred gender, plus a t-SNE map of PubMedBERT embeddings. Code: github.com/berenslab/llm-excess-vocab.

## Limitations and open questions

Only a lower bound: LLM-processed abstracts without any marker word are invisible, and the authors note native speakers may edit marker words out, so low bounds may reflect better hiding rather than less use. Cannot separate direct LLM use from humans adopting LLM vocabulary (see [[yakura-2024-empirical]] and [[geng-2025-human]] for that confound), and cannot attribute to a particular model. Marker words decay once publicised.

## Relevance to us

The cleanest training-free estimator of machine-written share in a corpus, transferable to any platform with a pre-LLM baseline (posts, comments, bios). For swarm detection, the subgroup idea matters: excess-marker rates localise to clusters (a journal, a country, a topic island), which is how a coordinated operation would show up against a population baseline. Pairs with [[liang-2024-monitoring]] (needs reference corpora) and [[gray-2024-chatgpt]] (earlier marker-word count).
