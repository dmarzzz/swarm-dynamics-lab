# Living library

`import { GraphView, HeroSwarm } from './graph'`

Both mount without props and share a cached fetch of `data/graph.json`, `library.json`, and `timeline.json` relative to Vite's base URL. Optional props: `data: {graph, library, timeline?}`, `dataUrl`, `className`, and `onSelect(entry)`. GraphView has its own inspector even when onSelect is supplied. HeroSwarm calls onSelect for integration with the overview's source drawer.

Styles are scoped to `.swarm-root` and consume U's paper/ink/rule/accent/font tokens. The renderer batches native WebGL points and sampled edges in two draw calls; falls back to Canvas 2D when WebGL is unavailable. No additional npm dependency. Topic cohesion and mean-velocity alignment use O(nodes + explicit wikilinks) per frame. Links from library metadata exert weak symmetric attraction. Shared-topic graph edges are visualization only. Deterministic starting positions avoid a layout explosion. Simulation is illustrative, not an embedding or similarity metric.

Search, topic selection, source list, and inspector are keyboard usable. Pan and zoom are optional pointer controls. Reduced motion stops simulation automatically; explicit pause is independent. Offscreen/hidden fields stop rendering. The replay uses actual current-source first-add timestamps from noon ET October 3. Historical deleted sources are not invented to match the timeline totals. The snapshot end is the last current-source addition, not wall-clock now.

Canvas `data-perf` reports renderer, measured frame frequency, average JS update/draw submission milliseconds, and node count. This is not GPU timing. FPS measured in software-rendered headless Chromium is not evidence of laptop hardware FPS.

## Verification, October 3

TypeScript strict check and Vite production build pass. Playwright exercised title search, source inspection, timestamp replay, dark theme, 390px mobile (no horizontal overflow), reduced-motion preference, and forced Canvas fallback, with no browser exceptions. Screenshots are in `/home/shad0w/.moltbot/projects/swarm-hackathon/dash-shots/graph/`.

Headless Chromium with ANGLE SwiftShader, 1440x1100: 2,463 real sources, 38.5 fps and 0.85 ms average JS simulation/render submission. Synthetic 3,000-source load at 1200x900: 25.2 fps, 1.21 ms JS. Forced Canvas fallback: 9 fps, 2.01 ms JS on this software-rendered host. GPU laptop 60 fps has not been verified; do not present these headless measurements as hardware performance. FPS fluctuates with shared host load and screenshot capture.
