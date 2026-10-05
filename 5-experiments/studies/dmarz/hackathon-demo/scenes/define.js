// Scene: define. What distributional safety is, against single-agent AI safety. Sits before the three questions.
(function () {
  const COPY = {
    kicker: 'definition',
    title: 'What is distributional safety?',
    left: { name: 'AI safety', says: 'aligning a single agent' },
    right: { name: 'Distributional safety', says: 'securing the properties of the swarm or market as a whole' },
    swarm: 110,   // dots in the illustration, not a result
  };
  const NS = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const LX = 520, RX = 1380, CY = 470, RING = 190;
  let one, oneRing, dots = [], swarmG, bigRing, divider, lt, rt;

  FILM.scene({
    id: 'define',
    mount(root, ctx) {
      ctx.css(`
        #scene-define .d-kicker { left:100px; top:56px; }
        #scene-define .d-title { left:100px; top:88px; }
        #scene-define svg { left:0; top:0; width:1920px; height:1080px; }
        #scene-define .d-text { top:720px; width:760px; text-align:center; opacity:0; }
        #scene-define .d-name { font-size:46px; line-height:1.2; margin-bottom:18px; white-space:nowrap; }
        #scene-define .d-says { font-size:32px; line-height:1.35; color:var(--ink); text-wrap:balance; }
        #scene-define .d-div { left:950px; top:250px; width:1px; height:640px; background:var(--dim); opacity:0; transform-origin:50% 0; }
      `);
      ctx.el('div', 'f-kicker d-kicker', COPY.kicker, root);
      ctx.el('div', 'f-title d-title', COPY.title, root);
      const g = svg('svg', { viewBox: '0 0 1920 1080' }, root);
      // left: one agent, one ring around it
      oneRing = svg('circle', { cx: LX, cy: CY, r: 64, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2.5, pathLength: 1,
        'stroke-dasharray': 1, 'stroke-dashoffset': 1, transform: `rotate(-90 ${LX} ${CY})` }, g);
      one = svg('circle', { cx: LX, cy: CY, r: 20, fill: 'var(--ink)', opacity: 0 }, g);
      // right: many agents, one ring around the whole
      swarmG = svg('g', {}, g);
      const golden = Math.PI * (3 - Math.sqrt(5)), c = 15;
      for (let j = 0; j < COPY.swarm; j++) { const r = c * Math.sqrt(j + 0.5), a = j * golden;
        dots.push(svg('circle', { cx: (RX + r * Math.cos(a)).toFixed(1), cy: (CY + r * Math.sin(a)).toFixed(1), r: 6.5, fill: 'var(--ink)', opacity: 0 }, swarmG)); }
      bigRing = svg('circle', { cx: RX, cy: CY, r: RING, fill: 'none', stroke: 'var(--amber)', 'stroke-width': 3, pathLength: 1,
        'stroke-dasharray': 1, 'stroke-dashoffset': 1, transform: `rotate(-90 ${RX} ${CY})` }, g);
      divider = ctx.el('div', 'd-div', '', root);
      lt = ctx.el('div', 'd-text', `<div class="d-name">${COPY.left.name}</div><div class="d-says">${COPY.left.says}</div>`, root);
      lt.style.left = (LX - 380) + 'px';
      rt = ctx.el('div', 'd-text', `<div class="d-name" style="color:var(--amber)">${COPY.right.name}</div><div class="d-says">${COPY.right.says}</div>`, root);
      rt.style.left = (RX - 380) + 'px';
    },
    update(p, t, ctx) {
      // left first: the agent, its ring, its words
      one.setAttribute('opacity', ctx.seg(p, 0.08, 0.14));
      oneRing.setAttribute('stroke-dashoffset', (1 - ctx.seg(p, 0.12, 0.26)).toFixed(3));
      lt.style.opacity = ctx.seg(p, 0.18, 0.28);
      divider.style.opacity = 0.4 * ctx.seg(p, 0.30, 0.38);
      divider.style.transform = `scaleY(${ctx.seg(p, 0.30, 0.42).toFixed(3)})`;
      // then the swarm fills from the centre out, and one ring closes around all of it
      const k = ctx.lin(p, 0.38, 0.62), shown = k * dots.length;
      for (let j = 0; j < dots.length; j++) dots[j].setAttribute('opacity', ctx.clamp(shown - j).toFixed(2));
      swarmG.setAttribute('transform', `rotate(${(t * 1.5).toFixed(2)} ${RX} ${CY})`);   // alive: a slow turn
      bigRing.setAttribute('stroke-dashoffset', (1 - ctx.seg(p, 0.58, 0.76)).toFixed(3));
      rt.style.opacity = ctx.seg(p, 0.64, 0.76);
    },
  });
})();
