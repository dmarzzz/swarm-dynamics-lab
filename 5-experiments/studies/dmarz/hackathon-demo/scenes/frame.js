// Scene: frame. The definition, for the long film (replaces `define`). Designed for about 35 seconds, two parts.
// Sources (see ../INTRO-FACTS.md for the quotes):
//   Term: N. Tomasev, M. Franklin, J. Jacobs, S. Krier, S. Osindero, "Distributional AGI Safety", Google DeepMind,
//   arXiv:2512.16856 (v1 2025-12-18, v2 2026-05-19). The paper proposes "a framework for distributional AGI safety that
//   moves beyond evaluating and aligning individual agents" (abstract). It gives no one-line definition; the two
//   questions on screen are our gloss.
//   The three-agent chain is our own illustration, not a result and not the paper's example: the cite line leaves
//   before it starts and the tag on screen says so. It shows no numbers. It shows two routes out, one after the other:
//   path 1 through each other, path 2 through a message board the agents set up (an echo of the previous scene).
(function () {
  const COPY = {
    kicker: 'the lens',
    title: 'What is distributional safety?',
    left: { name: 'Single-agent safety', asks: 'Is one model’s behaviour acceptable?' },
    right: { name: 'Distributional safety', asks: 'Do the properties of the whole system of interacting agents hold?' },
    cite: 'after Tomašev et al., Google DeepMind, 2025, arXiv:2512.16856',   // "Distributional AGI Safety"; "after" because the two questions are our gloss
    swarm: 110,   // dots in the illustration, not a result
    chain: {
      heading: 'Three agents, each safe on its own',
      tag: 'an illustration, not a result',
      data: 'private data',
      net: 'the internet',
      agents: [
        { can: 'can read the data', cannot: 'no network' },
        { can: 'can pass messages', cannot: 'no data, no network' },
        { can: 'can post online', cannot: 'cannot see the data' },
      ],
      safe: 'safe alone',
      path1: 'path 1: through each other',
      board: 'a message board they set up',
      path2: 'path 2: a shared board',
      leak: 'two ways out: through each other, or through a board they built',
      verdict: 'Every agent passes its own check. The system fails.',
    },
    scope: 'We test three group-level properties in small exploratory experiments. No claim about AGI.',
  };

  // beats, as fractions of the scene
  const B1_OUT = [0.36, 0.39], B2_IN = 0.385, ARRIVE = [0.41, 0.49, 0.57];   // agents done by 0.64
  const LINES = 0.68, HOP0 = 0.70, HOP = 0.014, LAND = HOP0 + 4 * HOP;   // path 1: the token lands at 0.756
  const UNSAFE = [0.755, 0.775], POP = 0.77, LINES2 = 0.79;              // the checks leave, the board pops up, its lines draw
  const HOPS2 = [0.808, 0.820, 0.834, 0.838, 0.852, 0.866], LAND2 = HOPS2[5];   // path 2: to agent 1, to the board, (posted, read), to agent 3, out
  const VERDICT = 0.88, SCOPE = 0.91;

  const NS = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const draw = (attrs, parent) => svg('path', Object.assign({ fill: 'none', pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, attrs), parent);
  const tick = (x, y, parent) => draw({ d: `M ${x - 10} ${y} l 7 8 l 14 -17`, stroke: 'var(--zip)', 'stroke-width': 3 }, parent);
  const off = (e, v) => e.setAttribute('stroke-dashoffset', (1 - v).toFixed(3));

  const LX = 520, RX = 1380, CY = 400, RING = 162;   // beat 1
  const ROW = 520, AX = [620, 960, 1300], AR = 44, CAP = 72;   // the chain: row centre line, agents, agent ring, group ring
  const BOX = { w: 240, h: 84, data: 220, net: 1700 };          // box centres; the data box spans x 100..340, the internet box 1580..1820
  const STOPS = [BOX.data + BOX.w / 2, AX[0], AX[1], AX[2], BOX.net - BOX.w / 2];   // where the token rests between hops
  const BD = { x: 960, y: 340, w: 420, h: 60 };                  // the message board, centred over agent 2
  const UP = [[AX[0], ROW], [AX[0], BD.y], [BD.x - BD.w / 2, BD.y]];     // path 2: agent 1 up to the board
  const DOWN = [[BD.x + BD.w / 2, BD.y], [AX[2], BD.y], [AX[2], ROW]];   // path 2: the board down to agent 3
  const TOP = BD.y - BD.h / 2 - 26;                              // top of the red ring, above the board
  const along = (pts, u) => { const a = Math.abs(pts[1][0] - pts[0][0]) + Math.abs(pts[1][1] - pts[0][1]),
    b = Math.abs(pts[2][0] - pts[1][0]) + Math.abs(pts[2][1] - pts[1][1]), d = u * (a + b);
    const [s, e, f] = d <= a ? [pts[0], pts[1], a ? d / a : 0] : [pts[1], pts[2], (d - a) / b];
    return [s[0] + (e[0] - s[0]) * f, s[1] + (e[1] - s[1]) * f]; };
  let b1, g1, one, oneRing, dots = [], swarmG, bigRing, divider, lt, rt, cite;
  let g2, head, tag, dataBox, netBox, dataLbl, netLbl, agents = [], links = [], token, group, leak, verdict, scope;
  let boardG, boardBox, boardLbl, links2 = [], p1Lbl, p2Lbl;

  FILM.scene({
    id: 'frame',
    mount(root, ctx) {
      ctx.css(`
        #scene-frame .abs { position:absolute; font-family:var(--mono); }
        #scene-frame .fr-kicker { left:100px; top:56px; }
        #scene-frame .fr-title { left:100px; top:88px; white-space:nowrap; font-family:var(--display); }
        #scene-frame svg { position:absolute; left:0; top:0; width:1920px; height:1080px; }
        #scene-frame .fr-b1 { left:0; top:0; width:1920px; height:1080px; }
        #scene-frame .fr-text { top:612px; width:780px; text-align:center; opacity:0; }
        #scene-frame .fr-name { font-size:46px; line-height:1.2; margin-bottom:18px; white-space:nowrap; }
        #scene-frame .fr-asks { font-size:34px; line-height:1.35; color:var(--ink); text-wrap:balance; }
        #scene-frame .fr-div { left:950px; top:220px; width:1px; height:600px; background:var(--dim); opacity:0; transform-origin:50% 0; }
        #scene-frame .fr-cite { left:100px; top:960px; font-size:24px; color:var(--dim); white-space:nowrap; opacity:0; }
        #scene-frame .fr-head { left:100px; top:204px; font-size:38px; color:var(--ink); white-space:nowrap; opacity:0; }
        #scene-frame .fr-tag { left:100px; top:266px; font-size:24px; color:var(--dim); white-space:nowrap; opacity:0; }
        #scene-frame .fr-box { top:${ROW - 16}px; width:${BOX.w}px; text-align:center; font-size:24px; line-height:32px; color:var(--ink);
          white-space:nowrap; opacity:0; }
        #scene-frame .fr-safe { top:396px; font-size:24px; line-height:32px; color:var(--ink); white-space:nowrap; opacity:0; }
        #scene-frame .fr-agent { top:616px; width:340px; text-align:center; font-size:26px; line-height:1.35; white-space:nowrap; }
        #scene-frame .fr-can { color:var(--ink); opacity:0; }
        #scene-frame .fr-cannot { color:var(--dim); opacity:0; }
        #scene-frame .fr-board { left:${BD.x - BD.w / 2}px; top:${BD.y - BD.h / 2}px; width:${BD.w}px; height:${BD.h}px; line-height:${BD.h}px;
          text-align:center; font-size:22px; color:var(--ink); white-space:nowrap; opacity:0; }
        #scene-frame .fr-path { width:340px; text-align:center; font-size:20px; line-height:24px; color:var(--dim); white-space:nowrap; opacity:0; }
        #scene-frame .fr-leak { left:100px; top:722px; font-size:34px; color:var(--no); white-space:nowrap; opacity:0; }
        #scene-frame .fr-verdict { left:100px; top:796px; font-size:44px; color:var(--ink); white-space:nowrap; opacity:0; }
        #scene-frame .fr-scope { left:100px; top:900px; font-size:30px; white-space:nowrap; opacity:0; }
      `);
      ctx.el('div', 'f-kicker abs fr-kicker', COPY.kicker, root);
      ctx.el('div', 'f-title abs fr-title', COPY.title, root);

      // ---- beat 1: the split frame
      b1 = ctx.el('div', 'abs fr-b1', '', root);
      g1 = svg('svg', { viewBox: '0 0 1920 1080' }, b1);
      oneRing = svg('circle', { cx: LX, cy: CY, r: 60, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2.5, pathLength: 1,
        'stroke-dasharray': 1, 'stroke-dashoffset': 1, transform: `rotate(-90 ${LX} ${CY})` }, g1);
      one = svg('circle', { cx: LX, cy: CY, r: 19, fill: 'var(--ink)', opacity: 0 }, g1);
      swarmG = svg('g', {}, g1);
      const golden = Math.PI * (3 - Math.sqrt(5)), c = 12.8;
      for (let j = 0; j < COPY.swarm; j++) { const r = c * Math.sqrt(j + 0.5), a = j * golden;
        dots.push(svg('circle', { cx: (RX + r * Math.cos(a)).toFixed(1), cy: (CY + r * Math.sin(a)).toFixed(1), r: 5.6, fill: 'var(--ink)', opacity: 0 }, swarmG)); }
      bigRing = svg('circle', { cx: RX, cy: CY, r: RING, fill: 'none', stroke: 'var(--amber)', 'stroke-width': 3, pathLength: 1,
        'stroke-dasharray': 1, 'stroke-dashoffset': 1, transform: `rotate(-90 ${RX} ${CY})` }, g1);
      divider = ctx.el('div', 'abs fr-div', '', b1);
      lt = ctx.el('div', 'abs fr-text', `<div class="fr-name">${COPY.left.name}</div><div class="fr-asks">${COPY.left.asks}</div>`, b1);
      lt.style.left = (LX - 390) + 'px';
      rt = ctx.el('div', 'abs fr-text', `<div class="fr-name" style="color:var(--amber)">${COPY.right.name}</div><div class="fr-asks">${COPY.right.asks}</div>`, b1);
      rt.style.left = (RX - 390) + 'px';
      cite = ctx.el('div', 'abs fr-cite', COPY.cite, root);   // belongs to beat 1 only: the chain below is our example, not the paper's

      // ---- beat 2: three agents, each restricted, chained into a leak (an illustration)
      const K = COPY.chain;
      head = ctx.el('div', 'abs fr-head', K.heading, root);
      tag = ctx.el('div', 'abs fr-tag', K.tag, root);
      g2 = svg('svg', { viewBox: '0 0 1920 1080' }, root);
      const box = cx => draw({ d: `M ${cx - BOX.w / 2} ${ROW - BOX.h / 2} h ${BOX.w} v ${BOX.h} h ${-BOX.w} Z`, stroke: 'var(--ink)', 'stroke-width': 2 }, g2);
      dataBox = box(BOX.data); netBox = box(BOX.net);
      dataLbl = ctx.el('div', 'abs fr-box', K.data, root); dataLbl.style.left = (BOX.data - BOX.w / 2) + 'px';
      netLbl = ctx.el('div', 'abs fr-box', K.net, root); netLbl.style.left = (BOX.net - BOX.w / 2) + 'px';
      const ends = [[STOPS[0], AX[0] - AR], [AX[0] + AR, AX[1] - AR], [AX[1] + AR, AX[2] - AR], [AX[2] + AR, STOPS[4]]];
      links = ends.map(([a, b]) => draw({ d: `M ${a} ${ROW} L ${b} ${ROW}`, stroke: 'var(--ink)', 'stroke-width': 2 }, g2));
      K.agents.forEach((ag, i) => {
        const x = AX[i];
        const ring = svg('circle', { cx: x, cy: ROW, r: AR, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2, pathLength: 1,
          'stroke-dasharray': 1, 'stroke-dashoffset': 1, transform: `rotate(-90 ${x} ${ROW})` }, g2);
        const dot = svg('circle', { cx: x, cy: ROW, r: 16, fill: 'var(--ink)', opacity: 0 }, g2);
        const check = tick(x - 80, 414, g2);
        const safe = ctx.el('div', 'abs fr-safe', K.safe, root); safe.style.left = (x - 54) + 'px';
        const txt = ctx.el('div', 'abs fr-agent', '', root); txt.style.left = (x - 170) + 'px';
        const can = ctx.el('div', 'fr-can', ag.can, txt), cannot = ctx.el('div', 'fr-cannot', ag.cannot, txt);
        agents.push({ ring, dot, check, safe, can, cannot });
      });
      // path 2: a message board pops up above the row; agent 1 pushes to it, agent 3 reads from it
      boardG = svg('g', {}, g2);
      boardBox = draw({ d: `M ${BD.x - BD.w / 2} ${BD.y - BD.h / 2} h ${BD.w} v ${BD.h} h ${-BD.w} Z`, stroke: 'var(--ink)', 'stroke-width': 2 }, boardG);
      boardLbl = ctx.el('div', 'abs fr-board', K.board, root);
      links2 = [draw({ d: `M ${AX[0]} ${ROW - AR} V ${BD.y} H ${BD.x - BD.w / 2}`, stroke: 'var(--ink)', 'stroke-width': 2 }, g2),
        draw({ d: `M ${BD.x + BD.w / 2} ${BD.y} H ${AX[2]} V ${ROW - AR}`, stroke: 'var(--ink)', 'stroke-width': 2 }, g2)];
      p1Lbl = ctx.el('div', 'abs fr-path', K.path1, root); p1Lbl.style.left = ((AX[0] + AX[1]) / 2 + 10 - 170) + 'px'; p1Lbl.style.top = (ROW - 74) + 'px';
      p2Lbl = ctx.el('div', 'abs fr-path', K.path2, root); p2Lbl.style.left = (BD.x - 170) + 'px'; p2Lbl.style.top = (BD.y + BD.h / 2 + 12) + 'px';
      // one red ring around the whole system: the three agents and the board they built
      group = draw({ d: `M ${AX[0]} ${TOP} H ${AX[2]} A ${CAP} ${CAP} 0 0 1 ${AX[2] + CAP} ${TOP + CAP} V ${ROW} A ${CAP} ${CAP} 0 0 1 ${AX[2]} ${ROW + CAP} H ${AX[0]} A ${CAP} ${CAP} 0 0 1 ${AX[0] - CAP} ${ROW} V ${TOP + CAP} A ${CAP} ${CAP} 0 0 1 ${AX[0]} ${TOP} Z`,
        stroke: 'var(--no)', 'stroke-width': 3 }, g2);
      token = svg('circle', { cx: STOPS[0], cy: ROW, r: 10, fill: 'var(--amber)', opacity: 0 }, g2);   // the one amber signal
      leak = ctx.el('div', 'abs fr-leak', K.leak, root);
      verdict = ctx.el('div', 'abs fr-verdict', K.verdict, root);
      scope = ctx.el('div', 'abs fr-scope', COPY.scope, root);
    },
    update(p, t, ctx) {
      // ---- beat 1
      const gone = 1 - ctx.seg(p, B1_OUT[0], B1_OUT[1]);
      b1.style.opacity = gone.toFixed(3);
      one.setAttribute('opacity', ctx.seg(p, 0.03, 0.055));
      off(oneRing, ctx.seg(p, 0.045, 0.095));
      lt.style.opacity = ctx.seg(p, 0.07, 0.11);
      divider.style.opacity = 0.4 * ctx.seg(p, 0.12, 0.15);
      divider.style.transform = `scaleY(${ctx.seg(p, 0.12, 0.165).toFixed(3)})`;
      const k = ctx.lin(p, 0.15, 0.24) * dots.length;
      for (let j = 0; j < dots.length; j++) dots[j].setAttribute('opacity', ctx.clamp(k - j).toFixed(2));
      swarmG.setAttribute('transform', `rotate(${(t * 1.5).toFixed(2)} ${RX} ${CY})`);   // alive: a slow turn
      off(bigRing, ctx.seg(p, 0.225, 0.29));
      rt.style.opacity = ctx.seg(p, 0.25, 0.30);

      // ---- beat 2: the chain
      cite.style.opacity = ctx.seg(p, 0.27, 0.31) * gone;
      head.style.opacity = ctx.seg(p, B2_IN, B2_IN + 0.03);
      tag.style.opacity = ctx.seg(p, B2_IN + 0.015, B2_IN + 0.045);
      off(dataBox, ctx.seg(p, B2_IN + 0.005, B2_IN + 0.035)); dataLbl.style.opacity = ctx.seg(p, B2_IN + 0.02, B2_IN + 0.04);
      off(netBox, ctx.seg(p, B2_IN + 0.01, B2_IN + 0.04)); netLbl.style.opacity = ctx.seg(p, B2_IN + 0.025, B2_IN + 0.045);
      const dimmed = 1 - ctx.seg(p, UNSAFE[0], UNSAFE[1]);   // "safe alone" is gone before path 2 draws through that space
      agents.forEach((a, i) => { const s = ARRIVE[i];
        a.dot.setAttribute('opacity', ctx.seg(p, s, s + 0.02));
        off(a.ring, ctx.seg(p, s + 0.01, s + 0.04));
        a.can.style.opacity = ctx.seg(p, s + 0.015, s + 0.035);
        a.cannot.style.opacity = ctx.seg(p, s + 0.03, s + 0.05);
        off(a.check, ctx.seg(p, s + 0.05, s + 0.065)); a.check.setAttribute('opacity', dimmed.toFixed(3));
        a.safe.style.opacity = (ctx.seg(p, s + 0.05, s + 0.07) * dimmed).toFixed(3);
      });
      // path 1: through each other
      const second = ctx.seg(p, POP, LINES2), done = ctx.seg(p, LAND2, LAND2 + 0.02);
      links.forEach((e, i) => { off(e, ctx.seg(p, LINES + i * 0.008, LINES + 0.012 + i * 0.008));
        e.setAttribute('opacity', (1 - 0.6 * second + 0.6 * done).toFixed(3)); });   // steps back while path 2 plays
      p1Lbl.style.opacity = ctx.seg(p, LINES, LINES + 0.02);
      // path 2: the board pops up, then its two lines
      const pop = (0.8 + 0.2 * ctx.out(ctx.lin(p, POP, POP + 0.012))).toFixed(3);
      boardG.setAttribute('transform', `translate(${BD.x} ${BD.y}) scale(${pop}) translate(${-BD.x} ${-BD.y})`);
      off(boardBox, ctx.seg(p, POP, POP + 0.015));
      boardLbl.style.opacity = ctx.seg(p, POP + 0.004, POP + 0.018); boardLbl.style.transform = `scale(${pop})`;
      off(links2[0], ctx.seg(p, LINES2, LINES2 + 0.009)); off(links2[1], ctx.seg(p, LINES2 + 0.007, LINES2 + 0.016));
      p2Lbl.style.opacity = ctx.seg(p, LINES2, LINES2 + 0.02);
      // the one amber signal: the same token runs path 1, then path 2
      let tx = STOPS[0], ty = ROW, ta;
      if (p < LINES2) {
        for (let k = 0; k < 4; k++) tx += (STOPS[k + 1] - STOPS[k]) * ctx.seg(p, HOP0 + k * HOP, HOP0 + (k + 1) * HOP);
        ta = ctx.seg(p, HOP0 - 0.008, HOP0) * (1 - ctx.seg(p, LAND, LAND + 0.012));
      } else {
        const H = HOPS2;
        if (p < H[1]) tx += (AX[0] - STOPS[0]) * ctx.seg(p, H[0], H[1]);
        else if (p < (H[2] + H[3]) / 2) [tx, ty] = along(UP, ctx.seg(p, H[1], H[2]));        // pushed to the board
        else if (p < H[4]) [tx, ty] = along(DOWN, ctx.seg(p, H[3], H[4]));                   // read from the board
        else tx = AX[2] + (STOPS[4] - AX[2]) * ctx.seg(p, H[4], H[5]);
        const mid = (H[2] + H[3]) / 2;
        ta = ctx.seg(p, H[0] - 0.008, H[0]) * (1 - ctx.seg(p, H[2] - 0.001, mid) + ctx.seg(p, mid, H[3] + 0.001)) * (1 - ctx.seg(p, LAND2, LAND2 + 0.012));
      }
      token.setAttribute('cx', tx.toFixed(1)); token.setAttribute('cy', ty.toFixed(1));
      token.setAttribute('opacity', ctx.clamp(ta).toFixed(3));
      // the red state, after both routes have been shown
      netBox.setAttribute('stroke', p >= LAND2 ? 'var(--no)' : 'var(--ink)');
      off(group, ctx.seg(p, LAND2, LAND2 + 0.014));
      leak.style.opacity = ctx.seg(p, LAND2 + 0.002, LAND2 + 0.014);
      verdict.style.opacity = ctx.seg(p, VERDICT, VERDICT + 0.02);

      // ---- scope
      scope.style.opacity = ctx.seg(p, SCOPE, SCOPE + 0.02);
      scope.style.color = `color-mix(in srgb, var(--ink) ${(100 * ctx.seg(p, SCOPE + 0.005, SCOPE + 0.02)).toFixed(0)}%, var(--dim))`;
    },
  });
})();
