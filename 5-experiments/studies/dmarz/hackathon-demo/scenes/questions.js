// Scene: questions. Three research questions for distributional safety, each with a small line diagram.
(function () {
  const COPY = {
    kicker: 'distributional safety',
    title: 'Three questions for distributional safety',
    questions: [
      { n: '01', text: 'Under what scenarios will agents create Sybils?' },
      { n: '02', text: 'Can a few adversarial agents push an entire swarm into unsafe behavior?' },
      { n: '03', text: 'Can a swarm preserve its safety constraints as agents, memories, and context change?' },
    ],
    // Diagram labels. These are illustrations of the question, not results.
    sybil: { agent: '1 agent', ids: '5 identities', count: 5 },
    bft: { ring: 12, faulty: 3, label: '3 of 12 adversarial' },
    turnover: { count: 8, label: 'every agent replaced' },   // cyan = a replacement, as in result 2
  };

  // Beats, as fractions of the scene.
  const START = [0.08, 0.36, 0.64];   // each question starts arriving
  const LEN = 0.22;                   // text + diagram finish within this
  const LAST_SETTLE = 0.92;           // the last question settles to ink here

  const NS = 'http://www.w3.org/2000/svg';
  function svg(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  const rows = [];
  let dSybil, dBft, dSize;

  FILM.scene({
    id: 'questions',
    mount(root, ctx) {
      ctx.css(`
        #scene-questions .q-kicker { position:absolute; left:100px; top:56px; }
        #scene-questions .q-title { position:absolute; left:100px; top:88px; white-space:nowrap; }
        #scene-questions .q-row { position:absolute; left:100px; width:1720px; height:210px; }
        #scene-questions .q-num { position:absolute; left:0; top:50%; transform:translateY(-50%); font-family:var(--display);
          font-weight:var(--text-display-weight); font-size:96px; line-height:1; opacity:0; }
        #scene-questions .q-text { position:absolute; left:170px; top:0; width:1050px; height:210px; display:flex;
          align-items:center; font-family:var(--mono); font-size:44px; line-height:1.28; }
        #scene-questions .q-text > div { text-wrap:balance; }
        #scene-questions .q-text span { opacity:0; }
        #scene-questions .q-dia { position:absolute; left:1205px; top:-12px; width:515px; height:235px; overflow:visible; }
        #scene-questions .q-dia text { font-family:var(--mono); font-size:18px; fill:var(--dim); }
        #scene-questions .q-rule { position:absolute; left:100px; width:1720px; height:1px; background:var(--dim); opacity:0; }
      `);

      ctx.el('div', 'f-kicker q-kicker', COPY.kicker, root);
      ctx.el('div', 'f-title q-title', COPY.title, root);

      COPY.questions.forEach((q, i) => {
        const top = 236 + i * 250;
        const row = ctx.el('div', 'q-row', '', root);
        row.style.top = top + 'px';
        const num = ctx.el('div', 'q-num', q.n, row);
        const textBox = ctx.el('div', 'q-text', '', row);
        const inner = ctx.el('div', '', '', textBox);
        const chars = [];
        // Words stay whole when the line wraps; letters reveal one at a time.
        q.text.split(' ').forEach((word, wi, all) => {
          const w = document.createElement('span');
          w.style.opacity = 1;
          w.style.whiteSpace = 'nowrap';
          for (const ch of word) {
            const s = document.createElement('span');
            s.textContent = ch;
            w.appendChild(s);
            chars.push(s);
          }
          inner.appendChild(w);
          if (wi < all.length - 1) inner.appendChild(document.createTextNode(' '));
        });
        const dia = svg('svg', { class: 'q-dia', viewBox: '0 0 460 210' }, row);
        let rule = null;
        if (i > 0) {
          rule = ctx.el('div', 'q-rule', '', root);
          rule.style.top = (top - 20) + 'px';
        }
        rows.push({ num, textBox, chars, dia, rule });
      });

      // 01 Sybil: one agent dot splits into several identities.
      {
        const g = rows[0].dia, n = COPY.sybil.count;
        const ax = 70, ay = 96, ix = 290;
        const lines = [], ids = [];
        for (let j = 0; j < n; j++) {
          const y = 96 + (j - (n - 1) / 2) * 38;
          lines.push(svg('path', {
            d: `M ${ax + 14} ${ay} C ${ax + 110} ${ay}, ${ix - 110} ${y}, ${ix - 10} ${y}`,
            fill: 'none', stroke: 'var(--dim)', 'stroke-width': 2, pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1,
          }, g));
          ids.push(svg('circle', { cx: ix, cy: y, r: 8, fill: 'var(--void)', stroke: 'var(--ink)', 'stroke-width': 2, opacity: 0 }, g));
        }
        const agent = svg('circle', { cx: ax, cy: ay, r: 13, fill: 'var(--ink)', opacity: 0 }, g);
        const la = svg('text', { x: ax, y: ay + 48, 'text-anchor': 'middle', opacity: 0 }, g);
        la.textContent = COPY.sybil.agent;
        const li = svg('text', { x: ix + 26, y: ay + 6, opacity: 0 }, g);
        li.textContent = COPY.sybil.ids;
        dSybil = { lines, ids, agent, la, li };
      }

      // 02 BFT: a ring of agents, a fraction faulty (red), a threshold tick.
      {
        const g = rows[1].dia, n = COPY.bft.ring, cx = 150, cy = 108, R = 72;
        const dots = [];
        for (let j = 0; j < n; j++) {
          const a = -Math.PI / 2 + (j + 0.5) * 2 * Math.PI / n;
          dots.push(svg('circle', { cx: cx + R * Math.cos(a), cy: cy + R * Math.sin(a), r: 8, fill: 'var(--ink)', opacity: 0 }, g));
        }
        // Threshold tick at one third of the way round the ring.
        const ta = -Math.PI / 2 + 2 * Math.PI / 3;
        const RA = R + 18;   // arc just outside the ring, spanning the first third
        const arc = svg('path', {
          d: `M ${cx} ${cy - RA} A ${RA} ${RA} 0 0 1 ${(cx + RA * Math.cos(ta)).toFixed(1)} ${(cy + RA * Math.sin(ta)).toFixed(1)}`,
          fill: 'none', stroke: 'var(--dim)', 'stroke-width': 2, pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1,
        }, g);
        const tick = svg('line', {
          x1: cx + (R - 26) * Math.cos(ta), y1: cy + (R - 26) * Math.sin(ta),
          x2: cx + (R + 34) * Math.cos(ta), y2: cy + (R + 34) * Math.sin(ta),
          stroke: 'var(--ink)', 'stroke-width': 2, pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1,
        }, g);
        const lab = svg('text', { x: cx + (R + 44) * Math.cos(ta) + 8, y: cy + (R + 44) * Math.sin(ta) + 8, opacity: 0 }, g);
        lab.textContent = COPY.bft.label;
        dBft = { dots, arc, tick, lab };
      }

      // 03 Turnover: a row of agents, replaced one by one (ink dot leaves, cyan ring arrives).
      {
        const g = rows[2].dia, n = COPY.turnover.count, x0 = 28, step = 54, cy = 92;
        const olds = [], news = [];
        for (let j = 0; j < n; j++) {
          olds.push(svg('circle', { cx: x0 + j * step, cy, r: 12, fill: 'var(--ink)', opacity: 0 }, g));
          news.push(svg('circle', { cx: x0 + j * step, cy, r: 11, fill: 'var(--void)', stroke: 'var(--zip)', 'stroke-width': 3, opacity: 0 }, g));
        }
        const lab = svg('text', { x: x0 - 12, y: cy + 62, opacity: 0 }, g);
        lab.textContent = COPY.turnover.label;
        dSize = { olds, news, lab };
      }
    },

    update(p, t, ctx) {
      rows.forEach((r, i) => {
        const a = START[i];
        const next = i + 1 < START.length ? START[i + 1] : LAST_SETTLE;
        const settle = ctx.seg(p, next, next + 0.05);
        const amber = Math.round((1 - settle) * 100);
        const col = 'color-mix(in srgb, var(--amber) ' + amber + '%, var(--ink))';
        r.num.style.opacity = ctx.seg(p, a, a + 0.03);
        r.num.style.color = 'color-mix(in srgb, var(--amber) ' + amber + '%, var(--dim))';
        r.textBox.style.color = col;
        const k = ctx.lin(p, a + 0.015, a + 0.11);
        const shown = Math.round(k * r.chars.length);
        for (let j = 0; j < r.chars.length; j++) r.chars[j].style.opacity = j < shown ? 1 : 0;
        if (r.rule) r.rule.style.opacity = 0.35 * ctx.seg(p, a - 0.02, a + 0.02);
      });

      // Diagram build progress per question, 0..1.
      const d = START.map((a) => ctx.lin(p, a + 0.05, a + LEN));

      // 01 Sybil
      {
        const k = d[0], n = dSybil.lines.length;
        dSybil.agent.setAttribute('opacity', ctx.seg(k, 0, 0.15));
        dSybil.la.setAttribute('opacity', ctx.seg(k, 0.05, 0.25));
        for (let j = 0; j < n; j++) {
          const s = 0.2 + j * 0.1;
          dSybil.lines[j].setAttribute('stroke-dashoffset', (1 - ctx.seg(k, s, s + 0.3)).toFixed(3));
          dSybil.ids[j].setAttribute('opacity', ctx.seg(k, s + 0.24, s + 0.34));
        }
        dSybil.li.setAttribute('opacity', ctx.seg(k, 0.85, 1));
      }

      // 02 BFT
      {
        const k = d[1], n = dBft.dots.length, f = COPY.bft.faulty;
        const bad = ctx.clamp((k - 0.55) / 0.25);
        for (let j = 0; j < n; j++) {
          dBft.dots[j].setAttribute('opacity', ctx.seg(k, j * 0.04, j * 0.04 + 0.08));
          const isBad = j < f && bad > j / f;
          dBft.dots[j].setAttribute('fill', isBad ? 'var(--no)' : 'var(--ink)');
        }
        dBft.arc.setAttribute('stroke-dashoffset', (1 - ctx.seg(k, 0.6, 0.84)).toFixed(3));
        dBft.tick.setAttribute('stroke-dashoffset', (1 - ctx.seg(k, 0.8, 0.92)).toFixed(3));
        dBft.lab.setAttribute('opacity', ctx.seg(k, 0.88, 1));
      }

      // 03 Turnover
      {
        const k = d[2], n = dSize.olds.length;
        for (let j = 0; j < n; j++) {
          const arrive = ctx.seg(k, j * 0.03, j * 0.03 + 0.08);
          const swap = ctx.seg(k, 0.3 + j * 0.07, 0.3 + j * 0.07 + 0.1);
          dSize.olds[j].setAttribute('opacity', (arrive * (1 - swap)).toFixed(3));
          dSize.olds[j].setAttribute('cy', (92 + swap * 26).toFixed(1));
          dSize.news[j].setAttribute('opacity', swap.toFixed(3));
        }
        dSize.lab.setAttribute('opacity', ctx.seg(k, 0.9, 1));
      }
    },
  });
})();
