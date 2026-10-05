// Scene: twoopen (opening card of the two-experiment cut, ?film=two). What we set out to study, then the two questions.
// The dots are the agents of each run: 180 owners (sybil-rules-180) and 50 positions (swarm-of-theseus S50).
(function () {
  const COPY = {
    // README.md of the repo: "a research lab run by the swarm it studies"; the lab is open source (LICENSE, MIT)
    line: ['Swarm Dynamics Lab', 'open source', 'controlled experiments on groups of AI agents'],
    title: 'Two swarm experiments',
    // the frame of the four-minute cut (scenes/frame.js, INTRO-FACTS.md): single-agent safety against the properties of the whole system
    frame: ['single-agent safety: is one model’s behaviour acceptable?',
      'properties of swarms: what holds, and what fails, for a whole system of interacting agents?'],
    rows: [
      {
        n: '1', prop: 'Sybil resistance',
        q: ['Does a market rule still bind when', 'one owner can act as several firms?'],
        // 5-experiments/studies/dmarz/sybil-rules-180/RESULTS.md ("What was run": 180 owners, model gpt-6-sol)
        who: '180 agents in one economy // GPT-6 Sol',
        agents: 180,
      },
      {
        n: '2', prop: 'continuity under turnover',
        q: ['Does what a group learned survive', 'when every member is replaced?'],
        // 5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-POST-MORTEM.md
        // ("a connected institution with 50 active positions"; "All 50 founders acquired correct private routes")
        who: '50 agents in one institution // GPT-6 Sol',
        agents: 50,
      },
    ],
  };

  // Cues: seconds into the narration clip at which each phrase starts (word timings of _out/vo-two/twoopen.wav); the scene
  // adds the 0.25 s of silence before the voice. The title and the lab's name are on screen from the first frame: a chat
  // app shows that frame as the preview.
  const CUE = { frame: [0.0, 4.1], line: [null, 10.9, 11.6], row: [15.8, 21.7] };
  const LEAD = 0.25;
  const ROW_Y = [470, 716], DOT_X = 1290;
  const NS = 'http://www.w3.org/2000/svg';
  let segs = [], frame = [], rows = [], dots = [[], []];

  FILM.scene({
    id: 'twoopen',
    mount(root, ctx) {
      ctx.css(`
        #scene-twoopen .to { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-twoopen .to-line { left:100px; top:56px; font-size:22px; line-height:1; letter-spacing:.16em; text-transform:uppercase; color:var(--dim); }
        #scene-twoopen .to-title { left:94px; top:128px; font-family:var(--display); font-weight:var(--text-display-weight);
          font-size:124px; line-height:1; color:var(--ink); }
        #scene-twoopen .to-frame { left:100px; font-size:28px; line-height:1; opacity:0; }
        #scene-twoopen .to-row { position:absolute; left:0; width:1920px; height:200px; opacity:0; }
        #scene-twoopen .to-n { left:100px; top:22px; font-family:var(--display); font-weight:var(--text-display-weight); font-size:116px;
          line-height:1; color:var(--dim); }
        #scene-twoopen .to-prop { left:236px; top:0; font-size:22px; line-height:1; letter-spacing:.12em; text-transform:uppercase; color:var(--dim); }
        #scene-twoopen .to-q { left:236px; top:36px; font-size:36px; line-height:1.36; color:var(--ink); }
        #scene-twoopen .to-who { left:236px; top:150px; font-size:20px; line-height:1; letter-spacing:.12em; text-transform:uppercase; color:var(--dim); }
        #scene-twoopen svg { position:absolute; left:0; top:0; width:1920px; height:1080px; }
      `);
      const line = ctx.el('div', 'to to-line', '', root);
      COPY.line.forEach((s, i) => segs.push(ctx.el('span', '', (i ? '&nbsp;// ' : '') + s, line)));
      ctx.el('div', 'to to-title', COPY.title, root);
      COPY.frame.forEach((s, i) => { const e = ctx.el('div', 'to to-frame', s, root); e.style.top = (300 + i * 46) + 'px';
        e.style.color = i ? 'var(--ink)' : 'var(--dim)'; frame.push(e); });
      const g = document.createElementNS(NS, 'svg'); g.setAttribute('viewBox', '0 0 1920 1080'); root.appendChild(g);
      const dot = (x, y, r, k) => { const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', x.toFixed(1));
        c.setAttribute('cy', y.toFixed(1)); c.setAttribute('r', r); c.setAttribute('fill', 'var(--ink)'); c.setAttribute('opacity', 0);
        g.appendChild(c); dots[k].push(c); };
      COPY.rows.forEach((r, k) => {
        const row = ctx.el('div', 'to-row', '', root); row.style.top = ROW_Y[k] + 'px';
        ctx.el('div', 'to to-n', r.n, row);
        ctx.el('div', 'to to-prop', r.prop, row);
        ctx.el('div', 'to to-q', r.q.join('<br>'), row);
        ctx.el('div', 'to to-who', r.who, row);
        rows.push(row);
      });
      // experiment 1: 180 agents as 30 x 6. experiment 2: 50 agents as a ring, the shape its scene uses.
      for (let i = 0; i < COPY.rows[0].agents; i++) dot(DOT_X + (i % 30) * 17, ROW_Y[0] + 48 + Math.floor(i / 30) * 17, 4.5, 0);
      const n2 = COPY.rows[1].agents, cx = DOT_X + 246, cy = ROW_Y[1] + 88;
      for (let i = 0; i < n2; i++) { const a = -Math.PI / 2 + i * 2 * Math.PI / n2; dot(cx + 80 * Math.cos(a), cy + 80 * Math.sin(a), 4.5, 1); }
    },
    update(p, t, ctx) {
      const at = (cue, len) => ctx.ease(ctx.lin(t, cue + LEAD, cue + LEAD + (len || 0.6)));
      segs.forEach((s, i) => { s.style.opacity = CUE.line[i] == null ? 1 : at(CUE.line[i]); });
      frame.forEach((e, i) => { e.style.opacity = at(CUE.frame[i] + 0.3); });
      rows.forEach((row, i) => { const a = at(CUE.row[i]);
        row.style.opacity = a; row.style.transform = `translateY(${((1 - a) * 14).toFixed(2)}px)`; });
      dots.forEach((list, i) => { list.forEach((c, j) => { c.setAttribute('opacity', at(CUE.row[i] + 0.8 + j / list.length * 2.2, 0.7).toFixed(3)); }); });
    },
  });
})();
