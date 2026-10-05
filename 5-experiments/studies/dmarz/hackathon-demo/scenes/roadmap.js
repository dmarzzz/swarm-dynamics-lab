// Scenes: tracks, roadmap1, roadmap2, roadmap3. One radial research map, built once and returned to after each result.
// Data: scenes/roadmap.data.js, FILM.data.roadmap (regenerate with scenes/roadmap.build.py).
(function () {
  const COPY = {
    tracks: {
      kicker: 'first, understand the frontier',
      // 219 = candidates in 5-experiments/studies/dmarz/question-atlas/candidates.json; 15 = distinct `area` values there
      title: '219 candidate hypotheses, 15 research areas',
      centre: 'candidate hypotheses',
      each: ['Each dot is one candidate:', 'a question, a prediction,', 'a way to test it.'],
      status: 'none formally tested yet',                    // README.md: every study is exploratory
      // 3,319 = files under 1-library/{papers,threads,code,blogs,talks,datasets}/ (FACTS.md)
      source: 'from 3,319 catalogued sources, open sourced',
      // 7 tracks, 34 projects = swarmsafety.org/research.html "from questions to tracks" (roadmap.data.js siteTracks)
      tracksHead: 'experiments ran in 7 tracks',
    },
    roadmap: {
      kicker: (n) => 'what result ' + n + ' changes',
      title: (r) => r.name,
      centre: 'of 219 candidates lit',
      bears: 'bears on',
      next: 'next:',
      // evidence score = 5-experiments/evidence-metadata.json evidence_confidence.score (rubric 0 to 4)
      evidence: (r) => 'evidence ' + r.evidence + ' of ' + r.evidenceOf + ': ' + r.open,
      track: (r) => 'track: ' + r.siteTrack,
      // 12 = candidates cited by a registered study's own files (roadmap.data.js coveredCited); shown at the end of roadmap3
      rest: (n) => 'other studies in the lab cite ' + n + ' more',
    },
    // sentences, next steps and candidate links are in roadmap.data.js `results` (edit them in roadmap.build.py RESULTS)
  };

  // ---- geometry, identical in all four scenes
  const CX = 650, CY = 596, R = 270, RL = R + 24;
  const RINGS = [248, 225, 202, 179], DOT = 5.5, GAP = 0.022;
  const NS = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const pol = (r, a) => [CX + r * Math.sin(a), CY - r * Math.cos(a)];   // a = clock angle, 0 at top

  let LAYOUT = null;
  function layout() {
    if (LAYOUT) return LAYOUT;
    const D = FILM.data.roadmap, per = (2 * Math.PI) / D.total;
    let a = -D.areas[0].n * per / 2;
    const sectors = D.areas.map((s, i) => {
      const a0 = a, a1 = a + s.n * per; a = a1;
      return { i, a0, a1, mid: (a0 + a1) / 2, n: s.n, label: s.label, id: s.id };
    });
    const dots = [], byId = {};
    sectors.forEach((s) => {
      const mine = D.candidates.filter((c) => c[1] === s.i);
      // split the sector's dots over the four rings in proportion to radius (largest remainder)
      const sum = RINGS.reduce((x, y) => x + y, 0);
      const want = RINGS.map((r) => s.n * r / sum), got = want.map(Math.floor);
      let left = s.n - got.reduce((x, y) => x + y, 0);
      want.map((w, k) => [w - got[k], k]).sort((x, y) => y[0] - x[0]).forEach(([, k]) => { if (left-- > 0) got[k]++; });
      let j = 0;
      RINGS.forEach((r, k) => {
        for (let m = 0; m < got[k]; m++) {
          const f = (m + 0.5) / got[k];
          const ang = s.a0 + GAP + f * (s.a1 - s.a0 - 2 * GAP);
          const [x, y] = pol(r, ang), c = mine[j++];
          const d = { x, y, id: c[0], sector: s.i, cited: c[2], order: (ang - sectors[0].a0) / (2 * Math.PI) };
          dots.push(d); byId[c[0]] = d;
        }
      });
    });
    LAYOUT = { D, sectors, dots, byId };
    return LAYOUT;
  }

  // Builds the map into `root` and returns handles. Every scene calls this, so the figure is the same each time.
  function buildMap(root, ctx) {
    const L = layout();
    const s = svg('svg', { width: 1920, height: 1080, viewBox: '0 0 1920 1080', style: 'position:absolute;left:0;top:0;overflow:visible' }, root);
    const H = { arcs: [], labels: [], counts: [], dots: [], L };
    L.sectors.forEach((sec) => {
      const [x0, y0] = pol(R, sec.a0 + GAP * 0.6), [x1, y1] = pol(R, sec.a1 - GAP * 0.6);
      const large = sec.a1 - sec.a0 > Math.PI ? 1 : 0;
      H.arcs.push(svg('path', { d: `M${x0.toFixed(1)} ${y0.toFixed(1)}A${R} ${R} 0 ${large} 1 ${x1.toFixed(1)} ${y1.toFixed(1)}`,
        fill: 'none', stroke: 'var(--ink)', 'stroke-width': 3, 'stroke-linecap': 'butt' }, s));
      const sn = Math.sin(sec.mid), cs = Math.cos(sec.mid);
      let [lx, ly] = pol(RL, sec.mid), anchor = 'middle';
      if (sn > 0.3) anchor = 'start'; else if (sn < -0.3) anchor = 'end';
      if (anchor === 'middle') ly += cs > 0 ? -14 : 30; else ly += 8;
      const t = svg('text', { x: lx.toFixed(1), y: ly.toFixed(1), 'text-anchor': anchor, 'font-family': 'var(--mono)', 'font-size': 22, fill: 'var(--ink)' }, s);
      const name = svg('tspan', {}, t); name.textContent = sec.label;
      const cnt = svg('tspan', { dx: 10, fill: 'var(--dim)' }, t); cnt.textContent = sec.n;
      H.labels.push(t); H.counts.push(cnt);
    });
    L.dots.forEach((d) => {
      const c = svg('circle', { cx: d.x.toFixed(1), cy: d.y.toFixed(1), r: DOT, fill: 'var(--ink)' }, s);
      H.dots.push(c);
    });
    H.num = ctx.el('div', 'f-num rm-num', '', root);
    H.numL = ctx.el('div', 'rm-numL', '', root);
    return H;
  }

  const CSS = (id) => `
    #scene-${id} .abs { position:absolute; white-space:nowrap; }
    #scene-${id} .m { font-family:var(--mono); color:var(--ink); }
    #scene-${id} .rm-num { position:absolute; left:${CX - 200}px; top:${CY - 92}px; width:400px; text-align:center; font-size:112px; line-height:1; color:var(--ink); }
    #scene-${id} .rm-numL { position:absolute; left:${CX - 200}px; top:${CY + 34}px; width:400px; text-align:center; font-family:var(--mono); font-size:20px; color:var(--dim); }
  `;
  const PX = 1230, PW = 540;   // right panel

  // state of the map for a given set of lit dots; shared by the roadmap scenes
  // prev = {id: 1} lit in cyan; cur = [{id, k}] amber with k = 0..1 arrival; focus = sector indices with strength f
  function paint(H, ctx, o) {
    const L = H.L;
    L.sectors.forEach((sec, i) => {
      const f = o.focus && o.focus.indexOf(i) >= 0 ? o.f : 0;
      const base = o.built == null ? 1 : ctx.clamp((o.built - i) * 1);
      H.arcs[i].style.opacity = base * ctx.lerp(o.dimArc, 1, f);
      H.arcs[i].setAttribute('stroke-width', ctx.lerp(3, 6, f));
      H.labels[i].style.opacity = base * ctx.lerp(o.dimLabel, 1, f);
    });
    L.dots.forEach((d, j) => {
      const c = H.dots[j];
      let op = o.dotOp(d), col = 'var(--ink)', r = DOT;
      const k = o.cur && o.cur[d.id];
      if (o.prev && o.prev[d.id]) { col = 'var(--zip)'; op = 1; r = DOT + 2; }
      else if (k > 0) { col = 'var(--amber)'; op = ctx.lerp(op, 1, k); r = DOT + 2 + 5 * Math.sin(Math.PI * Math.min(1, k)) * (k < 1 ? 1 : 0); }
      else if (o.rest && d.cited) { op = ctx.lerp(op, 0.95, o.rest); }
      c.setAttribute('r', r.toFixed(2)); c.setAttribute('fill', col); c.style.opacity = op;
    });
  }

  // ---------------------------------------------------------------- scene: tracks
  (function () {
    let H, R_ = {};
    FILM.scene({
      id: 'tracks',
      mount(root, ctx) {
        const D = FILM.data.roadmap, C = COPY.tracks;
        ctx.css(CSS('tracks'));
        const mk = (cls, style, html) => { const e = ctx.el('div', cls, html || '', root); e.style.cssText += ';' + style; return e; };
        mk('f-kicker abs', 'left:100px;top:56px;font-size:22px;line-height:1', C.kicker);
        mk('f-title abs', 'left:100px;top:88px', C.title);
        H = buildMap(root, ctx);
        H.numL.textContent = C.centre;
        R_.each = mk('m abs', `left:${PX}px;top:268px;font-size:32px;line-height:1.4;white-space:pre`, C.each.join('\n'));
        R_.status = mk('m abs', `left:${PX}px;top:420px;font-size:24px;color:var(--dim)`, C.status);
        R_.head = mk('m abs', `left:${PX}px;top:520px;font-size:24px;color:var(--dim)`, C.tracksHead);
        R_.tracks = D.siteTracks.map((t, i) =>
          mk('m abs', `left:${PX}px;top:${568 + i * 44}px;font-size:28px`, t.name));
        R_.source = mk('m abs', `left:${PX}px;top:912px;font-size:22px;color:var(--dim)`, C.source);
      },
      update(p, t, ctx) {
        const L = H.L, n = L.sectors.length;
        // sectors arrive one by one between 6% and 62%; each sector's dots follow its arc
        const prog = ctx.lin(p, 0.06, 0.62) * n;
        let shown = 0;
        L.sectors.forEach((sec, i) => {
          const a = ctx.clamp(prog - i);
          H.arcs[i].style.opacity = ctx.out(ctx.clamp(a * 3));
          H.labels[i].style.opacity = ctx.out(ctx.clamp(a * 3 - 0.4));
        });
        L.dots.forEach((d, j) => {
          const sec = L.sectors[d.sector];
          const within = (d.order * 2 * Math.PI - (sec.a0 - L.sectors[0].a0)) / (sec.a1 - sec.a0);
          const a = ctx.clamp((prog - d.sector - 0.15 - within * 0.6) * 5);
          if (a > 0.5) shown++;
          H.dots[j].style.opacity = a * 0.8;
          H.dots[j].setAttribute('r', (DOT * (0.5 + 0.5 * a) + 3 * Math.sin(Math.PI * a) * (a < 1 ? 1 : 0)).toFixed(2));
        });
        const settle = ctx.seg(p, 0.64, 0.70);
        H.num.textContent = shown;
        H.num.style.opacity = ctx.seg(p, 0.05, 0.08);
        H.num.style.color = 'color-mix(in srgb, var(--amber) ' + Math.round((1 - settle) * 100) + '%, var(--ink))';
        H.numL.style.opacity = ctx.seg(p, 0.05, 0.08);
        R_.each.style.opacity = ctx.seg(p, 0.14, 0.19);
        R_.status.style.opacity = ctx.seg(p, 0.30, 0.35);
        R_.head.style.opacity = ctx.seg(p, 0.66, 0.70);
        R_.tracks.forEach((e, i) => { e.style.opacity = ctx.seg(p, 0.69 + i * 0.025, 0.72 + i * 0.025); });
        R_.source.style.opacity = ctx.seg(p, 0.48, 0.53);
      },
    });
  })();

  // ---------------------------------------------------------------- scenes: roadmap1..3
  [1, 2, 3].forEach((n) => {
    let H, P = {}, res, prev = {}, prevN = 0, focus = [];
    FILM.scene({
      id: 'roadmap' + n,
      mount(root, ctx) {
        const D = FILM.data.roadmap, C = COPY.roadmap, L = layout();
        res = D.results[n - 1];
        D.results.slice(0, n - 1).forEach((r) => r.lights.forEach((l) => { prev[l.id] = 1; }));
        prevN = Object.keys(prev).length;
        focus = res.areas.map((a) => L.sectors.findIndex((s) => s.id === a));
        ctx.css(CSS('roadmap' + n) + `
          #scene-roadmap${n} .rm-sent { left:${PX}px; top:262px; width:${PW}px; font-size:34px; line-height:1.36; white-space:normal; }
          #scene-roadmap${n} .rm-li { left:${PX}px; width:${PW}px; font-size:24px; line-height:1.36; white-space:normal; }
        `);
        const mk = (cls, style, html) => { const e = ctx.el('div', cls, html || '', root); e.style.cssText += ';' + style; return e; };
        mk('f-kicker abs', 'left:100px;top:56px;font-size:22px;line-height:1', C.kicker(n));
        mk('f-title abs', 'left:100px;top:88px', C.title(res));
        H = buildMap(root, ctx);
        H.numL.textContent = C.centre;
        P.track = mk('m abs', `left:${PX}px;top:214px;font-size:22px;color:var(--dim)`, C.track(res));
        P.sent = mk('m abs rm-sent', '', res.sentence);
        P.bearsH = mk('m abs', `left:${PX}px;top:584px;font-size:22px;color:var(--dim)`, C.bears);
        P.bears = res.lights.map((l, i) =>
          mk('m abs', `left:${PX}px;top:${622 + i * 38}px;font-size:22px`,
            l.id + '  ' + l.short));
        P.nextH = mk('m abs', `left:${PX}px;top:740px;font-size:22px;color:var(--dim)`, C.next);
        let y = 778;
        P.next = res.next.map((s) => {
          const e = mk('m abs rm-li', `top:${y}px`, s);
          y += (s.length > 36 ? 2 : 1) * 33 + 10;
          return e;
        });
        P.ev = mk('m abs', `left:${PX}px;top:516px;font-size:20px;color:var(--dim)`, C.evidence(res));
        P.rest = n === 3 ? mk('m abs', `left:${CX - 300}px;top:968px;width:600px;text-align:center;font-size:22px;color:var(--dim)`,
          C.rest(D.coveredCited - D.results.reduce((a, r) => a + r.lights.filter((l) => H.L.byId[l.id].cited).length, 0))) : null;
      },
      update(p, t, ctx) {
        const s = (a, b) => ctx.seg(p, a, b);
        // the track brightens 8..16%, dots turn amber one by one from 20%, panel follows
        const cur = {}; let lit = 0;
        res.lights.forEach((l, i) => {
          const a0 = 0.20 + i * 0.13;
          const k = ctx.lin(p, a0, a0 + 0.07);
          cur[l.id] = k; if (k > 0.5) lit++;
          P.bears[i].style.opacity = s(a0 + 0.03, a0 + 0.07);
          P.bears[i].style.color = 'var(--ink)';
        });
        const rest = n === 3 ? s(0.86, 0.92) : 0;
        paint(H, ctx, {
          focus, f: s(0.08, 0.16), dimArc: 0.35, dimLabel: 0.42,
          dotOp: (d) => focus.indexOf(d.sector) >= 0 ? ctx.lerp(0.3, 0.6, s(0.08, 0.16)) : 0.3,
          prev, cur, rest,
        });
        H.num.textContent = prevN + lit;
        H.num.style.opacity = 1; H.numL.style.opacity = 1;
        P.track.style.opacity = s(0.08, 0.13);
        P.bearsH.style.opacity = s(0.19, 0.23);
        P.sent.style.opacity = s(0.44, 0.50);
        P.nextH.style.opacity = s(0.66, 0.70);
        P.next.forEach((e, i) => { e.style.opacity = s(0.68 + i * 0.06, 0.73 + i * 0.06); });
        P.ev.style.opacity = s(0.56, 0.61);
        if (P.rest) P.rest.style.opacity = rest;
      },
    });
  });
})();
