// Scene: twotheseus (experiment 2 of the two-experiment cut, ?film=two). A replay of the fifty-member run's public event
// log: the founders learn, the run forks into four arms, three replace every founder, and every arm decides its 300 cases.
// Data: scenes/twotheseus.data.js (built by scenes/twotheseus.build.py from S50-EVENTS.json).
// Stated numbers: 5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-POST-MORTEM.md
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
    call: (n, total) => 'call ' + String(n).padStart(4, '0') + ' of ' + total,
    idle: 'one institution // replay of the run’s recorded events',
    event: {
      founder: (pos, ok) => pos + ' // founder infers its 2 sources: ' + (ok ? 'correct' : 'wrong'),
      replacement: (pos, ok) => pos + ' // founder replaced, successor’s note: ' + (ok ? 'correct' : 'not correct'),
      selection: (pos, ok) => pos + ' // asks its sources: ' + (ok ? 'the right 2' : 'not the right 2'),
      decision: (pos, n, h) => pos + ' // decides 6 cases: ' + n + ' correct' + (h ? ', ' + h + ' harmful approval' + (h > 1 ? 's' : '') : ''),
    },
    // the five rings. "Observed comparison": static handover 297/300, interactive predecessor handover 295/300, broken
    // inheritance 166/300, retained founders 298/300; shared initial checkpoint 299/300. Universal-defer reference: 150/300.
    rings: [
      { key: 'common', label: 'the 50 founders', after: 'before any turnover' },
      { key: 'static', label: 'written note', total: 297 },
      { key: 'interactive', label: 'conversation', total: 295 },
      { key: 'broken', label: 'nothing inherited', total: 166, note: 'deferring every case scores 150' },
      { key: 'retained', label: 'control: founders kept', total: 298 },
    ],
    of: 'of 300',
    learnedCount: n => 'learned: ' + n + ' of 50',
    replacedCount: n => 'replaced: ' + n + ' of 50',
    legend: 'dot = one position: white founder, cyan successor, red outline = it has the wrong sources // 6 marks = its 6 decisions: white correct, red wrong',
    claim: ['With a note, successors finished 1 decision behind founders who were never replaced.',
      'A conversation showed no advantage over the note.'],
    // post-mortem: "Independent n=1 ... one replacement wave, one model configuration"; "The complete acquired knowledge fits in two
    // source identifiers"; "Eight approved a required record dated 11 when the current time was 10"
    limits: ['limits: 1 world, 1 replacement wave, 1 model // what had to survive was small: 2 source names per position',
      'even with the right sources, 8 decisions approved a record dated in the future'],
    footer: '50 agents / GPT-6 Sol / swarm-of-theseus S50, replay of 700 recorded events over 1,118 model calls, exploratory / vishesh',
  };

  // Cues: seconds into the narration clip at which each phrase starts (word timings of _out/vo-two/twotheseus.wav).
  // The scene adds the 0.25 s of silence that narrate.py puts before the voice. Re-time these when the clip changes.
  const CUE = {
    inst: 8.0, job: 12.4, learned: 18.3, infers: 20.4, fork: 23.0, replace: 26.5,
    arm: { static: 30.4, interactive: 35.8, broken: 39.9, retained: 46.8 }, num: { static: 32.6, interactive: 38.2, broken: 41.9, retained: 49.0 },
    defer: 43.3, claim: [50.4, 55.0], limits: [58.3, 65.6],
  };
  const LEAD = 0.25;

  const CX = [240, 620, 950, 1280, 1610], CY = 520, RAD = 86, PIP0 = 13, PIPD = 7.5, N = 50;
  let R = {}, D, C = {}, TRACKS = [];

  FILM.data.links = FILM.data.links || {};
  if (FILM.data.links.theseus50) FILM.data.links.twotheseus = FILM.data.links.theseus50;   // same result page as the theseus50 scene

  FILM.scene({
    id: 'twotheseus',
    mount(root, ctx) {
      D = FILM.data.twotheseus;
      ctx.css(`
        #scene-twotheseus .t5 { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-twotheseus canvas { position:absolute; left:0; top:0; }
        #scene-twotheseus .t5c { width:340px; text-align:center; }
      `);
      const mk = (cls, style, html) => { const e = ctx.el('div', 't5 ' + cls, html || '', root); e.style.cssText += ';' + style; return e; };
      R = { label: [], status: [], tally: [], note: [] };
      R.canvas = ctx.el('canvas', '', '', root); R.canvas.width = 1920; R.canvas.height = 1080; R.g = R.canvas.getContext('2d');
      const css = getComputedStyle(document.getElementById('film')), col = n => css.getPropertyValue(n).trim();
      C = { ink: col('--ink'), amber: col('--amber'), no: col('--no'), zip: col('--zip'), slot: 'rgba(127,136,150,.22)' };

      mk('f-kicker', 'left:100px;top:56px;font-size:22px;line-height:1', COPY.kicker);
      mk('f-title', 'left:100px;top:88px;font-family:var(--display)', COPY.title);
      R.question = mk('', 'left:100px;top:180px;font-size:28px;opacity:0', COPY.question);
      R.job = mk('', 'left:100px;top:228px;font-size:22px;opacity:0', COPY.job);
      R.learned = mk('', 'left:100px;top:262px;font-size:22px;color:var(--dim);opacity:0', COPY.learned);
      R.console = mk('', 'left:100px;top:308px;font-size:20px;color:var(--zip);opacity:0', '');
      COPY.rings.forEach((ring, i) => { const x = CX[i] - 170;
        R.label.push(mk('t5c', `left:${x}px;top:352px;font-size:22px;opacity:0`, ring.label));
        R.status.push(mk('t5c', `left:${x}px;top:672px;font-size:20px;color:var(--dim);opacity:0`, ''));
        R.tally.push(mk('t5c', `left:${x}px;top:702px;opacity:0`, '<span class="f-num" style="font-family:var(--display);font-size:52px"></span>' +
          '<span style="font-size:20px;color:var(--dim)"> ' + COPY.of + '</span>'));
        R.note.push(mk('t5c', `left:${x}px;top:760px;font-size:18px;color:var(--dim);opacity:0`, ring.after || ring.note || '')); });
      R.legend = mk('', 'left:100px;top:790px;font-size:18px;color:var(--dim);opacity:0', COPY.legend);
      R.claims = COPY.claim.map((c, i) => mk('', `left:100px;top:${826 + i * 38}px;font-size:26px;opacity:0`, c));
      R.limits = COPY.limits.map((c, i) => mk('', `left:100px;top:${908 + i * 28}px;font-size:20px;color:var(--dim);opacity:0`, c));
      mk('', 'left:100px;top:986px;font-size:20px;color:var(--dim)', COPY.footer);

      // The replay: which recorded events play in which window of the narration (seconds), ring by ring, in recorded order.
      const A = D.arms, ev = (ring, kind, list, from, to) => ({ ring, kind, list, from, to });
      TRACKS = [
        ev(0, 'founder', D.founder, CUE.infers, CUE.infers + 1.3),
        ev(0, 'selection', A.common.selection, CUE.infers + 1.3, CUE.infers + 1.7),
        ev(0, 'decision', A.common.decision, CUE.infers + 1.7, CUE.fork - 0.2),
        ev(1, 'replacement', A.static.replacement, CUE.replace, CUE.replace + 1.4),
        ev(2, 'replacement', A.interactive.replacement, CUE.replace + 0.1, CUE.replace + 1.5),
        ev(3, 'replacement', A.broken.replacement, CUE.replace + 0.2, CUE.replace + 1.6),
      ];
      [['static', 1], ['interactive', 2], ['broken', 3], ['retained', 4]].forEach(([k, i]) => {
        const a = CUE.arm[k] + 0.2, b = CUE.num[k] - 0.1;
        TRACKS.push(ev(i, 'selection', A[k].selection, a, a + (b - a) * 0.3), ev(i, 'decision', A[k].decision, a + (b - a) * 0.3, b)); });
    },
    update(p, t, ctx) {
      const tv = t - LEAD;                                                      // seconds into the narration
      const at = (cue, len) => ctx.ease(ctx.lin(tv, cue, cue + (len || 0.6)));
      const g = R.g; g.clearRect(0, 0, 1920, 1080);
      R.question.style.opacity = ctx.ease(ctx.lin(t, 0.5, 1.1));
      R.job.style.opacity = at(CUE.job); R.learned.style.opacity = at(CUE.learned);

      // state of every position in every ring, from the events played so far
      const S = COPY.rings.map(() => ({ succ: new Array(N).fill(0), route: new Array(N).fill(null), dec: new Array(N).fill(null), replaced: 0, sum: 0 }));
      let last = null, active = null;
      for (const tr of TRACKS) { if (tv < tr.from) continue;
        const done = Math.min(tr.list.length, Math.floor((tv - tr.from) / (tr.to - tr.from) * tr.list.length) + 1), st = S[tr.ring];
        for (let i = 0; i < done; i++) { const e = tr.list[i];
          if (tr.kind === 'founder') st.route[e[1]] = e[2];
          else if (tr.kind === 'replacement') { st.succ[e[1]] = 1; st.route[e[1]] = e[2]; st.replaced++; }
          else if (tr.kind === 'selection') st.route[e[1]] = e[2];
          else { st.dec[e[1]] = e[2]; st.sum += e[2]; } }
        if (tv <= tr.to + 0.05) active = { tr, e: tr.list[done - 1] };
        if (!last || tr.from >= last.tr.from) last = { tr, e: tr.list[done - 1] }; }
      // the arms start from the founders, who all learned their sources (the founder events, checked in the build script)
      for (let i = 1; i < 5; i++) for (let k = 0; k < N; k++) if (S[i].route[k] === null) S[i].route[k] = 1;

      // rings
      COPY.rings.forEach((ring, i) => {
        const inn = i === 0 ? at(CUE.inst, 0.5) : at(CUE.fork + (i - 1) * 0.25, 0.7), st = S[i], slots = at(CUE.job);
        R.label[i].style.opacity = inn; R.label[i].style.color = active && active.tr.ring === i ? 'var(--amber)' : 'var(--ink)';
        R.status[i].textContent = i === 0 ? COPY.learnedCount(st.route.filter(v => v === 1).length) : COPY.replacedCount(st.replaced);
        R.status[i].style.opacity = i === 0 ? at(CUE.infers) : at(CUE.replace - 0.3);
        const shown = i === 0 ? at(CUE.fork - 0.2, 0.4) : at(CUE.num[ring.key] - 0.1, 0.4);
        R.tally[i].firstChild.textContent = i === 0 ? st.sum : ring.total; R.tally[i].style.opacity = shown;
        R.tally[i].firstChild.style.color = ring.key === 'broken' ? 'var(--no)' : ring.key === 'static' || ring.key === 'interactive' ? 'var(--zip)' : 'var(--ink)';
        R.note[i].style.opacity = i === 0 ? shown : ring.note ? at(CUE.defer) : 0;
        if (inn <= 0) return;
        for (let k = 0; k < N; k++) { const a = -Math.PI / 2 + k * 2 * Math.PI / N, ca = Math.cos(a), sa = Math.sin(a);
          const arrive = i === 0 ? at(CUE.inst + k / N * 1.4, 0.6) : inn, x = CX[i] + RAD * ca, y = CY + RAD * sa;
          const known = st.route[k], wrong = known === 0;
          g.globalAlpha = arrive; g.lineWidth = 1.6; g.beginPath(); g.arc(x, y, 4.3, 0, 6.2832);
          if (known === 1) { g.fillStyle = st.succ[k] ? C.zip : C.ink; g.fill(); }
          else { g.strokeStyle = wrong ? C.no : C.ink; g.globalAlpha = arrive * (wrong ? 1 : 0.6); g.stroke(); }
          for (let j = 0; j < D.cases; j++) { const rr = RAD + PIP0 + j * PIPD;
            if (st.dec[k] === null) { g.globalAlpha = arrive * slots; g.fillStyle = C.slot; }
            else { g.globalAlpha = arrive; g.fillStyle = j < st.dec[k] ? C.ink : C.no; }
            g.beginPath(); g.arc(CX[i] + rr * ca, CY + rr * sa, 2.3, 0, 6.2832); g.fill(); } }
        if (active && active.tr.ring === i) { const k = active.e[1], a = -Math.PI / 2 + k * 2 * Math.PI / N;     // the position acting now
          g.globalAlpha = 1; g.strokeStyle = C.amber; g.lineWidth = 2.5; g.beginPath(); g.arc(CX[i] + RAD * Math.cos(a), CY + RAD * Math.sin(a), 8.5, 0, 6.2832); g.stroke(); }
        g.globalAlpha = 1;
      });

      // console: the last recorded event played
      const total = D.calls.toLocaleString('en-US');
      if (last) { const e = last.e, pos = 'position_' + String(e[1]).padStart(2, '0'), k = last.tr.kind, ring = COPY.rings[last.tr.ring];
        const what = k === 'decision' ? COPY.event.decision(pos, e[2], e[3]) : COPY.event[k](pos, e[2]);
        R.console.textContent = COPY.call(e[0], total) + ' // ' + ring.label + ' // ' + what; }
      else R.console.textContent = COPY.call(0, total) + ' // ' + COPY.idle;
      R.console.style.opacity = at(CUE.inst);
      R.legend.style.opacity = at(CUE.fork + 1.2);
      R.claims.forEach((c, i) => { c.style.opacity = at(CUE.claim[i]); });
      R.limits.forEach((c, i) => { c.style.opacity = at(CUE.limits[i]); });
    },
  });
})();
