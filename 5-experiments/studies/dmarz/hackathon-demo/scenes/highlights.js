// Scene: highlights. The bridge into the results: how many studies the lab produced, and the three the film shows.
(function () {
  const COPY = {
    kicker: 'results',
    // 118 = study folders under 5-experiments/studies (README.md, "What is in the environment": "118 study folders")
    count: 118,
    countLabel: 'studies in one weekend, all exploratory',
    pick: 'we highlight three',
    three: ['Thou shalt not split', 'How to win agents and influence swarms', 'Swarm of Theseus'],
  };
  let num, label, pick, rows = [];
  FILM.scene({
    id: 'highlights',
    mount(root, ctx) {
      ctx.css(`
        #scene-highlights .h-kicker { left:100px; top:56px; }
        #scene-highlights .h-num { left:92px; top:150px; font-size:260px; color:var(--ink); }
        #scene-highlights .h-label { left:100px; top:430px; font-size:34px; white-space:nowrap; opacity:0; }
        #scene-highlights .h-pick { left:100px; top:560px; font-size:22px; letter-spacing:.14em; text-transform:uppercase; color:var(--dim);
          white-space:nowrap; opacity:0; }
        #scene-highlights .h-row { left:100px; white-space:nowrap; opacity:0; }
        #scene-highlights .h-row i { font-style:normal; font-family:var(--display); font-weight:var(--text-display-weight); font-size:56px;
          color:var(--dim); display:inline-block; width:120px; }
        #scene-highlights .h-row b { font-weight:400; font-family:var(--display); font-weight:var(--text-display-weight); font-size:56px; }
      `);
      ctx.el('div', 'f-kicker h-kicker', COPY.kicker, root);
      num = ctx.el('div', 'f-num h-num', '', root);
      label = ctx.el('div', 'h-label', COPY.countLabel, root);
      pick = ctx.el('div', 'h-pick', COPY.pick, root);
      rows = COPY.three.map((t, i) => { const r = ctx.el('div', 'h-row', `<i>0${i + 1}</i><b>${t}</b>`, root); r.style.top = (620 + i * 96) + 'px'; return r; });
    },
    update(p, t, ctx) {
      num.textContent = ctx.fmt(Math.round(COPY.count * ctx.out(ctx.lin(p, 0.06, 0.30))));
      num.style.opacity = ctx.seg(p, 0.05, 0.10);
      num.style.color = 'color-mix(in srgb, var(--amber) ' + Math.round((1 - ctx.seg(p, 0.40, 0.48)) * 100) + '%, var(--ink))';
      label.style.opacity = ctx.seg(p, 0.16, 0.26);
      pick.style.opacity = ctx.seg(p, 0.42, 0.50);
      rows.forEach((r, i) => { const a = 0.50 + i * 0.12, k = ctx.seg(p, a, a + 0.08), next = i < 2 ? a + 0.12 : 0.92, s = ctx.seg(p, next, next + 0.05);
        r.style.opacity = k; r.style.transform = `translateY(${((1 - k) * 12).toFixed(1)}px)`;
        r.lastChild.style.color = 'color-mix(in srgb, var(--amber) ' + Math.round((1 - s) * 100) + '%, var(--ink))'; });
    },
  });
})();
