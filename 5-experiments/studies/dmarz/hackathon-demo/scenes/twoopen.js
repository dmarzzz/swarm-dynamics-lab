// Scene: twoopen (opening card of the two-experiment cut, ?film=two). What the lab is, then the two questions.
// The dots are the agents of each run: 180 owners (sybil-rules-180) and 50 positions (swarm-of-theseus S50).
(function () {
  const COPY = {
    // README.md of the repo: "a research lab run by the swarm it studies"; the lab is open source (LICENSE, MIT)
    line: ['Swarm Dynamics Lab', 'open source', 'AI agents running experiments on groups of AI agents'],
    title: 'Two swarm experiments',
    rows: [
      {
        n: '1',
        q: ['Will agents split one business into', 'several firms to dodge a rule?'],
        // 5-experiments/studies/dmarz/sybil-rules-180/RESULTS.md ("What was run": 180 owners, model gpt-6-sol)
        who: '180 agents in one economy // GPT-6 Sol',
        agents: 180,
      },
      {
        n: '2',
        q: ['Does a group keep what its founders', 'learned, once every founder is replaced?'],
        // 5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-POST-MORTEM.md
        // ("a connected institution with 50 active positions"; "All 50 founders acquired correct private routes")
        who: '50 agents in one institution // GPT-6 Sol',
        agents: 50,
      },
    ],
  };

  // Beats, as fractions of the scene. They follow the narration: the lab, then question 1, then question 2.
  // The title and the lab's name are on screen from the first frame: a chat app shows that frame as the preview.
  const B = {
    line: [null, [0.18, 0.22], [0.24, 0.30]],
    row: [[0.42, 0.47], [0.69, 0.74]],
    dots: [[0.46, 0.62], [0.73, 0.87]],
  };
  const ROW_Y = [436, 700], DOT_X = 1290;
  const NS = 'http://www.w3.org/2000/svg';
  let segs = [], rows = [], dots = [[], []];

  FILM.scene({
    id: 'twoopen',
    mount(root, ctx) {
      ctx.css(`
        #scene-twoopen .to { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-twoopen .to-line { left:100px; top:56px; font-size:22px; line-height:1; letter-spacing:.16em; text-transform:uppercase; color:var(--dim); }
        #scene-twoopen .to-title { left:94px; top:150px; font-family:var(--display); font-weight:var(--text-display-weight);
          font-size:124px; line-height:1; color:var(--ink); }
        #scene-twoopen .to-row { position:absolute; left:0; width:1920px; height:200px; opacity:0; }
        #scene-twoopen .to-n { left:100px; top:0; font-family:var(--display); font-weight:var(--text-display-weight); font-size:116px;
          line-height:1; color:var(--dim); }
        #scene-twoopen .to-q { left:236px; top:2px; font-size:38px; line-height:1.36; color:var(--ink); }
        #scene-twoopen .to-who { left:236px; top:124px; font-size:22px; line-height:1; letter-spacing:.12em; text-transform:uppercase; color:var(--dim); }
        #scene-twoopen svg { position:absolute; left:0; top:0; width:1920px; height:1080px; }
      `);
      const line = ctx.el('div', 'to to-line', '', root);
      COPY.line.forEach((s, i) => segs.push(ctx.el('span', '', (i ? '&nbsp;// ' : '') + s, line)));
      ctx.el('div', 'to to-title', COPY.title, root);
      const g = document.createElementNS(NS, 'svg'); g.setAttribute('viewBox', '0 0 1920 1080'); root.appendChild(g);
      const dot = (x, y, r, k) => { const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', x.toFixed(1));
        c.setAttribute('cy', y.toFixed(1)); c.setAttribute('r', r); c.setAttribute('fill', 'var(--ink)'); c.setAttribute('opacity', 0);
        g.appendChild(c); dots[k].push(c); };
      COPY.rows.forEach((r, k) => {
        const row = ctx.el('div', 'to-row', '', root); row.style.top = ROW_Y[k] + 'px';
        ctx.el('div', 'to to-n', r.n, row);
        ctx.el('div', 'to to-q', r.q.join('<br>'), row);
        ctx.el('div', 'to to-who', r.who, row);
        rows.push(row);
      });
      // experiment 1: 180 agents as 30 x 6. experiment 2: 50 agents as a ring, the shape its scene uses.
      for (let i = 0; i < COPY.rows[0].agents; i++) dot(DOT_X + (i % 30) * 17, ROW_Y[0] + 14 + Math.floor(i / 30) * 17, 4.5, 0);
      const n2 = COPY.rows[1].agents, cx = DOT_X + 246, cy = ROW_Y[1] + 62;
      for (let i = 0; i < n2; i++) { const a = -Math.PI / 2 + i * 2 * Math.PI / n2; dot(cx + 86 * Math.cos(a), cy + 86 * Math.sin(a), 4.5, 1); }
    },
    update(p, t, ctx) {
      segs.forEach((s, i) => { s.style.opacity = B.line[i] ? ctx.seg(p, B.line[i][0], B.line[i][1]) : 1; });
      rows.forEach((row, i) => { const a = ctx.seg(p, B.row[i][0], B.row[i][1]);
        row.style.opacity = a; row.style.transform = `translateY(${((1 - a) * 14).toFixed(2)}px)`; });
      dots.forEach((list, i) => { const [a, b] = B.dots[i], span = (b - a) * 0.75;
        list.forEach((c, j) => { const f = j / list.length * span; c.setAttribute('opacity', ctx.seg(p, a + f, a + f + (b - a) * 0.25).toFixed(3)); }); });
    },
  });
})();
