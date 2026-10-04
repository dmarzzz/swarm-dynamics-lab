# Reproduce the saved verification result

Start with [the post-mortem](v1-post.md). Public artifacts contain authored assessments, aggregate/paired outcomes and visualizations. **Raw native episodes, transport and usage records remain private and require separate disclosure authorization.** No raw AI Village data, account records, credentials or operator conversation is published. Full independent replay is therefore available only to an authorized holder of the retained native archive.

Use Python 3.12 or 3.13 with the tested dependencies: jsonschema 4.26.0, matplotlib 3.11.2, Pillow 12.3.0 and PyYAML 6.0.3. From this directory, supplying an authorized private archive:

```sh
python reproduce_saved.py --results /path/to/private/native-records --out /tmp/immune-verification-saved-replay
python render_saved.py /path/to/private/native-records/episodes.json /tmp/immune-verification-saved-replay/figures
```

Choose a fresh output directory. The first command checks public report and frozen source hashes, then reconstructs every native request and transition from the caller's retained data. Its reconciliation must equal the published report. It performs zero model calls, does not fetch credentials and never uploads the private data. The second command rebuilds the discrete-tick visualization; fonts and pixel rendering can vary across platforms while measurements remain fixed.

[The evidence index](evidence-index.json) identifies every public report/artifact. [The quality review](v1-quality.json) is the owning scientific assessment and retains the capability gap. Operational finalize is separate and does not itself establish scientific review.
