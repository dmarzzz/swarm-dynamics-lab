// stack: the lab's control path as one diagram, built left to right.
// Three researchers' agents -> one git repo -> OpenTofu + Ansible -> short-lived servers -> run hub -> dashboard and registry.
// Then one amber token per agent travels the path: an experiment being deployed.
(() => {
  const COPY = {
    kicker: 'architecture',
    title: 'Open source, infrastructure as code',
    // one stage per column. `name` is the large label, `files` the small mono lines under it.
    stages: [
      // AGENTS.md, "What this repo is": "Three researchers each run their own AI agents against this one repo".
      // AGENTS.md is the operating manual every agent reads first.
      { name: ["researchers'", 'agents'], files: ['AGENTS.md'] },
      // agentops/fleet.example.yml ("Copy to fleet.yml", one entry per server);
      // agentops/scripts/agentops.py line 10: `claim` "writes claims/ID.yml via an auto-merged PR"; example agentops/claims/alice-boids-sweep.yml
      { name: ['git repo'], files: ['fleet.yml', 'claims/&lt;id&gt;.yml'] },
      // agentops/Taskfile.yml: `up` runs `tofu apply` (agentops/tofu/main.tf, digitalocean_droplet);
      // `provision` runs `ansible-playbook playbooks/provision.yml` (agentops/ansible/roles/*)
      { name: ['OpenTofu', '+ Ansible'], files: ['task up', 'task provision'] },
      // agentops/fleet.example.yml field `expires`; agentops/README.md "Costs and safety": every server needs an expires date.
      // lab/templates/experiment-worker/src/worker.py: the worker that executes queued runs on the server
      { name: ['short-lived', 'servers'], files: ['expires:', 'src/worker.py'] },
      // agentops/hub/hub.py (API, run queue, artifacts); agentops/hub/swarm_report.py (client every run reports with);
      // contract in agentops/docs/REPORTING.md
      { name: ['run hub'], files: ['hub/hub.py', 'swarm_report'] },
      // agentops/hub/dashboard.html; 5-experiments/EVIDENCE.md (the evidence registry, AGENTS.md Layout table)
      { name: ['dashboard,', 'evidence registry'], files: ['hub/dashboard.html', 'EVIDENCE.md'] },
    ],
    closing: 'all open source, MIT licence',     // LICENSE line 1: "MIT License". Comma, not colon: the Doto colon reads as a dagger
    note: 'the fleet setup is published as a scrubbed template: no secrets, no live inventory',   // agentops/README.md
    loop: 'results come back to the agents, who plan the next run',   // AGENTS.md, the session loop: agents read results and STATUS before picking work
    url: 'github.com/dmarzzz/swarm-dynamics-lab',         // AGENTS.md, Quick start: git clone https://github.com/dmarzzz/swarm-dynamics-lab
  };

  // geometry. YC is the path's centre line; TX is each column's text left edge.
  const YC = 400, NAME_Y = 600, FILE_Y = 690;
  const TX = [100, 400, 670, 1000, 1280, 1520];
  const AG = { x: 120, ys: [320, 400, 480] };                        // three agents (three researchers, AGENTS.md)
  const REPO = { x: 420, y0: 296, y1: 504 };
  const TOFU = { x: 690, s: 40 }, ANS = { x: 790, s: 40 };           // two steps: create, then configure
  const SRV = { x: 1040, ys: [272, 336, 400, 464, 528], s: 14 };     // illustrative: no count is claimed on screen
  const HUB = { x: 1320, r: 24 };
  const OUT = { x: 1540, y: 354, w: 140, h: 92 };
  // beats, as fractions of the scene
  const S = [[0.04, 0.12], [0.12, 0.21], [0.21, 0.30], [0.30, 0.39], [0.39, 0.47], [0.47, 0.56]];
  const TOK = [{ ag: 0, srv: 1, a: 0.57, b: 0.65 }, { ag: 1, srv: 3, a: 0.65, b: 0.73 }, { ag: 2, srv: 0, a: 0.73, b: 0.81 }];
  const LOOP = [0.80, 0.86], BACK = [0.845, 0.915];                  // the return path is drawn, then one result travels it
  const LOOP_Y = 208;
  const CLOSE = [0.90, 0.94];
  const NDOT = 16, NREP = 6;                                          // swarm dots per server, reports per deployment

  FILM.scene({
    id: 'stack',
    mount(root, ctx) {
      ctx.css(`
        #scene-stack .abs { position: absolute; white-space: nowrap; }
        #scene-stack canvas { position: absolute; left: 0; top: 0; }
        #scene-stack .name { font-size: 28px; line-height: 36px; color: var(--ink); }
        #scene-stack .files { font-size: 22px; line-height: 32px; color: var(--dim); }
        #scene-stack .closing { font-size: 56px; color: var(--zip); }
        #scene-stack .url { font-size: 28px; color: var(--ink); }
        #scene-stack .note { font-size: 22px; color: var(--dim); white-space: nowrap; }
      `);
      const cs = getComputedStyle(root), v = n => cs.getPropertyValue(n).trim() || '#888';
      this.C = { ink: v('--ink'), dim: v('--dim'), amber: v('--amber'), zip: v('--zip'), bg: v('--void') };
      const cv = ctx.el('canvas', '', null, root); cv.width = 1920; cv.height = 1080; this.g = cv.getContext('2d');
      const A = (cls, html, x, y) => { const e = ctx.el('div', 'abs ' + cls, html, root); e.style.left = x + 'px'; e.style.top = y + 'px'; return e; };
      A('f-kicker', COPY.kicker, 100, 56); A('f-title', COPY.title, 100, 88);
      this.names = COPY.stages.map((s, i) => A('name', s.name.join('<br>'), TX[i], NAME_Y));
      this.files = COPY.stages.map((s, i) => A('files', s.files.join('<br>'), TX[i], FILE_Y));
      this.closing = A('f-num closing', COPY.closing, 100, 822);
      this.url = A('url', COPY.url, 100, 900);
      this.note = A('note', COPY.note, 100, 950);
      this.loop = A('files', COPY.loop, 560, LOOP_Y - 44);

      // swarm dots around each server (a phyllotaxis spiral, like the lab scene)
      this.swarm = SRV.ys.map((y, i) => Array.from({ length: NDOT }, (_, j) => {
        const r = 13 + 3.6 * Math.sqrt(j + 0.5), a = j * 2.39996 + i * 1.7;
        return { x: SRV.x + r * Math.cos(a), y: y + r * Math.sin(a) }; }));
      // token paths: agent -> its commit on the repo -> down the repo line -> tofu -> ansible -> a server
      this.paths = TOK.map(t => {
        const pts = [[AG.x, AG.ys[t.ag]], [REPO.x, AG.ys[t.ag]], [REPO.x, YC], [ANS.x + ANS.s, YC], [SRV.x, SRV.ys[t.srv]]];
        const len = [0]; for (let i = 1; i < pts.length; i++) len.push(len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
        return { pts, len }; });
      // dashboard cells: 6 columns x 3 rows, one row per deployment
      this.cells = []; for (let r = 0; r < 3; r++) for (let c = 0; c < NREP; c++) this.cells.push({ x: OUT.x + 11 + c * 20, y: OUT.y + 30 + r * 19 });
    },

    update(p, t, ctx) {
      const g = this.g, C = this.C;
      g.clearRect(0, 0, 1920, 1080); g.lineCap = 'butt';
      let active = -1; S.forEach((s, i) => { if (p >= s[0] && p < s[1]) active = i; });
      const k = (i, a, b) => ctx.seg(p, S[i][0] + (S[i][1] - S[i][0]) * a, S[i][0] + (S[i][1] - S[i][0]) * b);   // eased 0..1 inside stage i
      const col = i => active === i ? C.amber : C.ink;
      const line = (x1, y1, x2, y2, f, c, w, al) => { if (f <= 0) return; g.globalAlpha = al; g.strokeStyle = c; g.lineWidth = w;
        g.beginPath(); g.moveTo(x1, y1); g.lineTo(x1 + (x2 - x1) * f, y1 + (y2 - y1) * f); g.stroke(); };
      const dot = (x, y, r, c, al) => { if (al <= 0) return; g.globalAlpha = al; g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.fill(); };
      const box = (x, y, w, h, c, al, lw) => { if (al <= 0) return; g.globalAlpha = al; g.strokeStyle = c; g.lineWidth = lw || 2; g.strokeRect(x, y, w, h); };

      // text: the stage being built is the one amber thing
      COPY.stages.forEach((s, i) => {
        this.names[i].style.opacity = k(i, 0, 0.3); this.names[i].style.color = active === i ? 'var(--amber)' : 'var(--ink)';
        this.files[i].style.opacity = k(i, 0.45, 0.85); });

      // connectors (dim), drawn first so glyphs sit on top
      const CA = 0.55;
      AG.ys.forEach((y, i) => line(AG.x + 14, y, REPO.x, y, k(1, 0.08 * i, 0.4 + 0.08 * i), C.dim, 1.5, CA));
      line(REPO.x, YC, TOFU.x, YC, k(2, 0, 0.35), C.dim, 1.5, CA);
      line(TOFU.x + TOFU.s, YC, ANS.x, YC, k(2, 0.4, 0.6), C.dim, 1.5, CA);
      SRV.ys.forEach((y, i) => line(ANS.x + ANS.s, YC, SRV.x - 12, y, k(3, 0.05 * i, 0.4 + 0.05 * i), C.dim, 1.5, CA));
      SRV.ys.forEach((y, i) => line(SRV.x + 12, y, HUB.x, YC, k(4, 0.05 * i, 0.4 + 0.05 * i), C.dim, 1.5, CA));
      line(HUB.x + HUB.r, YC, OUT.x, YC, k(5, 0, 0.35), C.dim, 1.5, CA);

      // 0. agents: three dots
      AG.ys.forEach((y, i) => dot(AG.x, y, 10, col(0), k(0, 0.15 * i, 0.4 + 0.15 * i)));

      // 1. repo: one line of history, one commit per agent
      line(REPO.x, REPO.y0, REPO.x, REPO.y1, k(1, 0.3, 0.75), col(1), 3, 1);
      AG.ys.forEach((y, i) => { const a = k(1, 0.4 + 0.08 * i, 0.6 + 0.08 * i); dot(REPO.x, y, 9, C.bg, a); dot(REPO.x, y, 9 * a, col(1), a); });

      // 2. OpenTofu creates the server, Ansible configures it
      box(TOFU.x, YC - TOFU.s / 2, TOFU.s, TOFU.s, col(2), k(2, 0.3, 0.5));
      const an = k(2, 0.55, 0.8); box(ANS.x, YC - ANS.s / 2, ANS.s, ANS.s, col(2), an);
      if (an > 0) { g.globalAlpha = an; g.fillStyle = col(2); g.fillRect(ANS.x + 12, YC - 8, 16, 16); }

      // 3. servers: empty until an experiment lands on them
      const land = SRV.ys.map(() => 2); TOK.forEach(tk => { land[tk.srv] = tk.b; });
      SRV.ys.forEach((y, i) => { const a = k(3, 0.3 + 0.07 * i, 0.55 + 0.07 * i), run = p >= land[i];
        g.globalAlpha = a; g.fillStyle = C.bg; g.fillRect(SRV.x - SRV.s / 2, y - SRV.s / 2, SRV.s, SRV.s);
        box(SRV.x - SRV.s / 2, y - SRV.s / 2, SRV.s, SRV.s, active === 3 ? C.amber : run ? C.ink : C.dim, a);
        if (run) this.swarm[i].forEach((d, j) => dot(d.x, d.y, 3, C.ink, 0.9 * ctx.lin(p, land[i] + j * 0.003, land[i] + j * 0.003 + 0.012))); });

      // 4. hub
      const hb = k(4, 0.4, 0.7);
      dot(HUB.x, YC, HUB.r, C.bg, hb > 0 ? 1 : 0);
      if (hb > 0) { g.globalAlpha = hb; g.strokeStyle = col(4); g.lineWidth = 2;
        g.beginPath(); g.arc(HUB.x, YC, HUB.r, 0, 6.2832); g.stroke(); g.beginPath(); g.arc(HUB.x, YC, 8, 0, 6.2832); g.stroke(); }

      // 5. dashboard: a frame, a header rule, one cell per reported run
      const ob = k(5, 0.3, 0.6);
      box(OUT.x, OUT.y, OUT.w, OUT.h, col(5), ob);
      line(OUT.x + 11, OUT.y + 16, OUT.x + OUT.w - 11, OUT.y + 16, k(5, 0.5, 0.8), col(5), 2, 1);
      this.cells.forEach((c, n) => { const tk = TOK[Math.floor(n / NREP)], j = n % NREP, a0 = tk.b + 0.012 + j * 0.012, done = ctx.lin(p, a0 + 0.05, a0 + 0.06);
        box(c.x + 0.5, c.y + 0.5, 13, 13, C.dim, ob * 0.6 * (1 - done), 1);
        if (done > 0) { g.globalAlpha = done; g.fillStyle = C.zip; g.fillRect(c.x, c.y, 14, 14); } });

      // reports: each run on a server reports to the hub, then shows on the dashboard
      TOK.forEach((tk, n) => { for (let j = 0; j < NREP; j++) { const a0 = tk.b + 0.012 + j * 0.012, q = ctx.lin(p, a0, a0 + 0.05);
        if (q <= 0 || q >= 1) continue; const c = this.cells[n * NREP + j], sy = SRV.ys[tk.srv];
        if (q < 0.55) { const f = ctx.ease(q / 0.55); dot(ctx.lerp(SRV.x + 12, HUB.x, f), ctx.lerp(sy, YC, f), 3, C.ink, 1); }
        else { const f = ctx.ease((q - 0.55) / 0.45); dot(ctx.lerp(HUB.x, c.x + 7, f), ctx.lerp(YC, c.y + 7, f), 3, C.ink, 1); } } });

      // the token: one experiment being deployed, from one agent to one server
      TOK.forEach((tk, n) => { if (p < tk.a || p >= tk.b) return; const P = this.paths[n], L = P.len[P.len.length - 1], d = ctx.seg(p, tk.a, tk.b) * L;
        let i = 1; while (i < P.len.length - 1 && P.len[i] < d) i++;
        const f = (d - P.len[i - 1]) / (P.len[i] - P.len[i - 1]), x = ctx.lerp(P.pts[i - 1][0], P.pts[i][0], f), y = ctx.lerp(P.pts[i - 1][1], P.pts[i][1], f);
        dot(x, y, 16, C.amber, 0.18); dot(x, y, 8, C.amber, 1); });

      // 6. the loop: results come back to the agents (cyan = a confirmed result)
      { const pts = [[OUT.x + OUT.w / 2, OUT.y], [OUT.x + OUT.w / 2, LOOP_Y], [AG.x, LOOP_Y], [AG.x, AG.ys[0] - 18]];
        const len = [0]; for (let i = 1; i < pts.length; i++) len.push(len[i - 1] + Math.abs(pts[i][0] - pts[i - 1][0]) + Math.abs(pts[i][1] - pts[i - 1][1]));
        const L = len[len.length - 1], at = d => { let i = 1; while (i < len.length - 1 && len[i] < d) i++; const f = (d - len[i - 1]) / (len[i] - len[i - 1]);
          return [ctx.lerp(pts[i - 1][0], pts[i][0], f), ctx.lerp(pts[i - 1][1], pts[i][1], f)]; };
        const f = ctx.seg(p, LOOP[0], LOOP[1]);
        if (f > 0) { g.globalAlpha = 0.8; g.strokeStyle = C.zip; g.lineWidth = 2; g.beginPath(); g.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < pts.length; i++) { if (len[i] <= f * L) g.lineTo(pts[i][0], pts[i][1]); else { const q = at(f * L); g.lineTo(q[0], q[1]); break; } }
          g.stroke(); }
        if (f >= 1) { const [x, y] = pts[3]; g.globalAlpha = 0.9; g.fillStyle = C.zip; g.beginPath(); g.moveTo(x, y + 4); g.lineTo(x - 7, y - 8); g.lineTo(x + 7, y - 8); g.closePath(); g.fill(); }
        const b = ctx.lin(p, BACK[0], BACK[1]);
        if (b > 0 && b < 1) { const q = at(ctx.ease(b) * L); dot(q[0], q[1], 14, C.zip, 0.18); dot(q[0], q[1], 7, C.zip, 1); }
        const got = ctx.seg(p, BACK[1], BACK[1] + 0.03);
        if (got > 0) AG.ys.forEach(y => { g.globalAlpha = got; g.strokeStyle = C.zip; g.lineWidth = 2; g.beginPath(); g.arc(AG.x, y, 16, 0, 6.2832); g.stroke(); });
        this.loop.style.opacity = ctx.seg(p, LOOP[0] + 0.02, LOOP[1]); this.loop.style.color = 'var(--zip)'; }

      // closing line
      this.closing.style.opacity = ctx.seg(p, CLOSE[0], CLOSE[1]);
      this.url.style.opacity = ctx.seg(p, CLOSE[0] + 0.02, CLOSE[1] + 0.02);
      this.note.style.opacity = ctx.seg(p, CLOSE[0] + 0.04, CLOSE[1] + 0.04);
      g.globalAlpha = 1;
    },
  });
})();
