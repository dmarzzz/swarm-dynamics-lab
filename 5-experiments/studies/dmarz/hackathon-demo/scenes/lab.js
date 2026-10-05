// lab: the autonomous research lab as one diagram, built left to right.
// Data comes from scenes/lab.data.js (regenerate with: python3 scenes/lab.build.py).
(() => {
  const COPY = {
    kicker: 'how we worked',
    title: 'An open source, mostly-autonomous swarm research lab',
    // every count below is read from FILM.data.lab; the comment names the file that proves it
    sourcesUnit: 'sources',                       // library/<type>/*.md, one file per source (3,319); one dot = 5 sources
    sourcesLine: ['papers, X threads, code,', 'blogs, talks, datasets'],
    hypUnit: 'hypotheses',                        // 5-experiments/studies/dmarz/question-atlas/candidates.json (219 candidates)
    areasLine: n => n + ' research areas',        // same file, topics (15)
    expUnit: 'experiments',                       // hub-snapshot.json, experiments registered at the hub (103)
    srvUnit: 'servers',                           // fleet.yml + claims/*.yml across swarm-labs-agentops copies (25)
    runUnit: 'runs in 16 hours',                  // hub-snapshot.json, Oct 3 20:24 to Oct 4 12:20 PT (1,584); one dot = one run
    railNote: 'every step gated in CI',
    gates: ['scan', 'survey', 'hypothesis', 'plan', 'run', 'post-mortem'],   // AGENTS.md, "The work runs in phases, and the order is enforced"
  };

  const TYPE_COL = { papers: '#cfc8b8', threads: '#8d97c2', code: '#a98fc0', blogs: '#bf9c82', talks: '#a9a67f', datasets: '#77909a' };
  const X1 = 100, X2 = 452, X3 = 812, XR = 1820, YD = 334;        // column lefts, right edge, diagram top
  const GATE_X = [100, 330, 540, 900, 1240, 1530];
  const B = { lit0: 0.04, lit1: 0.21, hyp0: 0.23, hyp1: 0.38, srv0: 0.40, srv1: 0.48, run0: 0.48, run1: 0.87, hold: 0.90 };

  FILM.scene({
    id: 'lab',
    mount(root, ctx) {
      const D = (FILM.data || {}).lab; this.D = D;
      if (!D) { ctx.el('div', 'f-body', 'lab.data.js missing', root); return; }
      ctx.css(`
        #scene-lab .abs { position: absolute; white-space: nowrap; }
        #scene-lab canvas { position: absolute; left: 0; top: 0; }
        #scene-lab .num { font-size: 92px; color: var(--ink); }
        #scene-lab .unit { font-size: 24px; }
        #scene-lab .note { font-size: 20px; line-height: 28px; color: var(--dim); }
        #scene-lab .gate { font-size: 32px; color: var(--dim); }
      `);
      const cs = getComputedStyle(root);
      const v = n => cs.getPropertyValue(n).trim() || '#888';
      this.C = { ink: v('--ink'), dim: v('--dim'), amber: v('--amber'), zip: v('--zip'), no: v('--no') };
      const cv = ctx.el('canvas', '', null, root); cv.width = 1920; cv.height = 1080; this.g = cv.getContext('2d');
      const A = (cls, html, x, y) => { const e = ctx.el('div', 'abs ' + cls, html, root); e.style.left = x + 'px'; e.style.top = y + 'px'; return e; };
      A('f-kicker', COPY.kicker, 100, 56); A('f-title', COPY.title, 100, 92).style.fontSize = '50px';   // the long title fits at 50px

      // hero numbers, one short label each
      const F = D.fleet, U = (txt, x) => A('f-small unit', txt, x, 276);
      this.nums = [
        { el: A('f-num num', '0', X1, 178), n: D.libTotal, a: B.lit0, b: B.lit1, unit: U(COPY.sourcesUnit, X1) },
        { el: A('f-num num', '0', X2, 178), n: D.hyp.total, a: B.hyp0, b: B.hyp1, unit: U(COPY.hypUnit, X2) },
        { el: A('f-num num', '0', X3, 178), n: F.nExperiments, a: B.srv0, b: B.srv1, unit: U(COPY.expUnit, X3) },
        { el: A('f-num num', '0', 1100, 178), n: F.nServers, a: B.srv0, b: B.srv1, unit: U(COPY.srvUnit, 1100) },
        { el: A('f-num num', '0', 1400, 178), n: F.nRuns, a: B.run0, b: B.run1, unit: U(COPY.runUnit, 1400), runs: true },
      ];

      // 1. literature: waffle, one dot per 5 sources, grouped by type
      const rnd = ctx.rng(7); this.lit = []; const COLS = 21, SP = 14; let k = 0;
      D.lib.forEach((t, ti) => { const n = Math.ceil(t.n / 5);
        for (let i = 0; i < n; i++, k++) this.lit.push({ x: X1 + 5 + (k % COLS) * SP, y: YD + 8 + Math.floor(k / COLS) * SP, c: TYPE_COL[t.type],
          sx: X1 + rnd() * 300, sy: YD + rnd() * 540, j: rnd(), ti }); });
      this.lit.forEach((d, i) => { d.a = i / this.lit.length; });
      const ly = YD + 8 + Math.ceil(k / COLS) * SP + 8;

      // 2. hypotheses: one cluster of dots per area, one dot per hypothesis
      this.hyp = []; let hk = 0, hy = YD + 8; const HC = 26, HS = 12.5, HG = 17;
      D.hyp.areas.slice().sort((a, b) => b.n - a.n).forEach((a, r) => {
        for (let i = 0; i < a.n; i++, hk++) this.hyp.push({ x: X2 + 5 + (i % HC) * HS, y: hy + Math.floor(i / HC) * HS, r, t: i < a.tested, k: hk });
        hy += Math.ceil(a.n / HC) * HS + HG; });
      const noteY = Math.max(ly, hy - HG + 4);
      this.litNote = A('note', COPY.sourcesLine.join('<br>'), X1, noteY);
      this.hypNote = A('note', COPY.areasLine(D.hyp.nAreas), X2, noteY);

      // 3. fleet: hub first, then servers by run count, then runs with no claim (dashed node, last cell)
      const srv = F.servers.slice().sort((a, b) => (b.name === 'hub-01') - (a.name === 'hub-01') || b.t.length - a.t.length);
      srv.push({ name: null, t: F.unclaimed.t, s: F.unclaimed.s });
      const GC = 7, GR = Math.max(4, Math.ceil(srv.length / GC)), CW = (XR - X3) / GC, CH = 548 / GR;
      const maxN = Math.max(1, ...srv.map(s => s.t.length)), K = Math.min(3, (Math.min(CW, CH) / 2 - 18) / Math.sqrt(maxN));
      this.srv = srv.map((s, i) => { if (!s.name) i = GC * GR - 1; const cx = X3 + CW * (i % GC + 0.5), cy = YD + 4 + (Math.floor(i / GC) + 0.5) * CH;
        const dots = s.t.map((t, j) => { const r = 9 + K * Math.sqrt(j + 0.5), a = j * 2.39996 + i; return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a), t: t / 1000, s: s.s[j] }; });
        return { cx, cy, dots, hub: s.name === 'hub-01', none: !s.name, first: dots.length ? dots[0].t : 2, i }; });

      // 4. process rail
      this.railNote = A('f-small', COPY.railNote, 100, 892);
      this.gates = COPY.gates.map((gt, i) => ({ x: GATE_X[i], a: A('gate', gt, GATE_X[i], 940) }));
    },

    update(p, t, ctx) {
      const D = this.D; if (!D) return; const g = this.g, C = this.C, F = D.fleet;
      g.clearRect(0, 0, 1920, 1080);
      const stage = p < B.lit0 ? -1 : p < B.hyp0 ? 0 : p < B.srv0 ? 1 : p < B.run0 ? 2 : 3;   // which stage is being built
      const dot = (x, y, r, col, al) => { g.globalAlpha = al; g.fillStyle = col; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.fill(); };

      // hero numbers: count up while their stage builds; the active one is amber
      const active = [0, 1, 3, 3, 4], stg = [0, 1, 2, 2, 3];
      this.nums.forEach((n, i) => { const k = ctx.lin(p, n.a, n.b);
        n.el.textContent = ctx.fmt(Math.round(n.n * (n.runs ? this._runFrac(p) : ctx.out(k))));
        const on = (stage === stg[i] && (i !== 2)) || (i === 4 && p >= B.run0);
        n.el.style.color = on ? 'var(--amber)' : 'var(--ink)';
        const vis = ctx.seg(p, n.a - 0.02, n.a + 0.01); n.el.style.opacity = vis; n.unit.style.opacity = vis; });
      const rk = ctx.lin(p, B.run0, B.run1);   // replay position through the 16 hours

      // 1. literature dots stream into the catalogue
      const litK = ctx.lin(p, B.lit0, B.lit1);
      for (const d of this.lit) { const k = ctx.out(ctx.clamp((litK - d.a * 0.8) / 0.2)); if (k <= 0) continue;
        dot(ctx.lerp(d.sx, d.x, k), ctx.lerp(d.sy, d.y, k), 4.2, d.c, 0.15 + 0.85 * k); }
      this.litNote.style.opacity = ctx.seg(p, B.lit1 - 0.04, B.lit1);

      // 2. hypotheses, row by row
      const hypK = ctx.lin(p, B.hyp0, B.hyp1), HN = this.hyp.length, showTested = p >= B.run1 - 0.02;
      for (const d of this.hyp) { const k = ctx.clamp((hypK * (HN + 12) - d.k) / 12); if (k <= 0) continue;
        const fresh = stage === 1 && k < 1;
        dot(d.x, d.y, 3.8, fresh ? C.amber : (d.t && showTested ? C.zip : C.ink), (d.t && showTested) || fresh ? 1 : 0.72 * k); }
      this.hypNote.style.opacity = ctx.seg(p, B.hyp1 - 0.04, B.hyp1);

      // 3. fleet: servers arrive, then the night replays
      for (const s of this.srv) { const k = ctx.seg(p, B.srv0 + 0.0026 * s.i, B.srv0 + 0.0026 * s.i + 0.025);
        const lit = rk >= s.first && s.dots.length;
        if (k <= 0) continue;
        g.globalAlpha = k; g.lineWidth = 1.5; g.strokeStyle = (stage === 2 && k < 1) ? C.amber : s.none ? C.dim : lit ? C.ink : C.dim;
        if (s.hub) { g.beginPath(); g.arc(s.cx, s.cy, 11, 0, 6.2832); g.stroke(); g.beginPath(); g.arc(s.cx, s.cy, 4, 0, 6.2832); g.stroke(); }
        else if (s.none) { g.setLineDash([2, 3]); g.strokeRect(s.cx - 4.5, s.cy - 4.5, 9, 9); g.setLineDash([]); }
        else g.strokeRect(s.cx - 4.5, s.cy - 4.5, 9, 9);
        for (const d of s.dots) { const age = rk - d.t; if (age < 0 || p < B.run0) continue;
          const fresh = age < 0.008 && p < B.run1;
          const col = fresh ? C.amber : d.s === 'd' ? C.zip : d.s === 'f' ? C.no : d.s === 'r' ? C.ink : C.dim;
          dot(d.x, d.y, fresh ? 2.6 : 1.9, col, fresh ? 1 : d.s === 'd' ? 0.85 : 0.9); } }

      // 4. rail: a thin line that fills as stages complete; the gate being passed is amber
      const prog = [B.lit0, B.lit1 - 0.03, B.hyp0, B.srv0, B.run0, B.run1];     // when each gate is reached
      const railK = ctx.seg(p, 0.03, 0.08);
      g.globalAlpha = railK * 0.5; g.strokeStyle = C.dim; g.lineWidth = 1; g.beginPath(); g.moveTo(100, 926.5); g.lineTo(100 + (XR - 100) * railK, 926.5); g.stroke();
      let cur = -1; prog.forEach((a, i) => { if (p >= a) cur = i; });
      const head = cur < 0 ? 100 : cur >= 5 ? ctx.lerp(GATE_X[5], XR, ctx.seg(p, B.run1, B.hold)) : ctx.lerp(GATE_X[cur], GATE_X[cur + 1], ctx.lin(p, prog[cur], prog[cur + 1]));
      g.globalAlpha = 1; g.strokeStyle = C.ink; g.lineWidth = 2; g.beginPath(); g.moveTo(100, 926.5); g.lineTo(head, 926.5); g.stroke();
      this.gates.forEach((gt, i) => { const reached = p >= prog[i], isCur = i === cur && p < B.hold;
        const o = ctx.seg(p, 0.04 + i * 0.008, 0.07 + i * 0.008); gt.a.style.opacity = o;
        gt.a.style.color = isCur && i < 4 ? 'var(--ink)' : reached ? 'var(--ink)' : 'var(--dim)';
        g.globalAlpha = o; g.fillStyle = reached ? C.ink : C.dim; g.fillRect(gt.x, 921, 3, 12); });
      this.railNote.style.opacity = ctx.seg(p, 0.05, 0.09);
      g.globalAlpha = 1;
    },

    // fraction of runs created by replay position (so the counter matches the dots on screen)
    _runFrac(p) {
      if (!this._ts) { this._ts = []; for (const s of this.srv) for (const d of s.dots) this._ts.push(d.t); this._ts.sort((a, b) => a - b); }
      if (p < B.run0) return 0; if (p >= B.run1) return 1;
      const rk = (p - B.run0) / (B.run1 - B.run0), ts = this._ts; let lo = 0, hi = ts.length;
      while (lo < hi) { const m = (lo + hi) >> 1; if (ts[m] <= rk) lo = m + 1; else hi = m; }
      return lo / ts.length;
    },
  });
})();
