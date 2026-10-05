// Scene: team (opening card). Team name, event, three teammates, repo.
(function () {
  const COPY = {
    event: 'AI Village x Grove Research / AI Swarm Dynamics Hackathon / Oct 3-4 2026',
    team: 'Swarm of Theseus',
    site: 'swarmsafety.org',
    repo: 'github.com/dmarzzz/swarm-dynamics-lab',
    scan: 'scan to follow',
    // Handles: GitHub login = the account that commits to dmarzzz/swarm-lab (gh api repos/dmarzzz/swarm-lab/contributors).
    // X handle = the twitter_username on that GitHub profile (gh api users/<login>). Set x: null to hide the line.
    people: [
      { name: 'dmarz', img: 'team/dmarz.png', github: 'dmarzzz', x: 'DistributedMarz' },
      { name: 'vishesh', img: 'team/vishesh.png', github: 'cytonomy', x: 'visavishesh' },
      { name: 'shadow', img: 'team/shadow.png', github: 'wakesync', x: '0xShadow' },
    ],
  };

  // Beats, as fractions of the scene.
  const B = {
    nameIn: [0.10, 0.34],          // team name types on
    people: [0.40, 0.52, 0.64],    // each avatar arrives
    personLen: 0.12,
    repo: [0.80, 0.90],
  };

  let chars = [], cursor, cards = [], repo;

  FILM.scene({
    id: 'team',
    mount(root, ctx) {
      ctx.css(`
        #scene-team .tm-event { position:absolute; left:100px; top:56px; white-space:nowrap; }
        #scene-team .tm-name { position:absolute; left:94px; top:196px; font-family:var(--display); font-weight:var(--text-display-weight);
          font-size:164px; line-height:1; color:var(--ink); white-space:nowrap; letter-spacing:0; }
        #scene-team .tm-name span { opacity:0; }
        #scene-team .tm-cursor { position:absolute; top:214px; width:14px; height:128px; background:var(--amber); opacity:0; }
        #scene-team .tm-card { position:absolute; top:452px; width:560px; height:420px; opacity:0; }
        #scene-team .tm-card img { position:absolute; left:0; top:0; width:200px; height:200px; object-fit:cover;
          display:block; filter:saturate(0.85); }
        #scene-team .tm-frame { position:absolute; left:-7px; top:-7px; width:212px; height:212px;
          border:1px solid var(--dim); box-sizing:border-box; }
        #scene-team .tm-who { position:absolute; left:232px; top:22px; font-family:var(--mono); white-space:nowrap; }
        #scene-team .tm-who .n { font-size:40px; line-height:1.1; color:var(--ink); margin-bottom:26px; }
        #scene-team .tm-who .h { font-size:22px; line-height:1.7; color:var(--dim); }
        #scene-team .tm-qr { position:absolute; left:0; top:244px; width:168px; height:168px; background:var(--bone); }
        #scene-team .tm-qr svg { position:absolute; left:0; top:0; width:168px; height:168px; display:block; }
        #scene-team .tm-x { position:absolute; left:232px; top:290px; font-family:var(--mono); white-space:nowrap; }
        #scene-team .tm-x .f-small { margin-bottom:10px; }
        #scene-team .tm-x .u { font-size:26px; line-height:1.3; color:var(--ink); }
        #scene-team .tm-repo span { color:var(--ink); }
        #scene-team .tm-repo { position:absolute; left:100px; top:938px; font-family:var(--mono); font-size:28px;
          color:var(--dim); white-space:nowrap; opacity:0; }
      `);

      ctx.el('div', 'f-kicker tm-event', COPY.event, root);

      const name = ctx.el('div', 'tm-name', '', root);
      chars = [];
      for (const ch of COPY.team) {
        const s = document.createElement('span');
        s.textContent = ch === ' ' ? ' ' : ch;
        name.appendChild(s);
        chars.push(s);
      }
      cursor = ctx.el('div', 'tm-cursor', '', root);

      const QR = (FILM.data.team && FILM.data.team.qr) || {};   // scenes/team.data.js, keyed by X handle
      cards = COPY.people.map((person, i) => {
        const card = ctx.el('div', 'tm-card', '', root);
        card.style.left = (100 + i * 580) + 'px';
        const img = document.createElement('img');
        img.src = ctx.asset(person.img);
        img.alt = person.name;
        card.appendChild(img);
        const frame = ctx.el('div', 'tm-frame', '', card);
        const who = ctx.el('div', 'tm-who', '', card);
        ctx.el('div', 'n', person.name, who);
        ctx.el('div', 'h', 'github.com/' + person.github, who);
        const qr = person.x && QR[person.x];
        if (person.x && !qr) ctx.el('div', 'h', 'x.com/' + person.x, who);
        if (qr) {   // QR to the X profile: n x n modules plus a 4-module quiet zone, dark on bone
          const q = qr.n + 8;
          ctx.el('div', 'tm-qr', `<svg viewBox="-4 -4 ${q} ${q}" shape-rendering="crispEdges"><path d="${qr.d}" fill="#03050a"/></svg>`, card);
          const x = ctx.el('div', 'tm-x', '', card);
          ctx.el('div', 'f-small', COPY.scan, x);
          ctx.el('div', 'u', 'x.com/' + person.x, x);
        }
        return { card, frame };
      });

      repo = ctx.el('div', 'tm-repo', '<span>' + COPY.site + '</span>&nbsp;&nbsp;/&nbsp;&nbsp;' + COPY.repo, root);
    },

    update(p, t, ctx) {
      // Team name types on, one dotted letter at a time.
      const k = ctx.lin(p, B.nameIn[0], B.nameIn[1]);
      const shown = Math.round(k * chars.length);
      let cx = null;
      for (let i = 0; i < chars.length; i++) chars[i].style.opacity = i < shown ? 1 : 0;
      if (k > 0 && k < 1 && shown > 0) {
        const last = chars[shown - 1];
        cx = last.offsetLeft + last.offsetWidth + last.parentNode.offsetLeft + 10;
      }
      cursor.style.opacity = cx === null ? 0 : 1;
      if (cx !== null) cursor.style.left = cx + 'px';

      // Avatars arrive one after another. The one arriving carries the amber frame, then settles to dim.
      cards.forEach((c, i) => {
        const a = B.people[i];
        const arrive = ctx.seg(p, a, a + B.personLen);
        const nextStart = i + 1 < B.people.length ? B.people[i + 1] : a + B.personLen + 0.02;
        const settle = ctx.seg(p, nextStart, nextStart + 0.06);
        const amber = Math.round((arrive > 0 ? 1 - settle : 0) * 100);
        c.card.style.opacity = arrive;
        c.card.style.transform = 'translateY(' + ((1 - arrive) * 18).toFixed(2) + 'px)';
        c.frame.style.borderColor = 'color-mix(in srgb, var(--amber) ' + amber + '%, var(--dim))';
      });

      repo.style.opacity = ctx.seg(p, B.repo[0], B.repo[1]);
    },
  });
})();
