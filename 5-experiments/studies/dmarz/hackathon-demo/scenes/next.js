// Scene: next (closing). Three next steps arriving one at a time, then the end card.
(function () {
  const COPY = {
    kicker: 'What comes next',
    title: 'Next steps',

    step1: {
      label: 'Mine our own traces to make the lab more autonomous',
      logs: 'traces + logs',
      loop: 'lab',
      out: 'writes',
      back: 'reads',
    },

    step2: {
      label: 'Finish the research program',
      // tested = 12, total = 219. Proof: swarm-labs-agentops site/public/hypotheses.json ("total": 219, "tested": 12),
      // written by site/scripts/hypotheses.py from 5-experiments/studies/dmarz/question-atlas/candidates.json
      // ("candidates": 219). "Tested" there means: the candidate id is cited by a hub experiment.
      // The script's 214 / 215 is the older atlas count (synthesis/research-question-atlas.md line 5 still says 214).
      tested: 12,
      total: 219,
      unit: 'candidates cited by an experiment so far',
      // Position in the atlas (0-based, candidates.json order) of each tested candidate:
      // PHY-09 SOC-02 SOC-07 SOC-08 SOC-24 SEC-19 SEC-43 SEC-47 SEC-52 SEC-54 MKT-03 MKT-11 (hypotheses.json "tested": true).
      // If this list does not have exactly `tested` entries, the first `tested` squares are filled instead.
      testedAt: [8, 39, 44, 45, 61, 101, 125, 129, 134, 136, 207, 215],
    },

    step3: {
      label: 'Scale from ~200 agents to 2,000, enough to recreate the Hugging Face scenario',
      // now = 200. Largest swarm actually run: 5-experiments/studies/vishesh/regrowth-200/README.md
      // ("200 cell identities, 80 rounds", 6 of 6 worlds; exploratory, one map). Largest with a full-size API model:
      // 5-experiments/studies/dmarz/sybil-rules-180/RESULTS.md (180 gpt-6-sol owners, two economies).
      // NOT reached: 5-experiments/studies/dmarz/growth-pressure-200/RESULTS.md stopped at qualification, no 200-agent run.
      now: 200,
      nowLabel: '~200 agents',
      nowNote: 'largest run',
      // target = 2000 is a plan, not a result (the script's own number).
      target: 2000,
      targetUnit: 'agents',
      targetNote: 'the incident: about 1,200',   // METR's count for the Hugging Face incident (INTRO-FACTS.md)
    },

    card: {
      team: 'Swarm of Theseus',
      repoLabel: 'site',
      repo: 'swarmsafety.org',
      liveLabel: 'code + data',
      live: 'github.com/dmarzzz/swarm-dynamics-lab',
      qrNote: 'scan for the repo',
      open: 'The entire lab is open source, from the prompts to the infrastructure as code.',
    },
  };

  // QR for https://github.com/dmarzzz/swarm-dynamics-lab (33x33 modules, segno, error level M), regenerated after the repo rename. Earlier markup came from
  // 5-experiments/studies/dmarz/discussion-dose/src/film_v3/qr-repo.svg; decoded with cv2.QRCodeDetector on 2026-10-04,
  // it reads exactly "https://github.com/dmarzzz/swarm-dynamics-lab". If COPY.card.repo changes, replace this path or remove the QR.
  const QR_PATH = 'M0 0.5h7M8 0.5h1M10 0.5h1M12 0.5h3M16 0.5h1M18 0.5h4M23 0.5h1M26 0.5h7M0 1.5h1M6 1.5h1M10 1.5h1M13 1.5h1M15 1.5h4M20 1.5h2M26 1.5h1M32 1.5h1M0 2.5h1M2 2.5h3M6 2.5h1M11 2.5h2M14 2.5h2M18 2.5h1M20 2.5h3M26 2.5h1M28 2.5h3M32 2.5h1M0 3.5h1M2 3.5h3M6 3.5h1M10 3.5h1M12 3.5h3M16 3.5h1M18 3.5h2M22 3.5h1M24 3.5h1M26 3.5h1M28 3.5h3M32 3.5h1M0 4.5h1M2 4.5h3M6 4.5h1M8 4.5h3M12 4.5h1M15 4.5h1M18 4.5h4M23 4.5h1M26 4.5h1M28 4.5h3M32 4.5h1M0 5.5h1M6 5.5h1M8 5.5h2M11 5.5h1M13 5.5h2M18 5.5h1M20 5.5h1M24 5.5h1M26 5.5h1M32 5.5h1M0 6.5h7M8 6.5h1M10 6.5h1M12 6.5h1M14 6.5h1M16 6.5h1M18 6.5h1M20 6.5h1M22 6.5h1M24 6.5h1M26 6.5h7M11 7.5h1M13 7.5h4M21 7.5h1M23 7.5h1M1 8.5h7M9 8.5h1M12 8.5h2M17 8.5h1M23 8.5h1M27 8.5h2M32 8.5h1M4 9.5h2M7 9.5h4M14 9.5h3M19 9.5h2M23 9.5h1M26 9.5h2M29 9.5h4M0 10.5h2M6 10.5h2M10 10.5h1M12 10.5h1M15 10.5h2M18 10.5h1M21 10.5h2M24 10.5h1M28 10.5h1M30 10.5h2M0 11.5h1M2 11.5h4M7 11.5h3M11 11.5h1M15 11.5h2M18 11.5h1M20 11.5h3M24 11.5h1M26 11.5h1M28 11.5h3M32 11.5h1M2 12.5h6M10 12.5h1M12 12.5h4M18 12.5h1M22 12.5h4M28 12.5h2M32 12.5h1M2 13.5h1M4 13.5h2M7 13.5h10M18 13.5h3M23 13.5h1M26 13.5h1M31 13.5h2M0 14.5h3M5 14.5h2M9 14.5h1M12 14.5h1M16 14.5h1M22 14.5h1M25 14.5h2M31 14.5h1M3 15.5h1M8 15.5h5M15 15.5h1M18 15.5h1M20 15.5h2M24 15.5h4M30 15.5h1M1 16.5h1M3 16.5h1M5 16.5h2M8 16.5h2M11 16.5h1M14 16.5h1M16 16.5h4M22 16.5h4M27 16.5h2M32 16.5h1M2 17.5h1M4 17.5h1M9 17.5h2M13 17.5h2M16 17.5h1M19 17.5h2M23 17.5h1M26 17.5h2M29 17.5h4M0 18.5h1M2 18.5h3M6 18.5h2M11 18.5h5M17 18.5h1M20 18.5h2M24 18.5h5M30 18.5h2M0 19.5h1M4 19.5h1M8 19.5h1M10 19.5h1M12 19.5h4M19 19.5h4M25 19.5h1M27 19.5h4M32 19.5h1M2 20.5h1M4 20.5h1M6 20.5h2M9 20.5h3M15 20.5h2M19 20.5h1M22 20.5h1M27 20.5h3M32 20.5h1M0 21.5h2M8 21.5h2M11 21.5h2M14 21.5h1M16 21.5h1M19 21.5h3M23 21.5h1M26 21.5h1M29 21.5h1M32 21.5h1M0 22.5h1M5 22.5h3M9 22.5h1M11 22.5h1M14 22.5h3M18 22.5h1M20 22.5h1M24 22.5h2M28 22.5h2M31 22.5h1M0 23.5h1M3 23.5h1M5 23.5h1M7 23.5h1M9 23.5h5M15 23.5h1M18 23.5h1M20 23.5h3M25 23.5h2M29 23.5h3M0 24.5h1M4 24.5h1M6 24.5h2M9 24.5h3M13 24.5h1M16 24.5h4M22 24.5h1M24 24.5h6M31 24.5h2M8 25.5h2M11 25.5h2M14 25.5h4M19 25.5h1M21 25.5h1M23 25.5h2M28 25.5h1M30 25.5h3M0 26.5h7M8 26.5h4M13 26.5h1M15 26.5h1M17 26.5h2M20 26.5h1M23 26.5h2M26 26.5h1M28 26.5h1M30 26.5h2M0 27.5h1M6 27.5h1M8 27.5h4M13 27.5h1M16 27.5h1M18 27.5h1M20 27.5h5M28 27.5h3M32 27.5h1M0 28.5h1M2 28.5h3M6 28.5h1M8 28.5h1M11 28.5h1M14 28.5h1M19 28.5h1M22 28.5h1M24 28.5h6M0 29.5h1M2 29.5h3M6 29.5h1M8 29.5h3M12 29.5h2M15 29.5h1M19 29.5h1M22 29.5h4M28 29.5h1M30 29.5h1M32 29.5h1M0 30.5h1M2 30.5h3M6 30.5h1M8 30.5h1M11 30.5h1M14 30.5h1M16 30.5h1M20 30.5h1M22 30.5h1M26 30.5h2M29 30.5h1M0 31.5h1M6 31.5h1M8 31.5h1M13 31.5h2M16 31.5h2M19 31.5h1M21 31.5h2M25 31.5h2M28 31.5h3M0 32.5h7M10 32.5h1M15 32.5h2M18 32.5h1M22 32.5h4M27 32.5h1M29 32.5h1M31 32.5h1';

  // Beats, as fractions of the scene. Steps fill the first 55%; the end card and its QR hold for the last 30%.
  const B = {
    s1: [0.03, 0.075], s1logs: [0.05, 0.105], s1loop: [0.075, 0.14],
    s2: [0.155, 0.195], s2grid: [0.17, 0.27], s2fill: [0.27, 0.335], s2count: [0.295, 0.345],
    s3: [0.36, 0.40], s3now: [0.375, 0.41], s3grow: [0.41, 0.50],
    out: [0.56, 0.61],
    cardName: [0.60, 0.68], cardRepo: [0.66, 0.71], cardLive: [0.70, 0.75], cardQr: [0.62, 0.70],
  };

  // Layout (stage pixels).
  const COL = { x1: 100, w1: 400, x2: 560, w2: 680, x3: 1300, w3: 520 };
  const TOP = { idx: 216, label: 250, gfx: 400 };
  const GRID = { cols: 20, pitch: 34, size: 22 };
  const DOT = { r: 2, pitch: 7.2 };

  const SVGNS = 'http://www.w3.org/2000/svg';
  function svg(tag, attrs, parent) {
    const e = document.createElementNS(SVGNS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  let steps, heads = [], logBars = [], arcOut, arcBack, loopArc, loopHead, runner, loopText, tagOut, tagBack, tagLogs;
  let squares = [], testedSet, numEl, unitEl, canvas, g2d, dots = [], capNow, capTarget, targetNum, colors = {};
  let card, nameChars = [], cursor, repoRow, liveRow, qrBox, qrNote, openRow;
  const LOOP = { cx: 200, cy: 100, r: 74 };

  FILM.scene({
    id: 'next',
    mount(root, ctx) {
      ctx.css(`
        #scene-next .nx-kicker { position:absolute; left:100px; top:56px; }
        #scene-next .nx-title { position:absolute; left:100px; top:88px; }
        #scene-next .nx-steps { position:absolute; left:0; top:0; width:1920px; height:1080px; }
        #scene-next .nx-idx { position:absolute; top:${TOP.idx}px; }
        #scene-next .nx-label { position:absolute; top:${TOP.label}px; font-family:var(--mono); font-size:27px; line-height:1.36;
          color:var(--ink); }
        #scene-next .nx-gfx { position:absolute; top:${TOP.gfx}px; }
        #scene-next .nx-gfx svg { position:absolute; left:0; top:0; overflow:visible; }
        #scene-next .nx-tag { font-family:var(--mono); font-size:18px; letter-spacing:.12em; text-transform:uppercase; fill:var(--dim); }
        #scene-next .nx-looptext { font-family:var(--mono); font-size:26px; fill:var(--ink); }
        #scene-next .nx-sq { position:absolute; width:${GRID.size}px; height:${GRID.size}px; border:1px solid var(--dim); opacity:0; }
        #scene-next .nx-num { position:absolute; left:${COL.x2}px; top:800px; font-size:112px; color:var(--ink); opacity:0; }
        #scene-next .nx-num b { font-weight:inherit; color:var(--amber); }
        #scene-next .nx-unit { position:absolute; left:${COL.x2 + 4}px; top:928px; font-family:var(--mono); font-size:27px; color:var(--ink);
          white-space:nowrap; opacity:0; }
        #scene-next .nx-cap { position:absolute; font-family:var(--mono); font-size:26px; line-height:1.3; color:var(--ink);
          white-space:nowrap; opacity:0; }
        #scene-next .nx-cap .f-small { display:block; margin-top:6px; }
        #scene-next .nx-card { position:absolute; left:0; top:0; width:1920px; height:1080px; }
        #scene-next .nx-name { position:absolute; left:94px; top:150px; font-family:var(--display); font-size:164px; line-height:1;
          color:var(--ink); white-space:nowrap; letter-spacing:0; }
        #scene-next .nx-name span { opacity:0; }
        #scene-next .nx-cursor { position:absolute; top:168px; width:14px; height:128px; background:var(--amber); opacity:0; }
        #scene-next .nx-row { position:absolute; left:100px; opacity:0; white-space:nowrap; }
        #scene-next .nx-row .u { font-family:var(--mono); font-size:50px; line-height:1.2; color:var(--ink); margin-top:10px; }
        #scene-next .nx-qr { position:absolute; left:1364px; top:452px; width:456px; height:456px; background:var(--bone);
          padding:48px; opacity:0; }
        #scene-next .nx-qr svg { display:block; width:360px; height:360px; }
        #scene-next .nx-open { position:absolute; left:100px; top:372px; width:1200px; font-family:var(--mono); font-size:34px;
          line-height:1.35; color:var(--zip); opacity:0; }
        #scene-next .nx-qrnote { position:absolute; left:1364px; top:928px; opacity:0; }
      `);

      const cs = getComputedStyle(root);
      const tok = (n, fb) => (cs.getPropertyValue(n) || '').trim() || fb;
      colors = { zip: tok('--zip', '#5ad7e6'), ink: tok('--ink', '#e8eaee'), dim: tok('--dim', '#7f8896') };

      ctx.el('div', 'f-kicker nx-kicker', COPY.kicker, root);
      ctx.el('div', 'f-title nx-title', COPY.title, root);

      steps = ctx.el('div', 'nx-steps', '', root);
      const cols = [[COL.x1, COL.w1, COPY.step1.label], [COL.x2, COL.w2, COPY.step2.label], [COL.x3, COL.w3, COPY.step3.label]];
      heads = cols.map(([x, w, label], i) => {
        const idx = ctx.el('div', 'f-small nx-idx', '0' + (i + 1), steps);
        idx.style.left = x + 'px';
        const lab = ctx.el('div', 'nx-label', label, steps);
        lab.style.left = x + 'px';
        lab.style.width = w + 'px';
        return { idx, lab };
      });

      // Step 1: the lab loop writes traces and logs, and learns from them.
      const g1 = ctx.el('div', 'nx-gfx', '', steps);
      g1.style.left = COL.x1 + 'px';
      const s1 = svg('svg', { width: 400, height: 420, viewBox: '0 0 400 420' }, g1);
      const circ = 2 * Math.PI * LOOP.r;
      loopArc = svg('circle', { cx: LOOP.cx, cy: LOOP.cy, r: LOOP.r, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2,
        'stroke-dasharray': circ, 'stroke-dashoffset': circ, transform: `rotate(-90 ${LOOP.cx} ${LOOP.cy})` }, s1);
      loopHead = svg('path', { d: 'M-9 -7 L0 0 L-9 7', fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2 }, s1);
      loopText = svg('text', { x: LOOP.cx, y: LOOP.cy + 9, 'text-anchor': 'middle', class: 'nx-looptext' }, s1);
      loopText.textContent = COPY.step1.loop;
      runner = svg('circle', { r: 6, fill: 'var(--zip)' }, s1);
      // lab -> logs (left side, downwards) and logs -> lab (right side, upwards)
      arcOut = svg('path', { d: 'M150 158 C 110 200, 96 230, 96 268', fill: 'none', stroke: 'var(--dim)', 'stroke-width': 2 }, s1);
      svg('path', { d: 'M89 258 L96 270 L103 258', fill: 'none', stroke: 'var(--dim)', 'stroke-width': 2 }, s1).setAttribute('class', 'nx-ah-out');
      arcBack = svg('path', { d: 'M304 268 C 304 230, 290 200, 250 158', fill: 'none', stroke: 'var(--zip)', 'stroke-width': 2 }, s1);
      svg('path', { d: 'M263 162 L249 157 L253 171', fill: 'none', stroke: 'var(--zip)', 'stroke-width': 2 }, s1).setAttribute('class', 'nx-ah-back');
      tagOut = svg('text', { x: 84, y: 216, 'text-anchor': 'end', class: 'nx-tag' }, s1); tagOut.textContent = COPY.step1.out;
      tagBack = svg('text', { x: 316, y: 216, 'text-anchor': 'start', class: 'nx-tag' }, s1); tagBack.textContent = COPY.step1.back;
      const widths = [300, 236, 332, 188, 280];
      logBars = widths.map((w, i) => {
        const y = 286 + i * 22;
        const tick = svg('rect', { x: 34, y: y, width: 8, height: 8, fill: 'var(--dim)' }, s1);
        const bar = svg('rect', { x: 52, y: y + 2, width: w, height: 4, fill: 'var(--dim)' }, s1);
        return { tick, bar, w };
      });
      tagLogs = svg('text', { x: 34, y: 418, class: 'nx-tag' }, s1); tagLogs.textContent = COPY.step1.logs;
      [arcOut, arcBack].forEach((a) => { const L = a.getTotalLength(); a.dataset.len = L; a.setAttribute('stroke-dasharray', L); });

      // Step 2: one square per hypothesis.
      const g2 = ctx.el('div', 'nx-gfx', '', steps);
      g2.style.left = COL.x2 + 'px';
      const M = COPY.step2.total, N = COPY.step2.tested;
      const at = COPY.step2.testedAt;
      testedSet = new Set(at && at.length === N && at.every((i) => i < M) ? at : Array.from({ length: N }, (_, i) => i));
      squares = [];
      for (let i = 0; i < M; i++) {
        const q = ctx.el('div', 'nx-sq', '', g2);
        q.style.left = ((i % GRID.cols) * GRID.pitch) + 'px';
        q.style.top = (Math.floor(i / GRID.cols) * GRID.pitch) + 'px';
        squares.push(q);
      }
      numEl = ctx.el('div', 'f-num nx-num', '<b>' + ctx.fmt(N) + '</b> of ' + ctx.fmt(M), steps);
      unitEl = ctx.el('div', 'nx-unit', COPY.step2.unit, steps);

      // Step 3: every dot is one agent, same size in both clusters.
      const g3 = ctx.el('div', 'nx-gfx', '', steps);
      g3.style.left = COL.x3 + 'px';
      const CW = COL.w3, CH = 400;
      canvas = document.createElement('canvas');
      canvas.width = CW * 2; canvas.height = CH * 2;
      canvas.style.cssText = 'position:absolute;left:0;top:0;width:' + CW + 'px;height:' + CH + 'px;';
      g3.appendChild(canvas);
      g2d = canvas.getContext('2d');
      const c = DOT.pitch / Math.sqrt(Math.PI), GA = Math.PI * (3 - Math.sqrt(5));
      const rNow = c * Math.sqrt(COPY.step3.now) + DOT.r, rTar = c * Math.sqrt(COPY.step3.target) + DOT.r;
      const scale = Math.min(1, (CW - 36) / (2 * rNow + 2 * rTar)); // shrink pitch only if the copy asks for more dots than fit
      const cxNow = rNow * scale, cxTar = CW - rTar * scale, cy = Math.min(CH / 2, rTar * scale + 2);
      const rnd = ctx.rng(2000);
      dots = [];
      const cluster = (n, cx, kind) => {
        for (let i = 0; i < n; i++) {
          const r = c * Math.sqrt(i + 0.5) * scale, a = i * GA;
          dots.push({ x: cx + r * Math.cos(a), y: cy + r * Math.sin(a), kind, i, ph: rnd() * 6.283 });
        }
      };
      cluster(COPY.step3.now, cxNow, 0);
      cluster(COPY.step3.target, cxTar, 1);
      const capY = TOP.gfx + cy + rTar * scale + 22;
      capNow = ctx.el('div', 'nx-cap', COPY.step3.nowLabel + '<span class="f-small">' + COPY.step3.nowNote + '</span>', steps);
      capNow.style.left = COL.x3 + 'px'; capNow.style.top = capY + 'px';
      capTarget = ctx.el('div', 'nx-cap', '<span class="nx-tn"></span> ' + COPY.step3.targetUnit +
        '<span class="f-small">' + COPY.step3.targetNote + '</span>', steps);
      capTarget.style.left = (COL.x3 + Math.max(cxTar - 100, 250)) + 'px'; capTarget.style.top = capY + 'px';
      targetNum = capTarget.querySelector('.nx-tn');

      // End card.
      card = ctx.el('div', 'nx-card', '', root);
      const name = ctx.el('div', 'nx-name', '', card);
      nameChars = [];
      for (const ch of COPY.card.team) {
        const s = document.createElement('span');
        s.textContent = ch === ' ' ? ' ' : ch;
        name.appendChild(s);
        nameChars.push(s);
      }
      cursor = ctx.el('div', 'nx-cursor', '', card);
      repoRow = ctx.el('div', 'nx-row', '<div class="f-small">' + COPY.card.repoLabel + '</div><div class="u">' + COPY.card.repo + '</div>', card);
      openRow = ctx.el('div', 'nx-open', COPY.card.open, card);
      repoRow.style.top = '540px';
      liveRow = ctx.el('div', 'nx-row', '<div class="f-small">' + COPY.card.liveLabel + '</div><div class="u">' + COPY.card.live + '</div>', card);
      liveRow.style.top = '720px';
      qrBox = ctx.el('div', 'nx-qr', '<svg xmlns="' + SVGNS + '" viewBox="0 0 33 33" shape-rendering="crispEdges"><path stroke="#03050a" d="' +
        QR_PATH + '"/></svg>', card);
      qrNote = ctx.el('div', 'f-small nx-qrnote', COPY.card.qrNote, card);
    },

    update(p, t, ctx) {
      const out = ctx.seg(p, B.out[0], B.out[1]);
      steps.style.opacity = 1 - out;
      steps.style.transform = 'translateY(' + (-24 * out).toFixed(2) + 'px)';
      const titleKeep = 1 - out;
      steps.parentNode.querySelector('.nx-title').style.opacity = titleKeep;
      steps.parentNode.querySelector('.nx-kicker').style.opacity = titleKeep;

      // Step heads arrive one at a time.
      [B.s1, B.s2, B.s3].forEach((b, i) => {
        const a = ctx.seg(p, b[0], b[1]);
        heads[i].idx.style.opacity = a;
        heads[i].lab.style.opacity = a;
        heads[i].lab.style.transform = 'translateY(' + ((1 - a) * 14).toFixed(2) + 'px)';
      });

      // Step 1. The loop is drawn, the log lines are written, the feedback arrow closes the loop, a dot keeps circling.
      const k1 = ctx.seg(p, B.s1[0], B.s1logs[0] + 0.02);
      const circ = 2 * Math.PI * LOOP.r, arcFrac = 0.9;
      loopArc.setAttribute('stroke-dashoffset', (circ * (1 - arcFrac * k1)).toFixed(2));
      loopArc.setAttribute('stroke-dasharray', circ.toFixed(2));
      const ha = -Math.PI / 2 + 2 * Math.PI * arcFrac * k1;
      loopHead.setAttribute('transform', 'translate(' + (LOOP.cx + LOOP.r * Math.cos(ha)).toFixed(2) + ' ' +
        (LOOP.cy + LOOP.r * Math.sin(ha)).toFixed(2) + ') rotate(' + (ha * 180 / Math.PI + 90).toFixed(2) + ')');
      loopHead.style.opacity = k1 > 0.02 ? 1 : 0;
      loopText.style.opacity = k1;
      const kOut = ctx.seg(p, B.s1logs[0], B.s1logs[0] + 0.03);
      arcOut.setAttribute('stroke-dashoffset', (arcOut.dataset.len * (1 - kOut)).toFixed(2));
      arcOut.nextSibling.style.opacity = kOut > 0.95 ? 1 : 0;
      tagOut.style.opacity = kOut;
      logBars.forEach((l, i) => {
        const a = B.s1logs[0] + 0.02 + i * (B.s1logs[1] - B.s1logs[0] - 0.02) / logBars.length;
        const k = ctx.lin(p, a, a + 0.025);
        l.tick.style.opacity = k > 0 ? 1 : 0;
        l.bar.setAttribute('width', (l.w * k).toFixed(1));
      });
      tagLogs.style.opacity = ctx.seg(p, B.s1logs[1] - 0.02, B.s1logs[1]);
      const kBack = ctx.seg(p, B.s1loop[0] + 0.03, B.s1loop[1]);
      arcBack.setAttribute('stroke-dashoffset', (arcBack.dataset.len * (1 - kBack)).toFixed(2));
      arcBack.nextSibling.style.opacity = kBack > 0.95 ? 1 : 0;
      tagBack.style.opacity = kBack;
      const ra = -Math.PI / 2 + t * 1.6;
      runner.setAttribute('cx', (LOOP.cx + LOOP.r * Math.cos(ra)).toFixed(2));
      runner.setAttribute('cy', (LOOP.cy + LOOP.r * Math.sin(ra)).toFixed(2));
      runner.style.opacity = kBack;

      // Step 2. Squares are laid down in atlas order, then the tested ones fill.
      const M = squares.length;
      const kGrid = ctx.lin(p, B.s2grid[0], B.s2grid[1]);
      const kFill = ctx.lin(p, B.s2fill[0], B.s2fill[1]);
      let rank = 0;
      const nT = testedSet.size || 1;
      for (let i = 0; i < M; i++) {
        const q = squares[i];
        const on = ctx.clamp((kGrid * (M + 12) - i) / 12);
        q.style.opacity = on;
        if (testedSet.has(i)) {
          const f = ctx.clamp(kFill * nT - rank);
          rank++;
          q.style.background = f > 0 ? colors.zip : 'transparent';
          q.style.borderColor = f > 0 ? colors.zip : '';
          q.style.transform = 'scale(' + (1 + 0.5 * Math.sin(Math.PI * f)).toFixed(3) + ')';
        }
      }
      const kc = ctx.seg(p, B.s2count[0], B.s2count[1]);
      numEl.style.opacity = kc;
      unitEl.style.opacity = kc;
      numEl.firstChild.textContent = ctx.fmt(Math.round(Math.min(1, kFill) * COPY.step2.tested));

      // Step 3. 200 agents arrive, then the second cluster grows outward to 2,000. Dots drift a little: they are agents.
      const kNow = ctx.lin(p, B.s3now[0], B.s3now[1]);
      const kGrow = ctx.ease(ctx.lin(p, B.s3grow[0], B.s3grow[1]));
      const shownNow = Math.round(kNow * COPY.step3.now), shownTar = Math.round(kGrow * COPY.step3.target);
      g2d.setTransform(2, 0, 0, 2, 0, 0);
      g2d.clearRect(0, 0, canvas.width, canvas.height);
      for (let pass = 0; pass < 2; pass++) {
        g2d.fillStyle = pass === 0 ? colors.zip : colors.ink;
        g2d.globalAlpha = pass === 0 ? 1 : 0.62;
        g2d.beginPath();
        for (const d of dots) {
          if (d.kind !== pass || d.i >= (pass === 0 ? shownNow : shownTar)) continue;
          const x = d.x + 0.7 * Math.sin(t * 1.1 + d.ph), y = d.y + 0.7 * Math.cos(t * 0.9 + d.ph * 1.7);
          g2d.moveTo(x + DOT.r, y);
          g2d.arc(x, y, DOT.r, 0, 6.2832);
        }
        g2d.fill();
      }
      g2d.globalAlpha = 1;
      capNow.style.opacity = ctx.seg(p, B.s3now[0], B.s3now[1]);
      capTarget.style.opacity = ctx.seg(p, B.s3grow[0], B.s3grow[0] + 0.03);
      targetNum.textContent = ctx.fmt(shownTar);

      // End card: team name types on, links arrive, the QR is revealed top to bottom.
      card.style.opacity = p >= B.out[0] ? 1 : 0;
      const kn = ctx.lin(p, B.cardName[0], B.cardName[1]);
      const shown = Math.round(kn * nameChars.length);
      for (let i = 0; i < nameChars.length; i++) nameChars[i].style.opacity = i < shown ? 1 : 0;
      let cx = null;
      if (kn > 0 && kn < 1 && shown > 0) {
        const last = nameChars[shown - 1];
        cx = last.offsetLeft + last.offsetWidth + last.parentNode.offsetLeft + 10;
      }
      cursor.style.opacity = cx === null ? 0 : 1;
      if (cx !== null) cursor.style.left = cx + 'px';
      [[repoRow, B.cardRepo], [liveRow, B.cardLive]].forEach(([row, b]) => {
        const a = ctx.seg(p, b[0], b[1]);
        row.style.opacity = a;
        row.style.transform = 'translateY(' + ((1 - a) * 14).toFixed(2) + 'px)';
      });
      openRow.style.opacity = ctx.seg(p, B.cardLive[0], B.cardLive[1] + 0.03);
      const kq = ctx.seg(p, B.cardQr[0], B.cardQr[1]);
      qrBox.style.opacity = kq > 0 ? 1 : 0;
      qrBox.style.clipPath = 'inset(0 0 ' + ((1 - kq) * 100).toFixed(2) + '% 0)';
      qrNote.style.opacity = ctx.seg(p, B.cardQr[1] - 0.03, B.cardQr[1]);
    },
  });
})();
