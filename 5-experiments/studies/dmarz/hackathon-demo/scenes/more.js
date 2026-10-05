// Scene: more (breadth). Ten further experiments, one card each, arriving one after another, then holding.
// Data: scenes/more.data.js, FILM.data.more.cards (claim, numbers, model, score, source per card; proofs in its comments).
(function () {
  const COPY = {
    kicker: 'the rest of the weekend',
    title: 'Ten more experiments',   // ten = FILM.data.more.cards.length
    // Totals. README.md (repo root) line 53: "118 study folders"; line 54: "153 cohorts, each with a stated claim, sample
    // sizes and a 0 to 4 evidence score"; lines 153-154: the weekend's runs "went ahead as exploratory studies".
    totals: '118 study folders, 153 cohorts in the evidence registry, all exploratory',
    evidence: (score) => 'evidence ' + score + ' of 4',   // evidence-metadata.json, 0 to 4 per cohort
  };

  // Layout (stage pixels): 5 x 2 grid inside x 100..1820, cards end at y 900, totals line under it (x < 1770 below y 940).
  const COLS = 5, X0 = 100, Y0 = 200, GAP = 20, CW = 328, CH = 340;
  // Beats, as fractions of the scene: first card at 4.5%, one card every 4% (0.6 s at 15 s), hold from about 48%.
  const FIRST = 0.045, STEP = 0.04;
  let R = {};

  FILM.scene({
    id: 'more',
    mount(root, ctx) {
      const cards = FILM.data['more'].cards;
      ctx.css(`
        #scene-more .abs { position:absolute; white-space:nowrap; }
        #scene-more .card { position:absolute; width:${CW}px; height:${CH}px; box-sizing:border-box; }
        #scene-more .edge { position:absolute; inset:0; box-sizing:border-box; border:1px solid var(--dim); }
        #scene-more .edge.hot { border-color:var(--amber); }
        #scene-more .claim { position:absolute; left:14px; right:10px; top:16px; font-family:var(--mono); font-size:26px;
          line-height:1.3; color:var(--ink); }
        #scene-more .nums { position:absolute; left:14px; right:10px; top:148px; font-family:var(--mono); font-size:20px;
          line-height:1.4; color:var(--dim); }
        #scene-more .foot { position:absolute; left:14px; right:10px; bottom:14px; font-family:var(--mono); font-size:18px;
          line-height:1.4; color:var(--dim); }
      `);
      const mk = (cls, style, html, parent) => {
        const e = ctx.el('div', cls, html || '', parent || root);
        if (style) e.style.cssText += ';' + style;
        return e;
      };
      R = { cards: [] };
      mk('f-kicker abs', 'left:100px;top:56px', COPY.kicker);
      mk('f-title abs', 'left:100px;top:88px', COPY.title);

      cards.forEach((c, i) => {
        const col = i % COLS, row = Math.floor(i / COLS);
        const box = mk('card', `left:${X0 + col * (CW + GAP)}px;top:${Y0 + row * (CH + GAP)}px`);
        const C = { box };
        C.edge = mk('edge', 'opacity:0', '', box);
        C.hot = mk('edge hot', 'opacity:0', '', box);
        C.claim = mk('claim', 'opacity:0', '', box); C.claim.textContent = c.claim;
        C.nums = mk('nums', 'opacity:0', '', box); C.nums.textContent = c.numbers;
        C.foot = mk('foot', 'opacity:0', '', box);
        ctx.el('div', '', '', C.foot).textContent = c.model;
        ctx.el('div', '', '', C.foot).textContent = COPY.evidence(c.score);
        R.cards.push(C);
      });

      R.totals = mk('abs', `left:100px;top:${Y0 + 2 * CH + GAP + 44}px;font-family:var(--mono);font-size:24px;line-height:1.3;color:var(--dim);opacity:0`, COPY.totals);
    },

    update(p, t, ctx) {
      const s = (a, b) => ctx.seg(p, a, b);
      const n = R.cards.length;
      R.cards.forEach((C, i) => {
        const a = FIRST + i * STEP;
        const arr = s(a, a + 0.03);                      // the outline arrives
        const cool = s(a + STEP - 0.014, a + STEP + 0.004);   // amber settles to dim just as the next card arrives
        C.box.style.transform = `translateY(${(1 - arr) * 12}px)`;
        C.edge.style.opacity = 0.55 * arr;
        C.hot.style.opacity = arr * (1 - cool);
        C.claim.style.opacity = s(a + 0.005, a + 0.035);
        C.nums.style.opacity = s(a + 0.02, a + 0.05);
        C.foot.style.opacity = s(a + 0.03, a + 0.06);
      });
      const end = FIRST + n * STEP;                      // last card has settled
      R.totals.style.opacity = s(end + 0.03, end + 0.07);
    },
  });
})();
