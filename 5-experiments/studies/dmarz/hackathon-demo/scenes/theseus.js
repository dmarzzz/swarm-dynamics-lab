// Scene: theseus. Result 2. A crew whose members are replaced one by one: does the job survive, and what carries it?
// Data: scenes/theseus.data.js (reduced from vishesh's pilot, attempt S1-a1).
(function () {
  const COPY = {
    kicker: 'result 3',
    title: 'Swarm of Theseus',
    // design facts: 5-experiments/studies/vishesh/swarm-of-theseus/RESULTS.md ("The comparison"): 3 members per world, replaced one at
    // a time at steps 1-3, followed through steps 4-5; 3 scenarios x 2 worlds x 6 conditions = 36 runs; model claude-haiku-4-5-20251001.
    // 864 calls: results/S1-a1/summary.json cost.calls.
    founder: 'founder',
    newcomer: ['new-1', 'new-2', 'new-3'],
    left: (n) => n + ' of 3 founders left',
    handed: 'newcomers inherit notes, mentoring, both, or neither',
    // chart
    yTitle: 'crew accuracy by step',
    stepWord: 'step',
    band: 'scored: steps 4-5',
    guess: 'guessing',
    // RESULTS.md table, column "Equal-scenario mean": notes 100.00, both 100.00, mentoring 91.67, retained founders 89.58, neither 52.08
    lines: {
      notes: 'notes handed down 100%',
      neither: 'nothing handed down 52%',
    },
    // takeaway
    hero: '100%',
    heroLabel: 'with notes handed down',
    vs: '52%',
    vsLabel: 'with nothing handed down (guessing = 50%)',
    claim: 'A written note carried the job across a full turnover. Without it, the new crew guessed.',
    // limit: RESULTS.md intro + redesign/REVIEW.md ("supplied-procedure transmission baseline"), experiments/evidence-metadata.json rationale
    limit: 'Tested supplied procedures, not safety constraints. 36 runs, 6 synthetic worlds, one model.',
    footer: 'swarm-of-theseus / vishesh / Claude Haiku 4.5, 36 runs',
  };

  // Beats, as fractions of the scene.
  const SWAP = [[0.035, 0.085], [0.085, 0.135], [0.135, 0.185]];   // A: the three replacements
  const AXES = [0.06, 0.20];                                       // chart frame is built while the crew turns over
  const DRAW = [0.26, 0.56];                                       // B: the lines advance step 0 -> 5
  const LABELS = [0.56, 0.63];
  const HERO = [0.65, 0.73];                                       // C
  const CLAIM = [0.74, 0.80];
  const LIMIT = [0.82, 0.88];

  const NS = 'http://www.w3.org/2000/svg';
  function svg(tag, attrs, parent, text) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }

  // chart geometry
  const X = (s) => 900 + s * 150;
  const Y = (v) => 780 - v * 5.0;
  const SLOT_X = [200, 400, 600], SLOT_Y = 300, R = 44;
  const ARMS = [
    { key: 'neither', color: 'var(--no)', w: 5 },
    { key: 'notes', color: 'var(--zip)', w: 5 },
  ];

  const R_ = {};

  FILM.scene({
    id: 'theseus',
    mount(root, ctx) {
      const D = FILM.data['theseus'];
      ctx.css(`
        #scene-theseus .abs { position:absolute; white-space:nowrap; }
        #scene-theseus .t-kicker { left:100px; top:56px; }
        #scene-theseus .t-title { left:100px; top:88px; }
        #scene-theseus .t-left { left:100px; top:410px; font-size:30px; color:var(--ink); }
        #scene-theseus .t-slot { top:358px; width:160px; text-align:center; font-size:22px; color:var(--dim); }
        #scene-theseus .t-handed { left:100px; top:476px; width:640px; white-space:normal; font-size:24px; line-height:1.4; color:var(--dim); }
        #scene-theseus .t-hero { left:100px; top:455px; font-size:170px; color:var(--amber); }
        #scene-theseus .t-herolabel { left:104px; top:618px; font-size:28px; color:var(--ink); }
        #scene-theseus .t-vs { left:100px; top:690px; font-size:110px; color:var(--no); }
        #scene-theseus .t-vslabel { left:320px; top:708px; width:430px; white-space:normal; font-size:26px; line-height:1.35; color:var(--ink); }
        #scene-theseus .t-claim { left:100px; top:880px; font-size:30px; color:var(--ink); }
        #scene-theseus .t-limit { left:100px; top:930px; font-size:22px; color:var(--dim); }
        #scene-theseus .t-footer { left:100px; top:976px; font-size:20px; color:var(--dim); opacity:0.8; }
        #scene-theseus svg { position:absolute; left:0; top:0; }
        #scene-theseus svg text { font-family:var(--mono); }
      `);
      const add = (cls, html) => ctx.el('div', 'abs ' + cls, html, root);
      add('f-kicker t-kicker', COPY.kicker);
      add('f-title t-title', COPY.title);
      R_.left = add('t-left', '');
      R_.slotLabel = SLOT_X.map((x) => { const e = add('t-slot', COPY.founder); e.style.left = (x - 80) + 'px'; return e; });
      R_.handed = add('t-handed', COPY.handed);
      R_.hero = add('f-num t-hero', COPY.hero);
      R_.heroLabel = add('t-herolabel', COPY.heroLabel);
      R_.vs = add('f-num t-vs', COPY.vs);
      R_.vsLabel = add('t-vslabel', COPY.vsLabel);
      R_.claim = add('t-claim', COPY.claim);
      R_.limit = add('t-limit', COPY.limit);
      add('t-footer', COPY.footer);

      const s = svg('svg', { width: 1920, height: 1080, viewBox: '0 0 1920 1080' }, root);
      R_.svg = s;

      // crew: three slots. Founder dot, replacement dot and the note that travels between them.
      R_.crew = SLOT_X.map((x) => {
        svg('circle', { cx: x, cy: SLOT_Y, r: R + 8, fill: 'none', stroke: 'var(--dim)', 'stroke-width': 1, opacity: 0.35 }, s);
        const old = svg('circle', { cx: x, cy: SLOT_Y, r: R, fill: 'var(--bone)' }, s);
        const neu = svg('circle', { cx: x, cy: SLOT_Y, r: R, fill: 'var(--zip)', opacity: 0 }, s);
        const note = svg('g', { opacity: 0 }, s);
        svg('rect', { x: -15, y: -19, width: 30, height: 38, fill: 'var(--void)', stroke: 'var(--amber)', 'stroke-width': 2.5 }, note);
        for (let i = 0; i < 3; i++) svg('line', { x1: -8, x2: 8, y1: -9 + i * 9, y2: -9 + i * 9, stroke: 'var(--amber)', 'stroke-width': 2 }, note);
        return { x, old, neu, note };
      });

      // chart frame
      const g = svg('g', {}, s); R_.frame = g;
      R_.band = svg('rect', { x: X(3.55), y: Y(100) - 52, width: X(5.35) - X(3.55), height: Y(0) - Y(100) + 52, fill: 'var(--ink)', opacity: 0 }, s);
      R_.bandLabel = svg('text', { x: X(4.45), y: Y(0) - 14, 'text-anchor': 'middle', 'font-size': 22, fill: 'var(--dim)', opacity: 0 }, s, COPY.band);
      svg('text', { x: 852, y: 206, 'font-size': 24, fill: 'var(--dim)' }, g, COPY.yTitle);
      R_.yAxis = svg('line', { x1: 868, x2: 868, y1: Y(0), y2: Y(100), stroke: 'var(--dim)', 'stroke-width': 1.5 }, g);
      R_.xAxis = svg('line', { x1: 868, x2: X(5) + 24, y1: Y(0), y2: Y(0), stroke: 'var(--dim)', 'stroke-width': 1.5 }, g);
      [0, 50, 100].forEach((v) => {
        svg('text', { x: 856, y: Y(v) + 8, 'text-anchor': 'end', 'font-size': 22, fill: 'var(--dim)' }, g, v + '%');
      });
      svg('line', { x1: 868, x2: X(5) + 24, y1: Y(50), y2: Y(50), stroke: 'var(--dim)', 'stroke-width': 1, 'stroke-dasharray': '3 9', opacity: 0.7 }, g);
      svg('text', { x: X(0) - 20, y: Y(50) + 30, 'font-size': 22, fill: 'var(--dim)' }, g, COPY.guess);
      R_.ticks = D.steps.map((st, i) => {
        const tg = svg('g', {}, g);
        svg('text', { x: X(st), y: Y(0) + 34, 'text-anchor': 'middle', 'font-size': 22, fill: 'var(--dim)' }, tg, COPY.stepWord + ' ' + st);
        for (let k = 0; k < 3; k++) {
          const isFounder = k >= 3 - D.founders[i];       // slots are replaced left to right
          svg('circle', { cx: X(st) + (k - 1) * 20, cy: Y(0) + 62, r: 7, fill: isFounder ? 'var(--bone)' : 'var(--zip)' }, tg);
        }
        return tg;
      });

      // mean lines, drawn with a moving clip
      const defs = svg('defs', {}, s);
      const clip = svg('clipPath', { id: 'theseus-clip' }, defs);
      R_.clip = svg('rect', { x: 860, y: 180, width: 0, height: 640 }, clip);
      const lg = svg('g', { 'clip-path': 'url(#theseus-clip)' }, s);
      R_.lines = ARMS.map((arm) => {
        const pts = D.mean[arm.key].map((v, i) => X(i) + ',' + Y(v)).join(' ');
        const attrs = { points: pts, fill: 'none', stroke: arm.color, 'stroke-width': arm.w, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' };
        if (arm.dash) attrs['stroke-dasharray'] = arm.dash;
        svg('polyline', attrs, lg);
        // direct labels sit inside the plot, right-aligned to the scored band: notes above its line, nothing below its line
        const m = D.mean[arm.key];
        const ly = arm.key === 'notes' ? Y(Math.max(m[4], m[5])) - 18 : Y(Math.min(m[3], m[4], m[5])) + 52;
        const label = svg('text', { x: X(5.35) - 12, y: ly, 'text-anchor': 'end', 'font-size': 26, fill: arm.color, opacity: 0 }, s, COPY.lines[arm.key]);
        return { arm, label };
      });
    },

    update(p, t, ctx) {
      // A. the crew turns over, one slot at a time; the note passes from the leaver to the newcomer.
      let founders = 3;
      R_.crew.forEach((c, i) => {
        const u = ctx.lin(p, SWAP[i][0], SWAP[i][1]);
        const leave = ctx.ease(ctx.clamp(u / 0.55));
        const arrive = ctx.out(ctx.clamp((u - 0.35) / 0.65));
        c.old.setAttribute('cy', SLOT_Y + 0 * leave);
        c.old.setAttribute('cx', c.x);
        c.old.setAttribute('r', ctx.lerp(R, 14, leave));
        c.old.setAttribute('transform', 'translate(' + (-86 * leave) + ',' + (26 * leave) + ')');
        c.old.setAttribute('opacity', ctx.lerp(1, 0.22, leave));
        c.neu.setAttribute('cy', ctx.lerp(SLOT_Y - 90, SLOT_Y, arrive));
        c.neu.setAttribute('opacity', arrive);
        // note: appears on the leaver, travels up to the newcomer, settles beside it
        const n = ctx.ease(ctx.clamp((u - 0.2) / 0.6));
        const nx = ctx.lerp(c.x - 86, c.x + 64, n), ny = ctx.lerp(SLOT_Y + 26, SLOT_Y - 36, n);
        c.note.setAttribute('transform', 'translate(' + nx + ',' + ny + ') scale(' + ctx.lerp(1.2, 0.9, n) + ')');
        c.note.setAttribute('opacity', u <= 0 ? 0 : ctx.clamp(u / 0.15) * ctx.lerp(1, 0.55, ctx.clamp((u - 0.85) / 0.15)));
        R_.slotLabel[i].textContent = u > 0.5 ? COPY.newcomer[i] : COPY.founder;
        R_.slotLabel[i].style.color = u > 0.5 ? 'var(--zip)' : 'var(--dim)';
        if (u > 0.5) founders--;
      });
      R_.left.textContent = COPY.left(founders);

      // the one-line label arrives with the first swap and steps back for the takeaway
      const toHero = ctx.seg(p, HERO[0] - 0.03, HERO[0]);
      R_.handed.style.opacity = ctx.seg(p, 0.03, 0.07) * (1 - toHero);
      const calm = ctx.seg(p, 0.22, 0.27);
      R_.crew.forEach((c) => { c.note.style.filter = calm > 0.5 ? 'grayscale(1)' : 'none'; });

      // chart frame builds during A
      const ax = ctx.seg(p, AXES[0], AXES[1]);
      R_.frame.setAttribute('opacity', ax);
      R_.yAxis.setAttribute('y2', ctx.lerp(Y(0), Y(100), ax));
      R_.xAxis.setAttribute('x2', ctx.lerp(868, X(5) + 24, ax));
      R_.ticks.forEach((tg, i) => tg.setAttribute('opacity', ctx.seg(p, AXES[0] + 0.015 * i, AXES[0] + 0.04 + 0.015 * i)));

      // B. lines advance one step at a time
      const r = ctx.lin(p, DRAW[0], DRAW[1]) * 5;                    // 0..5, current step position
      const started = ctx.seg(p, DRAW[0] - 0.02, DRAW[0]);
      R_.clip.setAttribute('width', started ? (X(r) - 860 + 6) : 0);
      const band = ctx.seg(p, 0.44, 0.50);
      R_.band.setAttribute('opacity', 0.06 * band);
      R_.bandLabel.setAttribute('opacity', band);
      R_.lines.forEach((l, i) => l.label.setAttribute('opacity', ctx.seg(p, LABELS[0] + 0.012 * i, LABELS[1] + 0.012 * i)));

      // C. takeaway
      const hero = ctx.seg(p, HERO[0], HERO[1]);
      R_.hero.style.opacity = hero;
      R_.heroLabel.style.opacity = ctx.seg(p, HERO[0] + 0.02, HERO[1] + 0.02);
      const vs = ctx.seg(p, HERO[0] + 0.04, HERO[1] + 0.04);
      R_.vs.style.opacity = vs; R_.vsLabel.style.opacity = vs;
      R_.claim.style.opacity = ctx.seg(p, CLAIM[0], CLAIM[1]);
      R_.limit.style.opacity = ctx.seg(p, LIMIT[0], LIMIT[1]);
    },
  });
})();
