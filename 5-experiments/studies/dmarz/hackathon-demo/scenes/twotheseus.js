// Scene: twotheseus (experiment 2 of the two-experiment cut, ?film=two). The fifty-member Swarm of Theseus run, told as
// a study: the question, the institution and the job, how the founders learned, the four arms, the limits.
// All numbers: 5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-POST-MORTEM.md
// ("Observed comparison") and its PLAN.md (the task and the design).
(function () {
  const COPY = {
    kicker: 'experiment 2 // continuity under turnover',
    title: 'Swarm of Theseus',
    question: 'Does what a group learned survive when every member is replaced?',
    // PLAN.md: fifty positions; "Every owner consults two witnesses"; "Six cases per owner"
    job: '50 positions, 6 cases each // a correct decision needs the 2 sources authoritative for that position',
    // PLAN.md: "Do not supply the authoritative pair"; each learning episode "supplies its observed outcome"
    learned: 'founders are not told which 2: each infers them from labelled episodes',
    founders: 50,
    replacedLabel: 'founders replaced',
    notesLabel: 'handover arms: 50 of 50 notes correct',          // "50/50 notes correct in each inherited arm, 0/50 in broken inheritance"
    armsHead: 'which handover carries it: correct decisions after turnover, of 300',
    // "Observed comparison": static handover 297/300, interactive predecessor handover 295/300, broken inheritance 166/300,
    // retained founders 298/300. Universal-defer reference: 150/300.
    arms: [
      { label: 'written note from the predecessor', n: 297, colour: 'var(--zip)' },
      { label: 'conversation with the predecessor', n: 295, colour: 'var(--zip)' },
      { label: 'nothing inherited', n: 166, colour: 'var(--no)' },
      { label: 'control: founders never replaced', n: 298, colour: 'var(--ink)' },
    ],
    of: 300,
    defer: { n: 150, label: 'deferring every case scores 150' },
    claim: ['With a note, successors finished 1 decision behind founders who were never replaced.',
      'A conversation showed no advantage over the note.'],
    // post-mortem: "Independent n=1 ... one replacement wave, one model configuration"; "The complete acquired knowledge fits in two
    // source identifiers"; "Eight approved a required record dated 11 when the current time was 10"
    limits: ['limits: 1 world, 1 replacement wave, 1 model // what had to survive was small: 2 source names per position',
      'even with the right sources, 8 decisions approved a record dated in the future'],
    footer: '50 agents / GPT-6 Sol / swarm-of-theseus S50, 1,118 model calls, exploratory / vishesh',
  };

  // Cues: seconds into the narration clip at which each phrase starts (word timings of _out/vo-two/twotheseus.wav).
  // The scene adds the 0.25 s of silence that narrate.py puts before the voice. Re-time these when the clip changes.
  const CUE = {
    inst: 8.0, job: 12.4, sources: 15.7, learned: 18.3, infers: 20.4, fork: 23.0, replace: 26.5,
    arm: [30.4, 35.8, 39.9, 46.8], num: [32.6, 38.2, 41.9, 49.0], defer: 43.3,
    claim: [50.4, 55.0], limits: [58.3, 65.6],
  };
  const LEAD = 0.25;

  const NS = 'http://www.w3.org/2000/svg';
  const svg = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const CX = 400, CY = 528, RAD = 168, N = COPY.founders;
  const pos = i => { const a = -Math.PI / 2 + i * 2 * Math.PI / N; return [CX + RAD * Math.cos(a), CY + RAD * Math.sin(a)]; };
  const SRC = i => [(i + 17) % N, (i + 33) % N];               // schematic routes: which two positions an agent asks (not the run's real graph)
  const AX = 860, AY = 386, AH = 94, BW = 600;                // arms table: left edge, first row, row pitch, bar length for 300 of 300
  let dots = [], chords = [], focus = [], question, job, learned, num, notes, head, rows = [], deferLine, deferL, claims = [], limits = [];

  FILM.data.links = FILM.data.links || {};
  if (FILM.data.links.theseus50) FILM.data.links.twotheseus = FILM.data.links.theseus50;   // same result page as the theseus50 scene

  FILM.scene({
    id: 'twotheseus',
    mount(root, ctx) {
      ctx.css(`
        #scene-twotheseus .t5 { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-twotheseus svg.t5ring { position:absolute; left:0; top:0; width:1920px; height:1080px; }
        #scene-twotheseus .t5bar { position:absolute; height:16px; }
      `);
      const mk = (cls, style, html) => { const e = ctx.el('div', 't5 ' + cls, html || '', root); e.style.cssText += ';' + style; return e; };
      mk('f-kicker', 'left:100px;top:56px;font-size:22px;line-height:1', COPY.kicker);
      mk('f-title', 'left:100px;top:88px;font-family:var(--display)', COPY.title);
      question = mk('', 'left:100px;top:184px;font-size:28px;opacity:0', COPY.question);
      job = mk('', 'left:100px;top:234px;font-size:24px;opacity:0', COPY.job);
      learned = mk('', 'left:100px;top:274px;font-size:24px;color:var(--dim);opacity:0', COPY.learned);

      const g = svg('svg', { class: 't5ring', viewBox: '0 0 1920 1080' }, root);
      for (let i = 0; i < N; i++) SRC(i).forEach(j => { const [x1, y1] = pos(i), [x2, y2] = pos(j);
        chords.push(svg('line', { x1, y1, x2, y2, stroke: 'var(--dim)', 'stroke-width': 1, opacity: 0 }, g)); });
      SRC(0).forEach(j => { const [x1, y1] = pos(0), [x2, y2] = pos(j);       // one agent's two sources, shown bright as the example
        focus.push(svg('line', { x1, y1, x2, y2, stroke: 'var(--amber)', 'stroke-width': 2.5, pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, g)); });
      for (let i = 0; i < N; i++) { const [x, y] = pos(i); dots.push(svg('circle', { cx: x.toFixed(1), cy: y.toFixed(1), r: 7, fill: 'var(--ink)', opacity: 0 }, g)); }
      num = mk('', `left:${CX - 300}px;top:${CY + RAD + 26}px;width:600px;text-align:center;font-size:24px;opacity:0`, '');
      notes = mk('', `left:${CX - 300}px;top:${CY + RAD + 60}px;width:600px;text-align:center;font-size:22px;color:var(--zip);opacity:0`, COPY.notesLabel);

      head = mk('', `left:${AX}px;top:${AY - 46}px;font-size:20px;letter-spacing:.06em;color:var(--dim);opacity:0`, COPY.armsHead);
      COPY.arms.forEach((a, i) => { const y = AY + i * AH;
        const label = mk('', `left:${AX}px;top:${y}px;font-size:24px;opacity:0`, a.label);
        const track = ctx.el('div', 't5bar', '', root); track.style.cssText += `;left:${AX}px;top:${y + 44}px;width:${BW}px;background:rgba(127,136,150,.16)`;
        const bar = ctx.el('div', 't5bar', '', root); bar.style.cssText += `;left:${AX}px;top:${y + 44}px;width:0`;
        const n = mk('f-num', `left:${AX + BW + 36}px;top:${y + 14}px;font-size:60px;font-family:var(--display);opacity:0`, String(a.n));
        const of = mk('', `left:${AX + BW + 156}px;top:${y + 36}px;font-size:22px;color:var(--dim);opacity:0`, 'of ' + COPY.of);
        rows.push({ a, label, track, bar, n, of }); });
      // the reference score, as a tick on every bar
      const dx = AX + BW * COPY.defer.n / COPY.of;
      deferLine = ctx.el('div', '', '', root); deferLine.style.cssText = 'position:absolute;left:0;top:0;opacity:0';
      COPY.arms.forEach((a, i) => { const k = ctx.el('div', '', '', deferLine);
        k.style.cssText = `position:absolute;left:${dx - 1}px;top:${AY + i * AH + 37}px;width:2px;height:30px;background:var(--bone)`; });
      deferL = mk('', `left:${dx - 180}px;top:${AY + AH * 3 + 74}px;width:360px;text-align:center;font-size:20px;color:var(--dim);opacity:0`, COPY.defer.label);

      COPY.claim.forEach((c, i) => claims.push(mk('', `left:100px;top:${806 + i * 42}px;font-size:28px;opacity:0`, c)));
      COPY.limits.forEach((c, i) => limits.push(mk('', `left:100px;top:${900 + i * 32}px;font-size:22px;color:var(--dim);opacity:0`, c)));
      mk('', 'left:100px;top:980px;font-size:20px;color:var(--dim)', COPY.footer);
    },
    update(p, t, ctx) {
      const at = (cue, len) => ctx.ease(ctx.lin(t, cue + LEAD, cue + LEAD + (len || 0.6)));
      question.style.opacity = ctx.ease(ctx.lin(t, 0.5, 1.1));
      job.style.opacity = at(CUE.job); learned.style.opacity = at(CUE.learned);
      const exampleOff = at(CUE.fork - 0.8), kept = at(CUE.arm[0]);              // notes survive the turnover: chords turn cyan
      focus.forEach((l, k) => { l.setAttribute('stroke-dashoffset', (1 - at(CUE.sources + k * 0.5, 0.9)).toFixed(3));
        l.setAttribute('opacity', (1 - exampleOff).toFixed(2)); });
      chords.forEach((l, k) => { const f = k / chords.length; l.setAttribute('opacity', (0.22 * at(CUE.infers + f * 1.6, 0.8)).toFixed(3));
        l.setAttribute('stroke', kept > 0.5 ? 'var(--zip)' : 'var(--dim)'); });
      let replaced = 0;
      dots.forEach((d, i) => { const f = i / N, arrive = at(CUE.inst + f * 1.6, 0.7), sw = at(CUE.replace + f * 1.9, 0.5);
        if (sw >= 0.5) replaced++;
        const ex = i === 0 ? at(CUE.job) * (1 - exampleOff) : 0;                 // the example agent is amber while its job is shown
        d.setAttribute('opacity', arrive);
        d.setAttribute('fill', sw >= 0.5 ? 'var(--zip)' : ex > 0.5 ? 'var(--amber)' : 'var(--ink)');
        d.setAttribute('r', (7 + 3.5 * Math.sin(Math.PI * sw) + 2 * ex).toFixed(1)); });
      num.textContent = replaced + ' of ' + N + ' ' + COPY.replacedLabel; num.style.opacity = at(CUE.replace - 0.3);
      notes.style.opacity = kept;

      head.style.opacity = at(CUE.fork);
      rows.forEach((r, i) => {
        const shown = at(CUE.fork + 0.4 + i * 0.35), grow = at(CUE.num[i] - 0.5, 1.3);
        const next = i + 1 < rows.length ? CUE.arm[i + 1] : CUE.claim[0];
        const active = at(CUE.arm[i], 0.4) * (1 - at(next, 0.5));                // the arm being read is the one amber signal
        const colour = 'color-mix(in srgb, var(--amber) ' + Math.round(active * 100) + '%, ' + r.a.colour + ')';
        r.label.style.opacity = shown * (0.55 + 0.45 * at(CUE.arm[i], 0.4)); r.track.style.opacity = shown;
        r.bar.style.width = (BW * r.a.n / COPY.of * grow).toFixed(1) + 'px'; r.bar.style.background = colour;
        r.n.style.color = colour;                                                // the count is shown whole, never part-way
        r.n.style.opacity = at(CUE.num[i] - 0.5, 0.4); r.of.style.opacity = at(CUE.num[i] - 0.5, 0.4);
      });
      deferLine.style.opacity = at(CUE.defer); deferL.style.opacity = at(CUE.defer);
      claims.forEach((c, i) => { c.style.opacity = at(CUE.claim[i]); });
      limits.forEach((c, i) => { c.style.opacity = at(CUE.limits[i]); });
    },
  });
})();
