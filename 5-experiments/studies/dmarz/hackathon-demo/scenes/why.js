// Scene: why. The problem the hackathon set, shown with the incident's own numbers. Designed for about 16 seconds.
// Sources (see ../INTRO-FACTS.md):
//   prompt: HACKATHON.md, "Theme and prompt, verbatim".
//   incident numbers: METR, "Brief independent investigation of agents' behavior, reasoning and collaboration in the
//   OpenAI / Hugging Face hacking incident", 2026-08-26, catalogued as 1-library/blogs/metr-2026-brief.md and re-read
//   from metr.org on 2026-10-04. Its summary sentence: "Roughly 1200 agents meant to be isolated from one another found
//   a way to communicate with one another on an unsanctioned message board, sending over 70,000 messages and files
//   during the investigation period. Of these agents, 700 went on to participate in the attack on Hugging Face."
//   Its data sources: "A set of ~1,300 transcripts with raw chains of thought, each containing the actions and
//   reasoning from a single agent run."
(function () {
  const COPY = {
    kicker: 'the problem',
    quote: '“Building the tools we wished we had for the Hugging Face incident.”',   // HACKATHON.md, verbatim
    quoteBy: 'the hackathon’s prompt',
    // 1 dot = 10 agents. METR: "Roughly 1200 agents meant to be isolated from one another" (1-library/blogs/metr-2026-brief.md)
    agents: { dots: 120, label: 'about 1,200 agents, meant to be isolated' },
    // 1 row = 10 transcripts. METR: "~1,300 transcripts ... each ... from a single agent run" (metr.org report, data sources)
    transcripts: { rows: 130, label: 'about 1,300 transcripts, one agent run each' },
    // 1 line = 1,000 messages. METR: "over 70,000 messages and files" (1-library/blogs/metr-2026-brief.md)
    messages: { links: 70, label: '70,000+ messages and files between them' },
    // 70 of the 120 dots. METR: "Of these agents, 700 went on to participate in the attack on Hugging Face"
    attack: { dots: 70, label: 'about 700 join an attack on Hugging Face' },
    close1: 'Our goal: recreate an incident like this in a lab.',
    close2: 'This lab is the start. It does not run the full swarm yet.',
    source: 'numbers: METR independent investigation, 26 Aug 2026 / 1 dot = 10 agents, 1 line = 1,000 messages, 1 row = 10 transcripts',
  };

  const NS = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const CX = 440, CY = 478, RING = 200;         // the group
  const TX = 1000, TY = 286, TW = 330, TGAP = 40, PITCH = 6;   // the transcripts, two columns of 65 rows
  let chars = [], by, dots = [], links = [], rows = [], swarmG, ring, order = [];
  let cAgents, cTrans, cMsg, cAttack, c1, c2, src;

  FILM.scene({
    id: 'why',
    mount(root, ctx) {
      ctx.css(`
        #scene-why .abs { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-why .w-kicker { left:100px; top:56px; }
        #scene-why .w-quote { left:100px; top:92px; font-size:40px; line-height:1.2; color:var(--ink); }
        #scene-why .w-quote span { opacity:0; }
        #scene-why .w-by { left:100px; top:152px; font-size:22px; color:var(--dim); opacity:0; }
        #scene-why svg { position:absolute; left:0; top:0; width:1920px; height:1080px; }
        #scene-why .w-cap { font-size:26px; line-height:1.3; color:var(--ink); opacity:0; }
        #scene-why .w-c1 { left:100px; top:832px; font-size:30px; color:var(--ink); opacity:0; }
        #scene-why .w-c2 { left:100px; top:882px; font-size:38px; color:var(--ink); opacity:0; }
        #scene-why .w-src { left:100px; top:982px; font-size:18px; color:var(--dim); opacity:0; }
      `);
      ctx.el('div', 'f-kicker abs w-kicker', COPY.kicker, root);
      const q = ctx.el('div', 'abs w-quote', '', root);
      for (const ch of COPY.quote) { const s = document.createElement('span'); s.textContent = ch; q.appendChild(s); chars.push(s); }
      by = ctx.el('div', 'abs w-by', COPY.quoteBy, root);

      const g = svg('svg', { viewBox: '0 0 1920 1080' }, root);
      swarmG = svg('g', {}, g);
      const rnd = ctx.rng(1204);
      // the agents: a disc of dots, filled from the centre out
      const golden = Math.PI * (3 - Math.sqrt(5)), c = 16, pts = [];
      for (let j = 0; j < COPY.agents.dots; j++) { const r = c * Math.sqrt(j + 0.5), a = j * golden;
        pts.push([CX + r * Math.cos(a), CY + r * Math.sin(a)]); }
      // the messages: 70 links, each between a dot and one of its nearer neighbours
      const linkG = svg('g', {}, swarmG);
      for (let k = 0; k < COPY.messages.links; k++) {
        const i = Math.floor(rnd() * pts.length);
        const near = pts.map((q2, j) => [Math.hypot(q2[0] - pts[i][0], q2[1] - pts[i][1]), j]).sort((a, b) => a[0] - b[0]);
        const j = near[2 + Math.floor(rnd() * 9)][1];
        links.push(svg('line', { x1: pts[i][0].toFixed(1), y1: pts[i][1].toFixed(1), x2: pts[j][0].toFixed(1), y2: pts[j][1].toFixed(1),
          stroke: 'var(--dim)', 'stroke-width': 1.4, opacity: 0 }, linkG));
      }
      for (const [x, y] of pts) dots.push(svg('circle', { cx: x.toFixed(1), cy: y.toFixed(1), r: 6, fill: 'var(--ink)', opacity: 0 }, swarmG));
      // which 70 dots join the attack, and in what order (seeded shuffle)
      order = pts.map((_, j) => j);
      for (let j = order.length - 1; j > 0; j--) { const k = Math.floor(rnd() * (j + 1)); [order[j], order[k]] = [order[k], order[j]]; }
      ring = svg('circle', { cx: CX, cy: CY, r: RING, fill: 'none', stroke: 'var(--amber)', 'stroke-width': 3, pathLength: 1,
        'stroke-dasharray': 1, 'stroke-dashoffset': 1, transform: `rotate(-90 ${CX} ${CY})` }, g);
      // the transcripts: one thin row of log marks per ten transcripts
      const per = Math.ceil(COPY.transcripts.rows / 2);
      for (let j = 0; j < COPY.transcripts.rows; j++) {
        const col = j < per ? 0 : 1, y = TY + (j % per) * PITCH, x0 = TX + col * (TW + TGAP);
        const rg = svg('g', { opacity: 0 }, g);
        let x = 0; const end = TW * (0.55 + 0.45 * rnd());
        while (end - x > 14) { const w = Math.min(end - x, 18 + rnd() * 70);
          svg('rect', { x: (x0 + x).toFixed(1), y, width: w.toFixed(1), height: 3, fill: 'var(--dim)' }, rg); x += w + 8; }
        rows.push(rg);
      }

      cAgents = ctx.el('div', 'abs w-cap', COPY.agents.label, root);
      cAgents.style.left = (CX - RING - 15) + 'px'; cAgents.style.top = '222px';
      cTrans = ctx.el('div', 'abs w-cap', COPY.transcripts.label, root);
      cTrans.style.left = TX + 'px'; cTrans.style.top = '222px';
      cMsg = ctx.el('div', 'abs w-cap', COPY.messages.label, root);
      cMsg.style.left = (CX - RING - 15) + 'px'; cMsg.style.top = '702px';
      cAttack = ctx.el('div', 'abs w-cap', COPY.attack.label, root);
      cAttack.style.left = (CX - RING - 15) + 'px'; cAttack.style.top = '744px'; cAttack.style.color = 'var(--no)';
      c1 = ctx.el('div', 'abs w-c1', COPY.close1, root);
      c2 = ctx.el('div', 'abs w-c2', COPY.close2, root);
      src = ctx.el('div', 'abs w-src', COPY.source, root);
    },
    update(p, t, ctx) {
      // the prompt, letter by letter
      const shown = Math.round(ctx.lin(p, 0.04, 0.16) * chars.length);
      for (let j = 0; j < chars.length; j++) chars[j].style.opacity = j < shown ? 1 : 0;
      by.style.opacity = ctx.seg(p, 0.15, 0.20);

      // the agents arrive, and one transcript row per ten of them arrives beside
      const k = ctx.lin(p, 0.21, 0.38);
      for (let j = 0; j < dots.length; j++) dots[j].setAttribute('opacity', ctx.clamp(k * dots.length - j).toFixed(2));
      for (let j = 0; j < rows.length; j++) rows[j].setAttribute('opacity', (0.85 * ctx.clamp(k * rows.length - j)).toFixed(2));
      const settle = 1 - 0.45 * ctx.seg(p, 0.76, 0.82);   // captions step back when the closing lines arrive
      cAgents.style.opacity = ctx.seg(p, 0.20, 0.25) * settle;
      cTrans.style.opacity = ctx.seg(p, 0.24, 0.29) * settle;

      // the messages between them
      const m = ctx.lin(p, 0.41, 0.54);
      for (let j = 0; j < links.length; j++) links[j].setAttribute('opacity', (0.8 * ctx.clamp(m * links.length - j)).toFixed(2));
      cMsg.style.opacity = ctx.seg(p, 0.41, 0.46) * settle;

      // about 700 of them turn to the attack; the ring closes around the group, where the incident was
      const a = ctx.lin(p, 0.56, 0.68) * COPY.attack.dots;
      for (let j = 0; j < order.length; j++) dots[order[j]].setAttribute('fill', j < a ? 'var(--no)' : 'var(--ink)');
      cAttack.style.opacity = ctx.seg(p, 0.56, 0.61) * settle;
      ring.setAttribute('stroke-dashoffset', (1 - ctx.seg(p, 0.64, 0.74)).toFixed(3));
      swarmG.setAttribute('transform', `rotate(${(t * 1.2).toFixed(2)} ${CX} ${CY})`);   // alive: a slow turn

      c1.style.opacity = ctx.seg(p, 0.77, 0.82);
      c2.style.opacity = ctx.seg(p, 0.83, 0.89);
      src.style.opacity = ctx.seg(p, 0.30, 0.36);
    },
  });
})();
