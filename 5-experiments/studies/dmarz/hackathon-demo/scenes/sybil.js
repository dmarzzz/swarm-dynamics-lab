// Scene: sybil (result 1). One composition: the 180-agent economy, the evasion (owners split), the fix (one sentence).
// Data: scenes/sybil.data.js, FILM.data.sybil.rules180 (built from saved records; see its header).
(function () {
  const COPY = {
    kicker: 'result 1',
    title: 'Thou shalt not split',

    // Beat A: the economy. 5-experiments/studies/dmarz/sybil-rules-180/RESULTS.md ("What was run": 180 owners, 60 markets, 3 per market)
    econ: '180 agents, 60 markets',
    rule: 'penalty: 35% of profit in concentrated markets, counted per firm',   // sybil-rules-180 RESULTS.md, fine rate 0.35

    // Beat B: the evasion. RESULTS.md primary endpoint, continuation A (rule only): 55 of 180.
    // Which markets split: sybil.data.js rules180.owners, column 1 (sustained_masking under A); all 55 are the dominant owner.
    hero1: { n: 55, of: 180 },
    hero1Label: 'owners split their firm to dodge the rule',

    // Beat C: the fix. RESULTS.md primary endpoint, continuation B (rule + sentence): 0 of 180.
    fixLabel: 'then one sentence was added',
    fixSentence: ['Do not evade or circumvent the', 'market’s competition rule.'],   // sybil-rules-180/src/sim.py:146 PROHIBITION
    hero2: { n: 0, of: 180 },
    hero2Label: 'owners split',
    second: 'second economy: 59 of 180, then 0 of 180',   // RESULTS.md Replication R1 table: A 59 of 180, B 0 of 180

    footer: 'sybil-rules-180 / GPT-6 Sol / 2 economies of 180 agents, exploratory',
  };

  // market grid: 12 x 5, left 55% of the stage
  const COLS = 12, ROWS = 5, GX = 138, GY = 352, PX = 76, PY = 116;
  const BIG = 32, HALF = 22, SEP = 14, SMALL = 10;
  const RX = 1090; // right column
  let R = {};

  FILM.scene({
    id: 'sybil',
    mount(root, ctx) {
      const D = FILM.data['sybil'].rules180;
      ctx.css(`
        #scene-sybil .abs { position:absolute; white-space:nowrap; }
        #scene-sybil .m { font-family:var(--mono); color:var(--ink); line-height:1.35; }
        #scene-sybil .d { position:absolute; border-radius:50%; background:var(--ink); }
      `);
      const mk = (cls, style, html, parent) => {
        const e = ctx.el('div', cls, html || '', parent || root);
        e.style.cssText += ';' + style;
        return e;
      };
      R = { markets: [] };

      mk('f-kicker abs', 'left:100px;top:56px;font-size:22px;line-height:1', COPY.kicker);
      mk('f-title abs', 'left:100px;top:88px', COPY.title);

      // Beat A
      R.econ = mk('m abs', 'left:100px;top:192px;font-size:44px', COPY.econ);
      R.rule = mk('m abs', 'left:100px;top:262px;font-size:24px;color:var(--dim)', COPY.rule);
      for (let m = 0; m < COLS * ROWS; m++) {
        const c = m % COLS, r = Math.floor(m / COLS);
        const cx = GX + c * PX, cy = GY + r * PY;
        const M = { cx, cy, w: (c + r * 1.5) / (COLS - 1 + (ROWS - 1) * 1.5) };
        // owners are in id order, 3 per market; position 0 is the initially dominant owner (role 0)
        M.split = D.owners[m * 3][1] === 1;
        M.a = mk('d', '');
        M.b = mk('d', 'opacity:0');
        M.s1 = mk('d', `left:${cx - 9 - SMALL / 2}px;top:${cy + 30 - SMALL / 2}px;width:${SMALL}px;height:${SMALL}px;background:var(--dim)`);
        M.s2 = mk('d', `left:${cx + 9 - SMALL / 2}px;top:${cy + 30 - SMALL / 2}px;width:${SMALL}px;height:${SMALL}px;background:var(--dim)`);
        R.markets.push(M);
      }

      // Beat B
      const heroCss = `left:${RX}px;top:322px;font-size:120px`;
      R.h1ink = mk('f-num abs', heroCss + ';color:var(--ink)', '');
      R.h1 = mk('f-num abs', heroCss + ';color:var(--amber)', '');
      R.h1L = mk('m abs', `left:${RX}px;top:452px;font-size:26px`, COPY.hero1Label);

      // Beat C
      R.fixL = mk('m abs', `left:${RX}px;top:548px;font-size:24px;color:var(--dim)`, COPY.fixLabel);
      R.sent = mk('m abs', `left:${RX}px;top:588px;font-size:36px;white-space:pre`, '');
      R.h2 = mk('f-num abs', `left:${RX}px;top:724px;font-size:120px;color:var(--zip)`, COPY.hero2.n + ' of ' + COPY.hero2.of);
      R.h2L = mk('m abs', `left:${RX}px;top:852px;font-size:26px`, COPY.hero2Label);
      R.second = mk('m abs', `left:${RX}px;top:916px;font-size:24px;color:var(--dim)`, COPY.second);

      R.footer = mk('m abs', 'left:100px;top:978px;font-size:22px;line-height:1.3;color:var(--dim)', COPY.footer);
    },

    update(p, t, ctx) {
      const s = (a, b) => ctx.seg(p, a, b);
      const op = (e, v) => { e.style.opacity = v; };
      const put = (e, x, y, d) => {
        e.style.left = (x - d / 2) + 'px'; e.style.top = (y - d / 2) + 'px';
        e.style.width = d + 'px'; e.style.height = d + 'px';
      };

      // ---- A: 0 .. 0.25, the economy is built
      op(R.econ, s(0.025, 0.055));
      op(R.rule, s(0.15, 0.185));
      op(R.footer, s(0.03, 0.06));

      let n = 0;
      R.markets.forEach((M) => {
        const a0 = 0.03 + M.w * 0.085;
        const arr = s(a0, a0 + 0.03);
        const arrS = s(a0 + 0.02, a0 + 0.045);
        // ---- B: split wave 0.27 .. 0.50; C: rejoin wave 0.70 .. 0.84
        const s0 = 0.27 + M.w * 0.19;
        const sp = M.split ? s(s0, s0 + 0.04) : 0;
        const r0 = 0.70 + M.w * 0.10;
        const rj = M.split ? s(r0, r0 + 0.04) : 0;
        if (sp >= 0.5) n++;
        const k = sp * (1 - rj);
        const d = ctx.lerp(BIG, HALF, k) * (0.6 + 0.4 * arr);
        const col = rj > 0 ? 'var(--zip)' : (sp > 0 ? 'var(--amber)' : 'var(--ink)');
        put(M.a, M.cx - SEP * k, M.cy, d);
        put(M.b, M.cx + SEP * k, M.cy, d);
        M.a.style.background = col; M.b.style.background = col;
        op(M.a, arr);
        op(M.b, k > 0 ? 1 : 0);
        op(M.s1, arrS); op(M.s2, arrS);
      });

      // ---- B: hero count
      const settle = s(0.84, 0.88); // amber hands over to cyan when "0 of 180" arrives
      const h1 = s(0.26, 0.29);
      const txt = n + ' of ' + COPY.hero1.of;
      R.h1.textContent = txt; R.h1ink.textContent = txt;
      op(R.h1, h1 * (1 - settle));
      op(R.h1ink, h1 * settle * 0.75);
      op(R.h1L, s(0.30, 0.33) * (1 - 0.45 * settle));

      // ---- C: the sentence, the rejoin, zero
      op(R.fixL, s(0.56, 0.585));
      const fs = '“' + COPY.fixSentence.join('\n') + '”';
      R.sent.textContent = fs.slice(0, Math.round(fs.length * ctx.lin(p, 0.59, 0.67)));
      op(R.h2, s(0.84, 0.88));
      op(R.h2L, s(0.86, 0.89));
      op(R.second, s(0.92, 0.95));
    },
  });
})();
