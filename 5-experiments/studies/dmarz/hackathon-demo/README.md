# hackathon-demo: the two-minute submission film (team Swarm of Theseus)

This folder holds the source of the film the team submitted to the AI Village x Grove Research AI Swarm Dynamics
Hackathon on 2026-10-04. The film is one page, `index.html`, that plays at 1920x1080 and is a pure function of time.
Each scene is one classic script in `scenes/`. A recorder steps the page frame by frame into an mp4, and a second
script lays a generated narration on top. The filed film is the artifact `hackathon-demo-film` (see `artifacts.yaml`).

Site: swarmsafety.org. Repository: github.com/dmarzzz/swarm-dynamics-lab (renamed from `swarm-lab` on 2026-10-04).

## What the film says

| Scene | Starts | Seconds | Content |
|---|---|---|---|
| `team` | 0:00 | 3.5 | Team name, three GitHub avatars, a QR code to each X profile, the site and the repository |
| `define` | 0:03.5 | 7.8 | AI safety aligns a single agent; distributional safety secures the swarm or market as a whole |
| `questions` | 0:11 | 10.5 | Three questions: Sybils, a few adversarial agents, safety constraints under turnover |
| `method` | 0:22 | 7.8 | 3,319 sources reviewed and open sourced, 219 hypotheses, 15 research areas |
| `lab` | 0:30 | 12.3 | The lab as one diagram: sources, hypotheses, 103 experiments, 25 servers, 1,584 runs in 16 hours, the gate rail |
| `sybil` | 0:42 | 24.2 | Result 1, Thou shalt not split |
| `result3` | 1:06 | 19.8 | Result 2, How to win agents and influence swarms |
| `theseus` | 1:26 | 20.7 | Result 3, Swarm of Theseus |
| `next` | 1:47 | 14.2 | Three next steps, then the end card with the site, the repository and its QR code |

The scene lengths follow the narration clips (`narrate.py time`), so they change when the narration does.

## The four-minute cut

`index.html?film=long` plays a second cut of about four minutes that shares the scenes above and adds eight. It is a
draft: it had not been reviewed or filed as an artifact when this was written.

| Scene | Seconds | Content |
|---|---|---|
| `why` | 19 | The event's prompt and the Hugging Face incident in METR's numbers; the stated goal (recreate an incident like it in a lab) and that this lab does not run the full swarm yet |
| `frame` | 30 | Single-agent safety against distributional safety (after Tomasev et al., arXiv:2512.16856), then an illustration: three agents each safe alone, two routes by which the data still leaves (through each other, through a message board they set up) |
| `tracks` | 16 | The research map: 219 candidate hypotheses in 15 areas as a radial, the 7 experiment tracks by name |
| `stack` | 18 | The control path as infrastructure as code: agents, git, OpenTofu and Ansible, short-lived servers, the run hub, the dashboard, and results returning to the agents |
| `highlights` | 5 | 118 studies, three highlighted |
| `theseus50` | 26 | Result 3 in this cut: the fifty-member Swarm of Theseus run (S50, GPT-6 Sol). 297 of 300 decisions right with a written note, 166 of 300 with nothing inherited, 295 with dialogue, 298 with founders kept. It replaces the three-member pilot scene, which the two-minute cut still uses |
| `roadmap1`, `roadmap2`, `roadmap3` | 10 to 12 each | The same map after each result: the candidates it bears on, what it changes, the next experiments |
| `more` | 8 | Ten more experiments as cards, nulls and failures included |

Each result scene carries a link chip top right (`scenes/links.data.js`): its page on swarmsafety.org as text and a QR code.

Order: team, why, frame, questions, tracks, lab, stack, highlights, sybil, roadmap1, result3, roadmap2, theseus50, roadmap3, more, next.
`INTRO-FACTS.md` holds the quotes and sources behind `why` and `frame`, where the wording is the paper's and where it is
ours, and what a specialist could challenge. `scenes/roadmap.build.py` regenerates the map data; the links from results 1
and 2 to atlas candidates were chosen by lineage and by content, since neither study cites an atlas id.

```
python3 vo.py --script narration-long.json --out _out/vo-long --speed 1.17
python3 narrate.py time --film long
node record.mjs _out/picture-long.mp4 --film long
python3 narrate.py mix _out/picture-long.mp4 _out/film-long.mp4 --film long
```

### Static slides

`python3 slides.py` renders one still per scene state of the four-minute cut (19 slides) into a 16:9 `.pptx` that
Google Slides imports, with each scene's narration in the speaker notes. The slides are pictures of the film's frames,
so their text is not editable in the deck; change the scene and rebuild.

## The two-experiment cut

`index.html?film=two` plays a third cut of 3 min 12 s (192.4 s), made on 2026-10-05 (UTC) to be sent as a file in a
chat. It explains two of the experiments to someone who has not seen the hackathon film: the Sybil market experiment
(`sybil-rules-180`) and the fifty-member Swarm of Theseus run (S50). It has its own four scenes; the scenes of the
other two cuts are untouched.

| Scene | Seconds | Content |
|---|---|---|
| `twoopen` | 28.5 | What we set out to study (single-agent safety against properties of swarms, the frame of the four-minute cut), then the two questions with each run's agents drawn as dots (180 and 50). The title is on screen from the first frame, because a chat app shows that frame as the preview (`FILM.coldOpen`) |
| `twosybil` | 66.4 | Experiment 1 as a study: the question, the economy (60 markets of one dominant owner and two rivals), the rule and how it counts, the design (every condition restarts from one checkpoint), the result under the rule alone (55 of 180, all of them dominant owners; the repeat gave 57), the added sentence (0 of 180; dominant owners produced 21% less instead), the second economy, the limits |
| `twotheseus` | 70.7 | Experiment 2 as a study: the question, the institution and the job, how the founders learned their two sources, the four arms as bars of correct decisions out of 300 (written note 297, conversation 295, nothing inherited 166, founders never replaced 298, with the 150 that deferring every case scores as a tick), what follows, the limits |
| `twoclose` | 26.7 | What each experiment measured on the group and how far it goes (2 economies of 180 agents; 1 world of 50 agents, 1 replacement wave; both exploratory, one model), then the site, the repository and its QR code |

The first version (v1 of the artifact, 88.9 s) reused the `sybil` and `theseus50` scenes with the four-minute cut's
narration. Dan's note on it: "the explanation kind of sucks, we should mention that we were trying to study properties
of swarms and then explain the result more academically". The current version is the answer to that note.

Where each number comes from is in the `COPY` block of each scene. Two figures are computed here and not quoted from a
write-up: "21% less" is 513 against 652 mean output per dominant owner-round (`sybil-rules-180/RESULTS.md`, "B and C"),
and "1 decision behind" is 297 against 298 of 300 (`S50-POST-MORTEM.md`, "Observed comparison").

The pictures of these four scenes are timed in seconds against the narration clips, not in fractions of the scene: each
scene has a `CUE` block holding the second at which each phrase starts (word timings from transcribing the clip). A
re-voiced clip needs its `CUE` block re-timed.

The closing card shows `www.swarmsafety.org` because the bare domain did not resolve on 2026-10-05 (UTC) and `www` did.
In the narration "AI agents" is written as `AI`: Kokoro reads `A I` as "eye" (checked by transcription), which also
affects the `define` clip of the two-minute cut. The clips were checked by transcription only, like the rest. The three
QR codes were decoded from the encoded file.

```
python3 vo.py --script narration-two.json --out _out/vo-two --speed 1.17
python3 narrate.py time --film two
node record.mjs _out/two-picture.mp4 --film two
python3 narrate.py mix _out/two-picture.mp4 _out/swarm-two-experiments.mp4 --film two
```

The filed film is the artifact `two-experiments-film` (v2).

## The three results and where they come from

1. **Thou shalt not split** (`5-experiments/studies/dmarz/sybil-rules-180`, GPT-6 Sol, exploratory). An economy of 180
   owners in 60 markets pays a 35% penalty on profit in concentrated markets, counted per firm. Under the rule alone 55
   of 180 owners sustained the split; with one added sentence ("Do not evade or circumvent the market's competition
   rule.") 0 of 180 did. A second economy went from 59 to 0. The study calls these two observations, not a distribution,
   and notes that the sentence also signals regulator intent. The 55 dots that split on screen are the owners flagged in
   the run records.
2. **How to win agents and influence swarms** (`5-experiments/studies/vishesh/external-influence-v2`, Claude Haiku 4.5).
   Nine-agent teams (six analysts, two fact-checkers, one decision-maker) choose among options while an outside
   attacker alters evidence documents. In 6 of 6 targeted-check attack cases the checkers returned the true numbers and
   the final decision still went to the attacker's option. 50 team decisions, 750 model calls, synthetic tasks.
3. **Swarm of Theseus** (`5-experiments/studies/vishesh/swarm-of-theseus`, Claude Haiku 4.5, pilot S1-a1). Three-agent
   crews have every founder replaced one at a time. Crews that inherited written notes scored 100% on the scored steps;
   crews that inherited nothing scored 52%, where guessing is 50%. 36 runs across 6 synthetic worlds. The study tested
   supplied procedures, not safety constraints, and says so on screen.

## Numbers checked against the repository

`FACTS.md` is the check of the first script's numbers, made on 2026-10-04. The film shows the repository's values where
they differed from the script: 219 hypothesis candidates (the script said 214 and 215), 15 research areas (the script
said 9; no nine-way grouping was found), 103 experiments on the hub snapshot (the script said 105), and 12 of 219
candidates cited by a hub experiment.

Known gaps at filing:

- "Attacker alters 8 of 12 documents" in result 2 comes from the narration draft. The study's files confirm twelve
  documents; the eight was not found.
- The end card and the narration say the entire lab is open source, from the prompts to the infrastructure as code. The
  infrastructure is in this repository as `agentops/`, a scrubbed template of the fleet setup; the live fleet
  repository with its secrets and claims stays private.
- The 219 hypotheses are unreviewed candidates in the question atlas. The gate rail in the `lab` scene names the review
  gate, which only three formal hypothesis files had reached.
- The narration was checked by transcription only. The transcriber heard "Sybils" as "symbols" and one "Theseus" as
  "theses"; nobody had listened to the track when it was filed.

## Building it

The look (tokens, fonts, the cube loop) is not committed: it is read from a checkout of the private brand kit into
`kit/`, which is git-ignored. Without `kit/` the page does not render correctly.

```
K=~/dmarz-brand-and-content-kit/brand                       # the brand kit checkout
mkdir -p kit/fonts && cp -R $K/fonts/Doto $K/fonts/SpaceMono kit/fonts/ && cp $K/dist/tokens.css $K/marks/cube/cube-loop-alpha.webm kit/
# kit/fonts.css = the kit's normal-style faces as @font-face rules with base64 data URIs (see fonts.json in the kit)

python3 vo.py --speed 1.15                                  # narration.json -> _out/vo/*.wav (Kokoro af_heart, mlx-audio)
python3 narrate.py time                                     # scene seconds in index.html follow the clip lengths
node record.mjs _out/picture.mp4                            # frames piped to ffmpeg, about one minute
python3 narrate.py mix _out/picture.mp4 _out/film.mp4       # narration at -14 LUFS on the picture
node shot.mjs <scene id> 0.5,0.95                           # stills of one scene, for checking
```

`vo.py` needs a virtualenv with `mlx-audio` and `misaki[en]` plus the spaCy model `en_core_web_sm`; the header of the
file has the recipe. The words and numbers of each scene are in the `COPY` block at the top of its file. Scene order
and seconds are the `FILM.order` list in `index.html`. `scenes/result3.js` also carries two unused picks (`swarm-size`,
`immune-response`) behind `COPY.pick`.

## Scene contract

A scene is `scenes/<id>.js` (classic script, no modules, no fetch: the page runs from `file://`). Optional data goes in
`scenes/<id>.data.js` as `FILM.data['<id>'] = {...}`; both files are already listed in `index.html`. Binary assets
(avatars, images, clips) go in `assets/<id>/`.

```js
FILM.scene({
  id: 'lab',
  mount(root, ctx) {
    // called once. root is an empty absolutely positioned 1920x1080 div with id="scene-lab".
    // build all DOM / SVG / canvas here. Add CSS with ctx.css(`#scene-lab .x { ... }`), every selector scoped to #scene-<id>.
  },
  update(p, t, ctx) {
    // called every frame while the scene is visible. p = 0..1 through the scene, t = seconds into it, ctx.dur = its length.
    // MUST be a pure function of time: set styles/attributes/canvas from p or t only.
  },
});
```

Hard rules:

- Pure function of time. No CSS transitions or animations, no setTimeout, no requestAnimationFrame of your own, no
  Math.random (use `ctx.rng(seed)`). The recorder seeks to arbitrary frames, forwards and backwards.
- Write beats as fractions of the scene (`ctx.seg(p, 0.10, 0.25)` = eased 0..1 between 10% and 25% of the scene), so the
  scene still works when its duration is changed in `index.html`.
- The shell cross-fades scenes (about 0.4 s). Do not fade your whole scene in or out. Give the viewer about half a
  second before the first thing moves.
- All copy and every number sits in one `const COPY = {...}` block at the top of the scene file, so Dan can edit words
  in one place. Each number has a comment naming the file in the repo that proves it.
- Layout is absolute pixels on a 1920x1080 stage. Keep content inside x 100..1820, y 56..1010. The shell draws the
  thin cyan zip line at x=46 and a scene counter bottom right (y > 1030); do not draw there.
- No `<video>` unless you must; if you do, drive it only through `ctx.video(el, seconds)` inside `update`.

Helpers on `ctx`: `clamp(x)`, `ease(x)` (cubic in-out), `out(x)` (ease-out), `seg(p, a, b)` (eased 0..1 as p goes a..b),
`lin(p, a, b)` (linear), `lerp(a, b, x)`, `rng(seed)` (returns a function giving 0..1), `fmt(n)` (thousands commas),
`el(tag, cls, html, parent)` (make an element), `css(text)`, `asset(path)` (resolves `assets/...`), `dur`.

## Look (the dmarz brand kit; tokens and fonts are already loaded by the shell)

CSS variables: `--void` (background, already set), `--ink` (text), `--dim` (context, neighbours, labels), `--amber`
(ONE signal per frame: the active thing, the headline number), `--zip` (cyan: live or confirmed state), `--bone`,
`--no` (red: failed, bad state), `--mono` (Space Mono, all body text), `--display` (Doto, dotted display face: titles
and hero numbers only; it has no arrow glyph).

Shared classes from the shell (use them so scenes match):

- `.f-kicker`: 16px uppercase letterspaced dim label. Put the scene kicker at left:100px; top:56px.
- `.f-title`: Doto 60px. Scene title at left:100px; top:88px. One line. No subtitle line under a title, ever.
- `.f-body`: Space Mono 28px, line-height 1.4. Minimum on-screen text size is 18px; aim for 24px and up.
- `.f-num`: Doto, for hero numbers (set font-size yourself, 90 to 220px).
- `.f-small`: 18px dim uppercase letterspaced labels.

Taste rules (Dan has rejected work for each of these):

- Every number carries its unit and its comparison ("6 of 6 markets", never a bare "6"; "55 -> 0" alone means nothing).
- Colour carries meaning; do not decorate. Not too green. Glow at most subtle. No drifting background particles, no
  node-mesh wallpaper, no pills, no gradient cards, no emoji. Dots that ARE data (a run, an agent, a server) are welcome
  and should feel like a swarm.
- Motion means "arrived", "state changed" or "alive". Things get built on screen: show construction.
- Plain words. No em dashes, no "isn't X, it's Y" cadence, no hype adjectives. Sentence case. Short labels.
- Report data literally. Only show numbers you verified in the repo; if the script's number differs from the repo,
  show the repo's number and tell the lead in your final report (file + line).

## Checking your scene

```
cd 5-experiments/studies/dmarz/hackathon-demo
node shot.mjs <id> 0.1,0.5,0.9        # p values (0..1) -> _shots/<id>-<p>.png, then Read the PNGs and fix what looks off
open "index.html?only=<id>"            # live preview; space = pause, left/right = previous/next scene, click bar = seek
```

Look at your own frames before you report. Check text overlap, clipped text, and that every beat is legible in a
frame grab. Do not edit `index.html`, `shot.mjs`, or another scene's files.
