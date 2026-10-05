// Scene: twoclose (closing card of the two-experiment cut, ?film=two). What each experiment measured and how far it goes,
// then where the lab is. The repo QR is the one scenes/next.js draws (FILM.data.repoQr), so this file must load after it.
(function () {
  const COPY = {
    kicker: 'how far these two results go',
    head: 'both outcomes are measured at the level of the group',
    // sybil-rules-180/RESULTS.md: primary endpoint = fraction of owners with sustained masking; two economies of 180 owners.
    // S50-POST-MORTEM.md: primary endpoint = correct decisions among the 300 assigned terminal cases per arm; 1 world, one generation.
    rows: [
      { n: '1', name: 'Thou shalt not split', what: 'how many owners in an economy split', scope: '2 economies of 180 agents' },
      { n: '2', name: 'Swarm of Theseus', what: 'how many decisions stay correct after its members change', scope: '1 world of 50 agents, 1 replacement wave' },
    ],
    both: 'both exploratory // one model, GPT-6 Sol',     // RESULTS.md "Exploratory"; S50 evidence_confidence 1/4; both gpt-6-sol
    lab: 'Swarm Dynamics Lab',
    open: 'The lab is open source, from the prompts to the infrastructure as code.',
    siteLabel: 'site',
    site: 'www.swarmsafety.org',                       // the bare domain did not resolve on 2026-10-05 (UTC); www did
    codeLabel: 'code + data',
    code: 'github.com/dmarzzz/swarm-dynamics-lab',
    qrNote: 'scan for the repo',
    by: 'made by dmarz, vishesh and shadow',           // the hackathon team, scenes/team.js
  };
  // Cues: seconds into the narration clip at which each phrase starts (word timings of _out/vo-two/twoclose.wav); the scene
  // adds the 0.25 s of silence before the voice.
  const CUE = { head: 0.0, what: [2.4, 4.4], both: 8.3, scope: [13.2, 15.4], lab: 17.3, labEnd: 18.6, open: 18.9, qr: 19.3, code: 19.9, site: 21.2, by: 23.0 };
  const LEAD = 0.25;
  let head, rows = [], both, chars = [], cursor, open, site, code, qr, qrNote, by;

  FILM.scene({
    id: 'twoclose',
    mount(root, ctx) {
      ctx.css(`
        #scene-twoclose .tc { position:absolute; white-space:nowrap; font-family:var(--mono); }
        #scene-twoclose .tc-head { left:100px; font-size:22px; line-height:1; letter-spacing:.12em; text-transform:uppercase; color:var(--dim); opacity:0; }
        #scene-twoclose .tc-row { left:100px; font-size:30px; line-height:1; color:var(--ink); opacity:0; }
        #scene-twoclose .tc-row i { font-style:normal; color:var(--dim); display:inline-block; width:56px; }
        #scene-twoclose .tc-row b { font-weight:400; display:inline-block; width:480px; }
        #scene-twoclose .tc-scope { left:636px; font-size:22px; line-height:1; color:var(--dim); opacity:0; }
        #scene-twoclose .tc-lab { left:96px; top:446px; font-family:var(--display); font-weight:var(--text-display-weight); font-size:104px; line-height:1; }
        #scene-twoclose .tc-lab span { opacity:0; }
        #scene-twoclose .tc-cursor { position:absolute; top:458px; width:10px; height:80px; background:var(--amber); opacity:0; }
        #scene-twoclose .tc-open { left:100px; top:584px; font-size:28px; line-height:1.4; color:var(--ink); opacity:0; }
        #scene-twoclose .tc-link { left:100px; opacity:0; }
        #scene-twoclose .tc-link .u { font-size:44px; line-height:1; margin-top:14px; color:var(--ink); }
        #scene-twoclose .tc-qr { position:absolute; left:1464px; top:548px; width:356px; height:356px; background:var(--bone); padding:38px; opacity:0; }
        #scene-twoclose .tc-qr svg { display:block; width:280px; height:280px; }
        #scene-twoclose .tc-qrnote { left:1464px; top:920px; opacity:0; }
        #scene-twoclose .tc-by { left:100px; top:950px; font-size:22px; line-height:1; color:var(--dim); opacity:0; }
      `);
      const mk = (cls, html) => ctx.el('div', 'tc ' + cls, html || '', root);
      const k = mk('f-kicker', COPY.kicker); k.style.cssText += ';left:100px;top:56px;font-size:22px;line-height:1';
      head = mk('tc-head', COPY.head); head.style.top = '112px';
      COPY.rows.forEach((r, i) => {
        const row = mk('tc-row', `<i>${r.n}</i><b>${r.name}</b><span>${r.what}</span>`); row.style.top = (170 + i * 92) + 'px';
        const scope = mk('tc-scope', r.scope); scope.style.top = (214 + i * 92) + 'px';
        rows.push({ row, what: row.lastChild, scope });
      });
      both = mk('tc-head', COPY.both); both.style.top = '366px';
      const lab = mk('tc-lab', '');
      for (const ch of COPY.lab) chars.push(ctx.el('span', '', ch === ' ' ? '&nbsp;' : ch, lab));
      cursor = ctx.el('div', 'tc-cursor', '', root);
      open = mk('tc-open', COPY.open);
      site = mk('tc-link', `<div class="f-small">${COPY.siteLabel}</div><div class="u">${COPY.site}</div>`); site.style.top = '676px';
      code = mk('tc-link', `<div class="f-small">${COPY.codeLabel}</div><div class="u">${COPY.code}</div>`); code.style.top = '808px';
      qr = ctx.el('div', 'tc-qr', FILM.data.repoQr ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 33 33" shape-rendering="crispEdges">' +
        '<path stroke="#03050a" stroke-width="1" fill="none" d="' + FILM.data.repoQr + '"/></svg>' : '', root);
      qrNote = mk('f-small tc-qrnote', COPY.qrNote);
      by = mk('tc-by', COPY.by);
    },
    update(p, t, ctx) {
      const at = (cue, len) => ctx.ease(ctx.lin(t, cue + LEAD, cue + LEAD + (len || 0.6)));
      head.style.opacity = at(CUE.head + 0.2);
      rows.forEach((r, i) => { r.row.style.opacity = at(CUE.what[i] - 0.3); r.what.style.opacity = at(CUE.what[i]); r.scope.style.opacity = at(CUE.scope[i]); });
      both.style.opacity = at(CUE.both);
      const shown = Math.floor(ctx.lin(t, CUE.lab + LEAD, CUE.labEnd + LEAD) * chars.length);
      chars.forEach((c, i) => { c.style.opacity = i < shown ? 1 : 0; });
      const last = chars[Math.min(shown, chars.length) - 1];
      cursor.style.left = (96 + (last ? last.offsetLeft + last.offsetWidth : 0) + 8) + 'px';
      cursor.style.opacity = t >= CUE.lab + LEAD && t < CUE.labEnd + LEAD + 0.5 ? 1 : 0;
      open.style.opacity = at(CUE.open);
      site.style.opacity = at(CUE.site); code.style.opacity = at(CUE.code);
      const kq = FILM.data.repoQr ? at(CUE.qr, 1.4) : 0;
      qr.style.opacity = kq > 0 ? 1 : 0;
      qr.style.clipPath = 'inset(0 0 ' + ((1 - kq) * 100).toFixed(2) + '% 0)';
      qrNote.style.opacity = at(CUE.qr + 1.2);
      by.style.opacity = at(CUE.by);
    },
  });
})();
