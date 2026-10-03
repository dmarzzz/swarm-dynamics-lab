---
name: fd-add
description: File a deliverable (film, figure, paper, deck, dataset, doc, page, model, any output someone will use) into this project's governed artifacts/ folder with its provenance. Use it every time you have produced a finished output, before you report it; never write, copy or move files into artifacts/ by hand.
---

# fd-add: file an output into artifacts/

`artifacts/` is governed: every file there is named in `artifacts.yaml`, laid out `artifacts/<id>/<id>-v<N>.<ext>`,
never overwritten, only superseded by the next version, and hashed into `artifacts.lock.json`. A hook denies
direct writes there. The one door is:

```sh
python3 .flightdeck/fd.py add <file> --id <id> --type <type> --title "<title>" --note "<what changed>" \
    --prompt "<the human's words>" --ingredient src/<script that made it> [--ingredient <input>]...
```

- `<file>`: the finished output, wherever you made it (`src/out/film.mp4`, `/tmp/fig.png`). It is moved into place
  (`--copy` keeps the source).
- `--id`: the artifact's stable slug (`launch-film`, `fig-latency`). A NEW id needs `--type` and `--title`; an
  existing id needs only `--id` (the next version number is chosen for you).
- `--type`: one of `api app dataset deck doc figure film library model notebook package paper post repo service
  site spec thread`.
- `--by`, `--session`, `--model`: filled in for you in Claude Code and Codex (`fd.py` reads your session from the
  environment and the model from your own transcript; a `--model` that disagrees is overruled). Pass them only
  when `fd.py` cannot see a session: `--by claude|codex|nanocodex|hermes|human|ci`, `--session <harness>:<id>`.
- `--prompt`: the human's words, quoted, not paraphrased.
- `--ingredient`: each input the output was made from; repeat the flag. Generate figures, films, datasets and decks
  from a script under `src/` (not an inline `python -c` or a file in /tmp) and pass that script as an ingredient:
  `fd.py` warns without one, and `--strict` refuses.

`add` refuses a file that breaks the project's `formats:` policy in `project.yaml` (extension, size, codec,
faststart) and says the smallest change that passes; make the file right. If the request itself conflicts with
`formats:` (a 400px thumbnail where figures must be 1600px), say so and ask the user before substituting. It prepends the version to `artifacts.yaml`,
refreshes `artifacts.lock.json`, and prints the new path. Commit `artifacts.yaml` + `artifacts.lock.json`
together with the file.

Before you finish a session: `python3 .flightdeck/fd.py check --strict .` and leave it clean (the Stop hook
runs it too and reports what is wrong).

`scripts/fd-add.sh` is the same command as a wrapper: `.agents/skills/fd-add/scripts/fd-add.sh <file> --id …`.
