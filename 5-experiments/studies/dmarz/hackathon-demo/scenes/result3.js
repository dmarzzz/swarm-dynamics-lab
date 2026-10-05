// Spare third result (off by default: set ['result3', 25] in index.html FILM.order to show it).
// Change COPY.pick to switch between the three prepared results. Viz data: scenes/result3.data.js.
(() => {
const COPY = {
  pick: 'influence',             // 'swarm-size' | 'influence' | 'immune-response'
  kicker: 'result 3',
  // The film's second result. Source: 5-experiments/studies/vishesh/external-influence-v2/reviews/quality-post.md
  influenceFilm: {
    kicker: 'result 2',
    title: 'How to win agents and influence swarms',
    nDocs: 12, nAltered: 8,                                  // attacker could alter 8 of 12 evidence documents
    docsLabel: 'attacker alters 8 of 12 documents',
    nAnalysts: 6, nCheckers: 2,                              // nine-agent team: 6 analysts, 2 fact-checkers, 1 decision-maker
    analysts: '6 analysts', checkers: '2 fact-checkers', decider: '1 decision-maker',
    checkLabel: 'checkers return the true numbers',          // quality-post.md: both checkers returned the correct values
    decisionLabel: 'final decision: the attacker\'s option',
    hero: '6 of 6',                                          // quality-post.md: "All six targeted-check misleading/syndication cases show this discrepancy."
    heroLabel: 'targeted attacks won, even after the checkers were right',
    foot: '50 team decisions, 750 model calls, Claude Haiku 4.5, synthetic tasks', // quality-post.md S1: 50 outcomes, 750 calls; model-config.json
    footer: '9 agents per team / Claude Haiku 4.5 / external-influence-v2, 50 team decisions / vishesh',
  },
  picks: {
    // Research question 3 (swarm size). Source: 5-experiments/studies/vishesh/optimal-swarm-size/reviews/q-a6-post.md
    // and results/q-a6/analysis.json (root 5, parallel).
    'swarm-size': {
      title: 'Two agents: faster, and more wrong',
      vizNote: 'one 16-question task, same questions, split in parallel',
      lane1: '1 agent', lane2: '2 agents',
      score1: '11 of 16 right',        // q-a6-post.md root 5 parallel: quality .6875 = 11/16
      score2: '5 of 16 right',         // q-a6-post.md root 5 parallel: quality .3125 = 5/16
      time1: '25.2 s',                 // analysis.json pairs[2].n1.elapsed_s = 25.17
      time2: '17.0 s',                 // analysis.json pairs[2].n2.elapsed_s = 17.02
      heroLabel: 'with 2 agents',
      hero: '5 of 16',                 // same as score2
      unit: 'answers right, down from 11 of 16 with 1 agent',
      compare: 'Done in 17.0 s instead of 25.2 s. The other parallel task: 13 of 16 down to 11 of 16.', // q-a6-post.md root 4 parallel: .8125 → .6875
      model: 'Claude Haiku 4.5 · 8 episodes, 144 model calls', // q-a6-post.md: "8/8 ... 144 model calls", claude-haiku-4-5-20251001
      limit: 'Limit: 2 task roots, one response per condition, one synthetic task family. A pilot, no interval.', // q-a6-post.md, sample_size gap
    },
    // Research question 2 (fault tolerance). Source: 5-experiments/studies/vishesh/external-influence-v2/reviews/quality-post.md
    'influence': {
      title: 'Correct checks, attacker still chosen',
      vizNote: 'one nine-agent team, procurement case',
      doc: ['edited', 'evidence'],
      analysts: '6 analysts', analystsNote: '5 of 6 swayed',   // quality-post.md: "five of six analysts favored FinchSupport"
      checkers: '2 checkers', checkersNote: 'true numbers',    // quality-post.md: both checkers returned the correct values
      chair: 'chair', bad: 'attacker\'s option', good: 'correct option',
      heroLabel: 'attacks with checks',
      hero: '6 of 6',                  // quality-post.md: "All six targeted-check misleading/syndication cases show this discrepancy."
      unit: 'the chair chose the attacker\'s option after the checkers returned the true numbers',
      compare: 'Replaying the same check values by rule picks the correct option in all 6.', // quality-post.md: "A mechanical replay ... selects correctly in those six."
      model: 'Claude Haiku 4.5 · 50 team outcomes, 750 model calls', // quality-post.md S1: 50 outcomes, 750 calls; model-config.json
      limit: 'Limit: one task per application (3 tasks), 50 dependent outcomes. A pilot, not a robustness estimate.', // quality-post.md "Reconciled results"
    },
    // Research question 3 (swarm size). Source: 5-experiments/studies/vishesh/immune-response-v3/scenario-study/ASSESSMENT.md
    'immune-response': {
      title: 'Team of 4 waited. One agent acted',
      vizNote: 'three services, six ticks each',
      team: 'team of 4', solo: 'one agent',
      broken: 'broken', healthy: 'healthy',
      say: '"looks fine"',             // ASSESSMENT.md: "reviewers explicitly described a failing data-readability probe as healthy"
      tally: ['0 of 6 healthy', '5 of 6 healthy', '6 of 6 healthy', '3 of 6 healthy'], // ASSESSMENT.md "Single commander" table: team/solo broken, team/solo healthy
      heroLabel: 'team of 4, broken service',
      hero: '0 of 6',                  // ASSESSMENT.md: Stale advice, team retain healthy ticks 0/6
      unit: 'healthy ticks. One agent alone: 5 of 6',   // ASSESSMENT.md: Stale advice, solo retain 5/6
      compare: 'On a service that was already healthy, the team kept 6 of 6 and the lone agent kept 3 of 6.', // ASSESSMENT.md: Healthy false alarm 6/6 vs 3/6
      model: 'Claude Haiku 4.5 · team 12 episodes, 108 calls · solo 4 episodes, 24 calls', // ASSESSMENT.md "Evidence and cost"; model-config.json
      limit: 'Limit: single samples, fixed order, one constructed three-service exercise. Not proof the reviewers caused it.', // ASSESSMENT.md
    },
  },
};

const NS = 'http://www.w3.org/2000/svg';
const INK = 'var(--ink)', DIM = 'var(--dim)', ZIP = 'var(--zip)', NO = 'var(--no)';
const FAINT = 'rgba(127,136,150,.55)';
const sv = (tag, attrs, parent) => { const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]); if (parent) parent.appendChild(n); return n; };
const txt = (g, x, y, s, size, fill, anchor) => { const t = sv('text', { x, y, 'text-anchor': anchor || 'start' }, g);
  t.setAttribute('style', `font-family:var(--mono);font-size:${size}px;fill:${fill}`); t.textContent = s; return t; };
const op = (n, v) => n.setAttribute('opacity', v);
// a line that draws itself: pathLength=1, dash offset 1 -> 0
const draw = (n, v) => { n.setAttribute('stroke-dashoffset', 1 - v); n.setAttribute('visibility', v <= 0.002 ? 'hidden' : 'visible'); };
const dpath = (g, d, stroke, w) => sv('path', { d, fill: 'none', stroke, 'stroke-width': w, 'stroke-linecap': 'round',
  pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, g);

// ---- each builder draws in a 440 x 275 box (the showcase card box) and returns update(v), v = 0..1 through the build ----
const VIZ = {
  'swarm-size'(g, c, d, ctx) {
    const X0 = 14, PX = 268 / d.n1.seconds, TILE_H = 34, RUN = 0.9;
    const lanes = [
      { n: 1, label: c.lane1, score: c.score1, time: c.time1, data: d.n1, labelY: 44, railY: 60, tileY: 70 },
      { n: 2, label: c.lane2, score: c.score2, time: c.time2, data: d.n2, labelY: 160, railY: 176, tileY: 190 },
    ];
    txt(g, X0, 14, c.vizNote, 8.4, DIM);
    const xPair = X0 + d.n2.seconds * PX;
    const ghost = sv('line', { x1: xPair, x2: xPair, y1: lanes[0].tileY - 6, y2: lanes[1].tileY + TILE_H,
      stroke: FAINT, 'stroke-width': 0.8, 'stroke-dasharray': '2 3', opacity: 0 }, g);
    sv('line', { x1: X0 - 0.5, x2: X0 - 0.5, y1: lanes[0].railY - 8, y2: lanes[1].tileY + TILE_H + 4, stroke: FAINT, 'stroke-width': 0.8 }, g);
    const L = lanes.map((ln) => {
      const span = ln.data.seconds * PX, step = span / d.items, w = Math.max(5, step - 4);
      txt(g, X0 + 2, ln.labelY, ln.label, 11, INK);
      const ys = ln.n === 1 ? [ln.railY] : [ln.railY - 4.5, ln.railY + 4.5];
      const rails = ys.map(y => sv('line', { x1: X0, x2: X0, y1: y, y2: y, stroke: FAINT, 'stroke-width': 0.8, 'stroke-dasharray': '1 3' }, g));
      const heads = ys.map(y => sv('circle', { cx: X0, cy: y, r: 3.6, fill: INK }, g));
      const tiles = [];
      for (let i = 0; i < d.items; i++) {
        const wrong = ln.data.wrong.includes(i);
        tiles.push(sv('rect', { x: X0 + i * step + (step - w) / 2, y: ln.tileY, width: w, height: TILE_H, rx: 1.2,
          fill: wrong ? NO : 'none', 'fill-opacity': wrong ? 0.85 : 0, stroke: wrong ? NO : ZIP, 'stroke-width': 1, opacity: 0 }, g));
      }
      const time = txt(g, X0 + span, ln.tileY + TILE_H + 13, ln.time, 9.6, DIM, 'end');
      const score = txt(g, X0 + span + 12, ln.tileY + TILE_H / 2 + 4, ln.score, 11, ln.n === 2 ? NO : INK);
      return { span, rails, heads, tiles, time, score, tEnd: RUN * ln.data.seconds / d.n1.seconds };
    });
    return (v) => {
      for (const k of L) {
        const e = ctx.clamp(v / k.tEnd), x = X0 + k.span * e;   // constant pace, lane length = real seconds
        k.heads.forEach(h => h.setAttribute('cx', x));
        k.rails.forEach(r => r.setAttribute('x2', x));
        k.tiles.forEach((r, i) => op(r, ctx.ease(ctx.clamp((e * d.items - i) / 1.2))));
        const s = ctx.ease(ctx.clamp((v - k.tEnd) / 0.08));
        op(k.time, s); op(k.score, s);
      }
      op(ghost, 0.9 * ctx.ease(ctx.clamp((v - L[1].tEnd) / 0.08)));
    };
  },

  'influence'(g, c, d, ctx) {
    const ax = 160, chair = { x: 290, y: 132 }, bad = { x: 404, y: 62 }, good = { x: 404, y: 206 };
    const ay = i => 52 + i * 20, cy = i => 200 + i * 24;
    const sway = i => i !== 3 && i < d.swayed + 1;      // 5 of 6 lean to the attacker's option
    const docOut = { x: 66, y: 128 };
    txt(g, 14, 14, c.vizNote, 8.4, DIM);
    const doc = sv('g', { opacity: 0 }, g);
    sv('path', { d: 'M22 102 h28 l12 12 v40 h-40 z M50 102 v12 h12', fill: 'none', stroke: NO, 'stroke-width': 1.2 }, doc);
    sv('path', { d: 'M29 124 h26 M29 132 h20 M29 140 h26 M29 148 h14', fill: 'none', stroke: NO, 'stroke-width': 0.9, opacity: 0.7 }, doc);
    txt(doc, 42, 172, c.doc[0], 9, NO, 'middle'); txt(doc, 42, 184, c.doc[1], 9, NO, 'middle');
    const feed = [], toChair = [], agents = [], cks = [], ckLines = [];
    for (let i = 0; i < d.analysts; i++) feed.push(dpath(g, `M${docOut.x} ${docOut.y} L${ax - 8} ${ay(i)}`, NO, 0.8));
    feed.forEach(n => n.setAttribute('opacity', 0.55));
    for (let i = 0; i < d.analysts; i++) toChair.push(dpath(g, `M${ax + 8} ${ay(i)} L${chair.x - 14} ${chair.y}`, sway(i) ? NO : FAINT, 1));
    for (let i = 0; i < d.checkers; i++) ckLines.push(dpath(g, `M${ax + 8} ${cy(i)} L${chair.x - 14} ${chair.y + 4}`, ZIP, 1.2));
    const notTaken = sv('path', { d: `M${chair.x + 14} ${chair.y + 8} L${good.x - 17} ${good.y - 7}`, fill: 'none', stroke: ZIP,
      'stroke-width': 1.1, 'stroke-dasharray': '3 5', opacity: 0 }, g);
    for (let i = 0; i < d.analysts; i++) agents.push(sv('circle', { cx: ax, cy: ay(i), r: 6, fill: 'var(--void)', stroke: INK, 'stroke-width': 1.2 }, g));
    for (let i = 0; i < d.checkers; i++) cks.push(sv('rect', { x: ax - 6, y: cy(i) - 6, width: 12, height: 12, fill: 'var(--void)', stroke: INK, 'stroke-width': 1.2 }, g));
    const aLab = txt(g, ax, 32, c.analysts, 9, DIM, 'middle');
    const aNote = txt(g, ax - 14, ay(5) + 20, c.analystsNote, 8.4, NO, 'middle');
    const cLab = txt(g, ax - 14, cy(0) + 4, c.checkers, 9, DIM, 'end');
    const cNote = txt(g, ax - 14, cy(1) + 4, c.checkersNote, 8.4, ZIP, 'end');
    const badC = sv('circle', { cx: bad.x, cy: bad.y, r: 15, fill: NO, 'fill-opacity': 0, stroke: NO, 'stroke-width': 1.3 }, g);
    txt(g, bad.x, bad.y - 23, c.bad, 9, NO, 'middle');
    sv('circle', { cx: good.x, cy: good.y, r: 15, fill: 'none', stroke: ZIP, 'stroke-width': 1.3 }, g);
    txt(g, good.x, good.y + 30, c.good, 9, ZIP, 'middle');
    const dec = dpath(g, `M${chair.x + 13} ${chair.y - 7} L${bad.x - 17} ${bad.y + 8}`, NO, 2.6);
    sv('circle', { cx: chair.x, cy: chair.y, r: 13, fill: 'var(--void)', stroke: INK, 'stroke-width': 1.4 }, g);
    sv('circle', { cx: chair.x, cy: chair.y, r: 4, fill: INK }, g);
    txt(g, chair.x, chair.y + 30, c.chair, 9, INK, 'middle');
    return (v) => {
      op(doc, ctx.seg(v, 0.0, 0.08));
      feed.forEach((n, i) => draw(n, ctx.seg(v, 0.10 + i * 0.015, 0.24 + i * 0.015)));
      agents.forEach((n, i) => { const s = sway(i) ? ctx.seg(v, 0.30 + i * 0.02, 0.36 + i * 0.02) : 0;
        n.setAttribute('fill', s > 0.5 ? NO : 'var(--void)'); n.setAttribute('stroke', s > 0.5 ? NO : INK); });
      op(aNote, ctx.seg(v, 0.40, 0.46));
      toChair.forEach((n, i) => draw(n, ctx.seg(v, 0.44 + i * 0.015, 0.56 + i * 0.015)));
      op(aLab, 1); op(cLab, 1);
      cks.forEach((n, i) => { const s = ctx.seg(v, 0.60 + i * 0.03, 0.66 + i * 0.03);
        n.setAttribute('fill', s > 0.5 ? ZIP : 'var(--void)'); n.setAttribute('stroke', s > 0.5 ? ZIP : INK); });
      op(cNote, ctx.seg(v, 0.64, 0.70));
      ckLines.forEach((n, i) => draw(n, ctx.seg(v, 0.66 + i * 0.03, 0.76 + i * 0.03)));
      op(notTaken, 0.75 * ctx.seg(v, 0.76, 0.84));
      draw(dec, ctx.seg(v, 0.86, 0.97));
      badC.setAttribute('fill-opacity', 0.28 * ctx.seg(v, 0.95, 1));
    };
  },

  'immune-response'(g, c, d, ctx) {
    const PXS = [14, 240], ROWY = [112, 216], NODE = [56, 96, 136], NR = 11, PIP = 12, PG = 3, PIPX = 162;
    txt(g, 14, 12, c.vizNote, 8.4, DIM);
    const glyph = (x, y, r) => [[0, -1], [-1, 0], [1, 0], [0, 1]].forEach(([a, b]) => sv('circle', { cx: x + a * r * 1.9, cy: y + b * r * 1.9, r, fill: INK }, g));
    glyph(PXS[0] + 9, 34, 3); txt(g, PXS[0] + 26, 38, c.team, 11, INK);
    sv('circle', { cx: PXS[1] + 9, cy: 34, r: 3.4, fill: INK }, g); txt(g, PXS[1] + 26, 38, c.solo, 11, INK);
    [[24, ROWY[0] - 56], [ROWY[0] - 32, ROWY[1] - 56], [ROWY[1] - 32, 268]].forEach(([a, b]) =>
      sv('line', { x1: 227.5, x2: 227.5, y1: a, y2: b, stroke: FAINT, 'stroke-width': 0.8 }, g));
    txt(g, 227.5, ROWY[0] - 40, c.broken.toUpperCase(), 8.4, DIM, 'middle');
    txt(g, 227.5, ROWY[1] - 40, c.healthy.toUpperCase(), 8.4, DIM, 'middle');
    // cell: pi 0 team / 1 solo; ri 0 broken / 1 healthy; kind null | 'fix' | 'harm'; a..b = its slice of the build
    const cells = [];
    const cell = (pi, ri, healthy, kind, tally, a, b) => {
      const x0 = PXS[pi], y = ROWY[ri], startBad = ri === 0;
      if (pi === 0) glyph(x0 + 16, y, 4.6); else sv('circle', { cx: x0 + 16, cy: y, r: 5.2, fill: INK }, g);
      const [gx, wx, sx] = NODE.map(n => x0 + n);
      sv('line', { x1: gx + NR, x2: wx - NR, y1: y, y2: y, stroke: FAINT, 'stroke-width': 1 }, g);
      sv('line', { x1: wx + NR, x2: sx - NR, y1: y, y2: y, stroke: FAINT, 'stroke-width': 1 }, g);
      sv('circle', { cx: gx, cy: y, r: NR, fill: 'var(--void)', stroke: ZIP, 'stroke-width': 1.3 }, g);
      sv('circle', { cx: sx, cy: y, r: NR, fill: 'var(--void)', stroke: ZIP, 'stroke-width': 1.3 }, g);
      const worker = sv('circle', { cx: wx, cy: y, r: NR, fill: 'var(--void)', stroke: startBad ? NO : ZIP, 'stroke-width': 1.3 }, g);
      const k = 4.5;
      const cross = sv('path', { d: `M${wx - k} ${y - k}L${wx + k} ${y + k}M${wx + k} ${y - k}L${wx - k} ${y + k}`, stroke: NO,
        'stroke-width': 1.4, 'stroke-linecap': 'round', opacity: startBad ? 1 : 0 }, g);
      const reach = kind ? dpath(g, `M${x0 + 24} ${y - 4} Q ${(x0 + 24 + wx) / 2} ${y - 40} ${wx - 2} ${y - NR - 3}`, kind === 'fix' ? ZIP : NO, 1.4) : null;
      const pips = [];
      for (let i = 0; i < d.ticks; i++) {
        const px = x0 + PIPX + (i % 3) * (PIP + PG), py = y - PIP - PG / 2 + Math.floor(i / 3) * (PIP + PG);
        sv('rect', { x: px, y: py, width: PIP, height: PIP, rx: 1.2, fill: 'none', stroke: FAINT, 'stroke-width': 0.8 }, g);
        const good = i < healthy;
        pips.push(sv('rect', { x: px, y: py, width: PIP, height: PIP, rx: 1.2, fill: good ? 'none' : NO, stroke: good ? ZIP : NO,
          'stroke-width': 1.2, opacity: 0 }, g));
      }
      const lab = txt(g, x0 + PIPX + 3 * PIP + 2 * PG, y + PIP + PG + 14, tally, 8.4, healthy === 0 ? NO : DIM, 'end');
      cells.push({ kind, startBad, worker, cross, reach, pips, lab, a, b });
    };
    cell(0, 0, d.teamBroken, null, c.tally[0], 0.08, 0.34);
    cell(1, 0, d.soloBroken, 'fix', c.tally[1], 0.32, 0.58);
    cell(0, 1, d.teamHealthy, null, c.tally[2], 0.56, 0.78);
    cell(1, 1, d.soloHealthy, 'harm', c.tally[3], 0.76, 1.0);
    const say = txt(g, PXS[0] + 2, ROWY[0] - 26, c.say, 11, NO);
    return (v) => {
      op(say, ctx.seg(v, 0.02, 0.10));
      for (const k of cells) {
        const q = ctx.lin(v, k.a, k.b);                       // 0..1 through this cell's slice
        if (k.reach) {
          draw(k.reach, ctx.seg(q, 0.0, 0.3));
          const hit = q > 0.3;
          if (k.kind === 'fix') { k.worker.setAttribute('stroke', hit ? ZIP : NO); op(k.cross, hit ? 0 : 1); }
          if (k.kind === 'harm') { k.worker.setAttribute('stroke', hit ? NO : ZIP); op(k.cross, hit ? 1 : 0); }
        }
        k.pips.forEach((r, i) => op(r, ctx.seg(q, 0.32 + i * 0.08, 0.42 + i * 0.08)));
        op(k.lab, ctx.seg(q, 0.86, 1));
      }
    };
  },
};

// ---- the influence pick as a full-stage film scene (1920 x 1080), returns update(p) ----
function buildInfluence(root, c, ctx) {
  const abs = (cls, html, css) => { const n = ctx.el('div', cls, html, root); n.style.cssText = 'position:absolute;' + css; return n; };
  abs('f-kicker', c.kicker, 'left:100px;top:50px;font-size:22px');
  abs('f-title', c.title, 'left:100px;top:88px;white-space:nowrap');
  const svg = sv('svg', { viewBox: '0 0 1920 1080', width: 1920, height: 1080 }, root);
  svg.setAttribute('style', 'position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible');
  const g = sv('g', {}, svg);
  const CY = 410, DX = 100, DS = 44, DG = 16, AX = 760, KX = 1160, FX = 1560, LY = 590;
  const ay = i => CY + (i - (c.nAnalysts - 1) / 2) * 44, ky = i => CY + (i - (c.nCheckers - 1) / 2) * 72;
  const order = [1, 6, 3, 8, 4, 11, 9, 2, 0, 5, 7, 10].filter(i => i < c.nDocs).slice(0, c.nAltered);
  // lines first, so dots sit on top
  const feed = [], mid = [], out = [];
  for (let i = 0; i < c.nAnalysts; i++) { const n = dpath(g, `M${DX + 4 * DS + 3 * DG + 16} ${CY} L${AX - 24} ${ay(i)}`, NO, 2); n.setAttribute('opacity', 0.6); feed.push(n); }
  for (let i = 0; i < c.nAnalysts; i++) for (let j = 0; j < c.nCheckers; j++) mid.push(dpath(g, `M${AX + 24} ${ay(i)} L${KX - 28} ${ky(j)}`, FAINT, 1.5));
  for (let j = 0; j < c.nCheckers; j++) out.push(dpath(g, `M${KX + 28} ${ky(j)} L${FX - 40} ${CY}`, ZIP, 2.5));
  const docs = [], docsRed = [];
  for (let i = 0; i < c.nDocs; i++) {
    const x = DX + (i % 4) * (DS + DG), y = CY - 82 + Math.floor(i / 4) * (DS + DG);
    docs.push(sv('rect', { x, y, width: DS, height: DS, rx: 3, fill: 'none', stroke: DIM, 'stroke-width': 2, opacity: 0 }, g));
    docsRed[i] = sv('rect', { x, y, width: DS, height: DS, rx: 3, fill: NO, stroke: NO, 'stroke-width': 2, opacity: 0 }, g);
  }
  const analysts = [], checkers = [], checkersOn = [];
  for (let i = 0; i < c.nAnalysts; i++) analysts.push(sv('circle', { cx: AX, cy: ay(i), r: 15, fill: INK, opacity: 0 }, g));
  for (let j = 0; j < c.nCheckers; j++) {
    checkers.push(sv('circle', { cx: KX, cy: ky(j), r: 19, fill: INK, opacity: 0 }, g));
    checkersOn.push(sv('circle', { cx: KX, cy: ky(j), r: 19, fill: ZIP, opacity: 0 }, g));
  }
  const dec = sv('circle', { cx: FX, cy: CY, r: 30, fill: INK, opacity: 0 }, g);
  const decOn = sv('circle', { cx: FX, cy: CY, r: 30, fill: NO, opacity: 0 }, g);
  const lA = txt(g, AX, LY, c.analysts, 26, DIM, 'middle'), lK = txt(g, KX, LY, c.checkers, 26, DIM, 'middle');
  const lF = txt(g, FX, LY, c.decider, 26, DIM, 'middle');
  const lDocs = txt(g, DX, 290, c.docsLabel, 26, INK);
  const lCheck = txt(g, KX, 290, c.checkLabel, 26, ZIP, 'middle');
  const lDec = txt(g, 1800, 640, c.decisionLabel, 26, NO, 'end');
  [lA, lK, lF, lDocs, lCheck, lDec].forEach(n => op(n, 0));
  const hero = abs('f-num', c.hero, 'left:96px;top:690px;font-size:170px;line-height:1;color:var(--amber);white-space:nowrap');
  const heroLabel = abs('', c.heroLabel, 'left:800px;top:726px;width:800px;font-family:var(--mono);font-size:34px;line-height:1.35;color:var(--ink)');
  const foot = abs('', c.foot, 'left:100px;top:884px;font-family:var(--mono);font-size:24px;color:var(--dim);white-space:nowrap');
  abs('', c.footer, 'left:100px;top:966px;font-family:var(--mono);font-size:22px;color:var(--dim);white-space:nowrap');
  return (p) => {
    const S = (a, b) => ctx.seg(p, a, b);
    // beat A: the team, then the documents
    analysts.forEach((n, i) => op(n, S(0.03 + i * 0.008, 0.06 + i * 0.008)));
    op(lA, S(0.06, 0.10));
    checkers.forEach((n, j) => op(n, S(0.09 + j * 0.01, 0.12 + j * 0.01)));
    op(lK, S(0.10, 0.14));
    op(dec, S(0.13, 0.16)); op(lF, S(0.14, 0.18));
    docs.forEach((n, i) => op(n, S(0.17 + i * 0.003, 0.20 + i * 0.003)));
    op(lDocs, S(0.20, 0.24));
    order.forEach((di, k) => op(docsRed[di], S(0.21 + k * 0.009, 0.235 + k * 0.009)));
    // beat B: information moves through
    feed.forEach((n, i) => draw(n, S(0.31 + i * 0.006, 0.37 + i * 0.006)));
    mid.forEach((n, i) => draw(n, S(0.39 + i * 0.002, 0.44 + i * 0.002)));
    checkersOn.forEach((n, j) => op(n, S(0.455 + j * 0.012, 0.48 + j * 0.012)));
    op(lCheck, S(0.47, 0.51));
    out.forEach((n, j) => draw(n, S(0.51 + j * 0.01, 0.56 + j * 0.01)));
    op(decOn, S(0.57, 0.60)); op(lDec, S(0.585, 0.63));
    // beat C: the number
    op(g, 1 - 0.4 * S(0.65, 0.69));
    hero.style.opacity = S(0.66, 0.70);
    hero.style.transform = `translateY(${(1 - ctx.out(ctx.lin(p, 0.66, 0.70))) * 14}px)`;
    heroLabel.style.opacity = S(0.70, 0.75);
    foot.style.opacity = S(0.78, 0.83);
  };
}

FILM.scene({
  id: 'result3',
  mount(root, ctx) {
    if (COPY.pick === 'influence') { this.inf = buildInfluence(root, COPY.influenceFilm, ctx); return; }
    const c = COPY.picks[COPY.pick], d = (FILM.data['result3'] || {})[COPY.pick];
    if (!c || !d) throw new Error('result3: unknown COPY.pick "' + COPY.pick + '"');
    ctx.css(`
      #scene-result3 .viz { left: 65px; top: 196px; width: 1120px; height: 700px; }
      #scene-result3 .viz svg { display: block; width: 100%; height: 100%; overflow: visible; }
      #scene-result3 .col { left: 1270px; top: 236px; width: 550px; }
      #scene-result3 .col > * { position: static; }
      #scene-result3 .hero { font-size: 118px; color: var(--amber); margin: 14px 0 22px -4px; }
      #scene-result3 .unit { font-size: 28px; line-height: 1.35; color: var(--ink); }
      #scene-result3 .cmp { font-size: 24px; line-height: 1.4; color: var(--dim); margin-top: 26px; }
      #scene-result3 .model { font-size: 20px; line-height: 1.45; color: var(--ink); margin-top: 40px;
        padding-top: 18px; border-top: 1px solid rgba(127,136,150,.4); }
      #scene-result3 .limit { left: 100px; top: 956px; width: 1720px; font-size: 22px; color: var(--dim); white-space: nowrap; }
    `);
    const k = ctx.el('div', 'f-kicker', COPY.kicker, root); k.style.cssText = 'left:100px;top:56px';
    const t = ctx.el('div', 'f-title', c.title, root); t.style.cssText = 'left:100px;top:88px';
    const viz = ctx.el('div', 'viz', null, root);
    const svg = sv('svg', { viewBox: '0 0 448 280' }, viz);
    this.viz = VIZ[COPY.pick](sv('g', {}, svg), c, d, ctx);
    const col = ctx.el('div', 'col', null, root);
    this.heroLabel = ctx.el('div', 'f-small', c.heroLabel, col);
    this.hero = ctx.el('div', 'f-num hero', c.hero, col);
    this.unit = ctx.el('div', 'unit', c.unit, col);
    this.cmp = ctx.el('div', 'cmp', c.compare, col);
    this.model = ctx.el('div', 'model', c.model, col);
    this.limit = ctx.el('div', 'limit', c.limit, root);
  },
  update(p, t, ctx) {
    if (this.inf) return this.inf(p);
    this.viz(ctx.lin(p, 0.03, 0.62));                 // the picture builds first (linear: agents work at a constant pace)
    const hero = ctx.seg(p, 0.62, 0.67);
    this.heroLabel.style.opacity = hero;
    this.hero.style.opacity = hero;
    this.hero.style.transform = `translateY(${(1 - ctx.out(ctx.lin(p, 0.62, 0.67))) * 14}px)`;
    this.unit.style.opacity = ctx.seg(p, 0.66, 0.71);
    this.cmp.style.opacity = ctx.seg(p, 0.73, 0.78);
    this.model.style.opacity = ctx.seg(p, 0.81, 0.85);
    this.limit.style.opacity = ctx.seg(p, 0.87, 0.91);
  },
});
})();
