// Scene: twoclose (closing card of the two-experiment cut, ?film=two). How far the two results go, then where the lab is.
// The repo QR is the one scenes/next.js draws (FILM.data.repoQr), so this file must load after it.
(function () {
  const COPY = {
    kicker: 'how far these two results go',
    // sybil-rules-180/RESULTS.md: "Exploratory", gpt-6-sol, two economies of 180 owners (first economy and replication R1).
    // S50-POST-MORTEM.md: "1 synthetic world", "one generation", GPT-6 Sol, evidence_confidence 1/4.
    head: 'both exploratory // one model, GPT-6 Sol',
    rows: [
      { n: '1', name: 'Thou shalt not split', scope: '2 economies of 180 agents' },
      { n: '2', name: 'Swarm of Theseus', scope: '1 world of 50 agents, 1 generation' },
    ],
    lab: 'Swarm Dynamics Lab',
    open: 'The lab is open source, from the prompts to the infrastructure as code.',
    siteLabel: 'site',
    site: 'www.swarmsafety.org',                       // the bare domain did not resolve on 2026-10-05 (UTC); www did
    codeLabel: 'code + data',
    code: 'github.com/dmarzzz/swarm-dynamics-lab',
    qrNote: 'scan for the repo',
    by: 'made by dmarz, vishesh and shadow',           // the hackathon team, scenes/team.js
  };
  const B = {
    head: [0.03, 0.07], row: [[0.26, 0.31], [0.37, 0.42]],
    lab: [0.52, 0.60], open: [0.58, 0.64], qr: [0.60, 0.70], code: [0.63, 0.68], site: [0.73, 0.77], by: [0.80, 0.85],
  };
  let head, rows = [], chars = [], cursor, open, site, code, qr, qrNote, by;

  FILM.scene({
    id: 'twoclose',
    mount(root, ctx) {
      ctx.css(`
        #scene-twoclose .tc { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-twoclose .tc-head { left:100px; top:112px; font-size:22px; line-height:1; letter-spacing:.12em; text-transform:uppercase; color:var(--dim); opacity:0; }
        #scene-twoclose .tc-row { left:100px; font-size:32px; line-height:1; color:var(--ink); opacity:0; }
        #scene-twoclose .tc-row i { font-style:normal; color:var(--dim); display:inline-block; width:56px; }
        #scene-twoclose .tc-row b { font-weight:400; display:inline-block; width:520px; }
        #scene-twoclose .tc-lab { left:96px; top:392px; font-family:var(--display); font-weight:var(--text-display-weight); font-size:104px; line-height:1; }
        #scene-twoclose .tc-lab span { opacity:0; }
        #scene-twoclose .tc-cursor { position:absolute; top:404px; width:10px; height:80px; background:var(--amber); opacity:0; }
        #scene-twoclose .tc-open { left:100px; top:540px; font-size:28px; line-height:1.4; color:var(--ink); opacity:0; }
        #scene-twoclose .tc-link { left:100px; opacity:0; }
        #scene-twoclose .tc-link .u { font-size:44px; line-height:1; margin-top:14px; color:var(--ink); }
        #scene-twoclose .tc-qr { position:absolute; left:1464px; top:520px; width:356px; height:356px; background:var(--bone); padding:38px; opacity:0; }
        #scene-twoclose .tc-qr svg { display:block; width:280px; height:280px; }
        #scene-twoclose .tc-qrnote { left:1464px; top:896px; opacity:0; }
        #scene-twoclose .tc-by { left:100px; top:944px; font-size:22px; line-height:1; color:var(--dim); opacity:0; }
      `);
      const mk = (cls, html) => ctx.el('div', 'tc ' + cls, html || '', root);
      const k = mk('f-kicker', COPY.kicker); k.style.cssText += ';left:100px;top:56px;font-size:22px;line-height:1';
      head = mk('tc-head', COPY.head);
      COPY.rows.forEach((r, i) => { const row = mk('tc-row', `<i>${r.n}</i><b>${r.name}</b>${r.scope}`); row.style.top = (186 + i * 64) + 'px'; rows.push(row); });
      const lab = mk('tc-lab', '');
      for (const ch of COPY.lab) chars.push(ctx.el('span', '', ch === ' ' ? '&nbsp;' : ch, lab));
      cursor = ctx.el('div', 'tc-cursor', '', root);
      open = mk('tc-open', COPY.open);
      site = mk('tc-link', `<div class="f-small">${COPY.siteLabel}</div><div class="u">${COPY.site}</div>`); site.style.top = '650px';
      code = mk('tc-link', `<div class="f-small">${COPY.codeLabel}</div><div class="u">${COPY.code}</div>`); code.style.top = '790px';
      qr = ctx.el('div', 'tc-qr', FILM.data.repoQr ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 33 33" shape-rendering="crispEdges">' +
        '<path stroke="#03050a" stroke-width="1" fill="none" d="' + FILM.data.repoQr + '"/></svg>' : '', root);
      qrNote = mk('f-small tc-qrnote', COPY.qrNote);
      by = mk('tc-by', COPY.by);
    },
    update(p, t, ctx) {
      head.style.opacity = ctx.seg(p, B.head[0], B.head[1]);
      rows.forEach((r, i) => { r.style.opacity = ctx.seg(p, B.row[i][0], B.row[i][1]); });
      const k = ctx.lin(p, B.lab[0], B.lab[1]) * chars.length, shown = Math.floor(k);
      chars.forEach((c, i) => { c.style.opacity = i < shown ? 1 : 0; });
      const last = chars[Math.min(shown, chars.length) - 1];
      cursor.style.left = (96 + (last ? last.offsetLeft + last.offsetWidth : 0) + 8) + 'px';
      cursor.style.opacity = p >= B.lab[0] && p < B.lab[1] + 0.03 ? 1 : 0;
      open.style.opacity = ctx.seg(p, B.open[0], B.open[1]);
      site.style.opacity = ctx.seg(p, B.site[0], B.site[1]);
      code.style.opacity = ctx.seg(p, B.code[0], B.code[1]);
      const kq = FILM.data.repoQr ? ctx.seg(p, B.qr[0], B.qr[1]) : 0;
      qr.style.opacity = kq > 0 ? 1 : 0;
      qr.style.clipPath = 'inset(0 0 ' + ((1 - kq) * 100).toFixed(2) + '% 0)';
      qrNote.style.opacity = ctx.seg(p, B.qr[1] - 0.03, B.qr[1]);
      by.style.opacity = ctx.seg(p, B.by[0], B.by[1]);
    },
  });
})();
