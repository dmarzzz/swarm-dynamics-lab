// Scene: theseus50 (result 3 in the long cut). The fifty-member run of Swarm of Theseus.
// Source: 5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-POST-MORTEM.md
// ("Observed comparison"), its PLAN.md (the task), and the study README ("What changed from three to fifty members").
(function () {
  const COPY = {
    kicker: 'result 3',
    title: 'Swarm of Theseus',
    // PLAN.md: fifty positions; "every owner consults two witnesses"; "six cases per owner"
    job: 'the job: each of 50 agents decides 6 cases, after checking its 2 sources',
    learned: 'each founder learned which 2 sources to ask',     // post-mortem: "All 50 founders acquired correct private routes"
    founders: 50,
    replacedLabel: 'founders replaced',
    routesLabel: '50 of 50 routes kept',                        // "50/50 notes correct in each inherited arm"
    // static handover 297/300 (99.0%); README row "Written inheritance"
    hero: '99%', heroLabel: ['of decisions right with a', 'written note: 297 of 300'],
    // broken inheritance 166/300 (55.3%); README row "No inheritance". Universal-defer reference: 150/300.
    vs: '55%', vsLabel: ['nothing inherited: 166 of 300', '(always deferring: 150 of 300)'],
    // interactive predecessor handover 295/300; retained founders 298/300
    extra: ['talking to the predecessor instead: 295 of 300', 'founders kept, for comparison: 298 of 300'],
    claim: 'A written note carried the job through all 50 replacements.',
    // post-mortem: one world, one generation; "Correct memory did not prevent every unsafe action"; evidence 1/4
    limit: 'One synthetic world, one generation. Correct memory did not prevent every unsafe action.',
    footer: '50 agents / GPT-6 Sol / swarm-of-theseus S50, 1 world, 1,118 model calls / vishesh',
  };
  const NS = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const CX = 420, CY = 548, RAD = 200, N = COPY.founders;
  const pos = i => { const a = -Math.PI / 2 + i * 2 * Math.PI / N; return [CX + RAD * Math.cos(a), CY + RAD * Math.sin(a)]; };
  const SRC = i => [(i + 17) % N, (i + 33) % N];               // schematic routes: which two positions an agent asks (not the run's real graph)
  let dots = [], chords = [], focus = [], num, numL, routes, job, learned, hero, heroL, vs, vsL, extra, claim, limit;

  FILM.scene({
    id: 'theseus50',
    mount(root, ctx) {
      ctx.css(`
        #scene-theseus50 .t5 { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-theseus50 svg.t5ring { position:absolute; left:0; top:0; width:1920px; height:1080px; }
      `);
      const mk = (cls, style, html) => { const e = ctx.el('div', 't5 ' + cls, html || '', root); e.style.cssText += ';' + style; return e; };
      mk('f-kicker', 'left:100px;top:56px;font-size:22px;line-height:1', COPY.kicker);
      mk('f-title', 'left:100px;top:88px;font-family:var(--display)', COPY.title);
      job = mk('', 'left:100px;top:192px;font-size:28px;opacity:0', COPY.job);
      learned = mk('', 'left:100px;top:238px;font-size:24px;color:var(--dim);opacity:0', COPY.learned);
      const g = svg('svg', { class: 't5ring', viewBox: '0 0 1920 1080' }, root);
      for (let i = 0; i < N; i++) SRC(i).forEach(j => { const [x1, y1] = pos(i), [x2, y2] = pos(j);
        chords.push(svg('line', { x1, y1, x2, y2, stroke: 'var(--dim)', 'stroke-width': 1, opacity: 0 }, g)); });
      SRC(0).forEach(j => { const [x1, y1] = pos(0), [x2, y2] = pos(j);       // one agent's two sources, shown bright as the example
        focus.push(svg('line', { x1, y1, x2, y2, stroke: 'var(--amber)', 'stroke-width': 2.5, pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, g)); });
      for (let i = 0; i < N; i++) { const [x, y] = pos(i); dots.push(svg('circle', { cx: x.toFixed(1), cy: y.toFixed(1), r: 8, fill: 'var(--ink)', opacity: 0 }, g)); }
      num = mk('', `left:${CX - 300}px;top:${CY + RAD + 26}px;width:600px;text-align:center;font-size:26px;opacity:0`, '');
      numL = mk('', 'left:0;top:0;opacity:0', '');   // the label is part of the counter line now
      routes = mk('', `left:${CX - 300}px;top:${CY + RAD + 62}px;width:600px;text-align:center;font-size:24px;color:var(--zip);opacity:0`, COPY.routesLabel);
      hero = mk('f-num', 'left:900px;top:300px;font-size:150px;color:var(--amber);font-family:var(--display);opacity:0', COPY.hero);
      heroL = mk('', 'left:1290px;top:334px;font-size:28px;line-height:1.4;opacity:0', COPY.heroLabel.join('<br>'));
      vs = mk('f-num', 'left:900px;top:500px;font-size:150px;color:var(--no);font-family:var(--display);opacity:0', COPY.vs);
      vsL = mk('', 'left:1290px;top:534px;font-size:28px;line-height:1.4;opacity:0', COPY.vsLabel[0] + '<br><span style="color:var(--dim)">' + COPY.vsLabel[1] + '</span>');
      extra = mk('', 'left:900px;top:700px;font-size:24px;line-height:1.6;color:var(--dim);opacity:0', COPY.extra.join('<br>'));
      claim = mk('', 'left:100px;top:862px;font-size:34px;opacity:0', COPY.claim);
      limit = mk('', 'left:100px;top:920px;font-size:24px;color:var(--dim);opacity:0', COPY.limit);
      mk('', 'left:100px;top:978px;font-size:22px;color:var(--dim)', COPY.footer);
    },
    update(p, t, ctx) {
      const s = (a, b) => ctx.seg(p, a, b);
      // A: the institution and the job (0 .. 0.30)
      job.style.opacity = s(0.03, 0.07); learned.style.opacity = s(0.20, 0.25);
      const kept = s(0.50, 0.56);                                                  // routes survive the turnover: chords turn cyan
      focus.forEach((l, k) => { l.setAttribute('stroke-dashoffset', (1 - s(0.10 + k * 0.03, 0.16 + k * 0.03)).toFixed(3));
        l.setAttribute('opacity', (1 - s(0.27, 0.32)).toFixed(2)); });
      chords.forEach((l, k) => { const f = k / chords.length; l.setAttribute('opacity', (0.22 * s(0.18 + f * 0.08, 0.22 + f * 0.08)).toFixed(3));
        l.setAttribute('stroke', kept > 0.5 ? 'var(--zip)' : 'var(--dim)'); });
      // B: every founder is replaced, one after another (0.30 .. 0.46); cyan = a replacement, as in the pilot scene
      let replaced = 0;
      dots.forEach((d, i) => { const f = i / N, arrive = s(0.03 + f * 0.06, 0.06 + f * 0.06), sw = s(0.30 + f * 0.15, 0.32 + f * 0.15);
        if (sw >= 0.5) replaced++;
        const ex = i === 0 ? 1 - s(0.27, 0.32) : 0;                                 // the example agent is amber while its job is shown
        d.setAttribute('opacity', arrive);
        d.setAttribute('fill', sw >= 0.5 ? 'var(--zip)' : ex > 0.5 ? 'var(--amber)' : 'var(--ink)');
        d.setAttribute('r', (8 + 4 * Math.sin(Math.PI * sw) + 2 * ex).toFixed(1)); });
      num.textContent = replaced + ' of ' + N + ' ' + COPY.replacedLabel; num.style.opacity = s(0.29, 0.32);
      routes.style.opacity = kept;
      // C: the outcome (0.48 .. 0.88)
      const settle = s(0.66, 0.71);
      hero.style.opacity = s(0.50, 0.56); heroL.style.opacity = s(0.53, 0.59);
      hero.style.color = 'color-mix(in srgb, var(--amber) ' + Math.round((1 - settle) * 100) + '%, var(--zip))';
      vs.style.opacity = s(0.66, 0.72); vsL.style.opacity = s(0.69, 0.75);
      extra.style.opacity = s(0.84, 0.89);
      claim.style.opacity = s(0.88, 0.92); limit.style.opacity = s(0.92, 0.96);
    },
  });
})();
