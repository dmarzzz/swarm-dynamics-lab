// Scene: method. The bridge from the three questions to the lab: literature review, open sourced, hypotheses, areas.
(function () {
  const COPY = {
    kicker: 'method',
    title: 'To answer these, we had to be scientific',
    stats: [
      // 3,319 = files under library/{papers,threads,code,blogs,talks,datasets}/ on swarm-lab main (FACTS.md)
      { n: 3319, label: 'sources in our literature review', detail: 'papers, X threads, code, blogs, talks, datasets',
        open: 'open sourced: github.com/dmarzzz/swarm-dynamics-lab' },
      // 219 = candidates in 5-experiments/studies/dmarz/question-atlas/candidates.json (the script said 215)
      { n: 219, label: 'hypotheses generated', detail: 'each with a test, a baseline and a falsifier' },
      // 15 = distinct `area` values in the same file (the script said 9 tracks; the file also has 6 `lane` values)
      { n: 15, label: 'research areas', detail: '' },
    ],
  };
  const X = [100, 800, 1400], START = [0.08, 0.36, 0.62], LEN = 0.16;
  let cols = [], rail, ticks = [];

  FILM.scene({
    id: 'method',
    mount(root, ctx) {
      ctx.css(`
        #scene-method .m-kicker { left:100px; top:56px; }
        #scene-method .m-title { left:100px; top:88px; }
        #scene-method .m-col { top:370px; width:640px; height:520px; opacity:0; }
        #scene-method .m-num { left:-6px; top:0; font-size:190px; }
        #scene-method .m-label { left:0; top:262px; font-size:34px; line-height:1.25; white-space:nowrap; }
        #scene-method .m-detail { left:0; top:318px; width:520px; font-size:22px; line-height:1.45; color:var(--dim); }
        #scene-method .m-open { left:0; top:400px; font-size:22px; line-height:1.4; color:var(--zip); white-space:nowrap; opacity:0; }
        #scene-method .m-rail { left:100px; top:600px; width:1720px; height:2px; background:var(--dim); opacity:.55; transform-origin:0 50%; }
        #scene-method .m-tick { top:592px; width:2px; height:18px; background:var(--ink); opacity:0; }
      `);
      ctx.el('div', 'f-kicker m-kicker', COPY.kicker, root);
      ctx.el('div', 'f-title m-title', COPY.title, root);
      rail = ctx.el('div', 'm-rail', '', root);
      cols = COPY.stats.map((s, i) => {
        const col = ctx.el('div', 'm-col', '', root); col.style.left = X[i] + 'px';
        const num = ctx.el('div', 'f-num m-num abs', '', col);
        ctx.el('div', 'm-label abs', s.label, col);
        ctx.el('div', 'm-detail abs', s.detail, col);
        const open = s.open ? ctx.el('div', 'm-open abs', s.open, col) : null;
        const tick = ctx.el('div', 'm-tick', '', root); tick.style.left = X[i] + 'px'; ticks.push(tick);
        return { col, num, open, n: s.n };
      });
    },
    update(p, t, ctx) {
      cols.forEach((c, i) => {
        const a = START[i], arrive = ctx.seg(p, a, a + 0.06), count = ctx.out(ctx.lin(p, a, a + LEN));
        const next = i + 1 < START.length ? START[i + 1] : 0.9, settle = ctx.seg(p, next, next + 0.05);
        c.col.style.opacity = arrive;
        c.num.textContent = ctx.fmt(Math.round(c.n * count));
        c.num.style.color = 'color-mix(in srgb, var(--amber) ' + Math.round((1 - settle) * 100) + '%, var(--ink))';
        ticks[i].style.opacity = arrive;
        if (c.open) c.open.style.opacity = ctx.seg(p, a + LEN, a + LEN + 0.06);
      });
      // the rail reaches each column as it arrives
      const reach = [0, (X[1] - 100) / 1720, (X[2] - 100) / 1720, 1];
      let r = 0;
      START.forEach((a, i) => { r = Math.max(r, ctx.lerp(reach[i], reach[i + 1], ctx.seg(p, a + 0.04, a + LEN + 0.08))); });
      rail.style.transform = `scaleX(${(p < START[0] ? 0 : r).toFixed(4)})`;
    },
  });
})();
