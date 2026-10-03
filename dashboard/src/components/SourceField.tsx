import { useEffect, useRef } from 'react';
import type { Entry } from '../data/types';

/**
 * Hero fallback until lane G's HeroSwarm lands: every source in the library is one dot,
 * x = when an agent added it, y = topic band, colour = kind. Dots drift gently toward their slot.
 */
export function SourceField({ entries, times, start, end, topics, height = 300 }: {
  entries: Entry[]; times: Map<string, number>; start: number; end: number; topics: string[]; height?: number;
}) {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const cv = ref.current;
    if (!cv) return;
    const ctx0 = cv.getContext('2d');
    if (!ctx0) return;
    const ctx: CanvasRenderingContext2D = ctx0;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let raf = 0;
    let w = 0, h = 0;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const css = getComputedStyle(document.documentElement);
    const color = (k: string) => css.getPropertyValue(`--k-${k}`).trim() || '#888';
    const ink = css.getPropertyValue('--rule').trim();
    const tIdx = new Map(topics.map((t, i) => [t, i]));
    let seed = 7;
    const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    const pts = entries.map((e) => {
      const t = times.get(e.id) ?? start;
      const ti = tIdx.get(e.topics[0]) ?? topics.length - 1;
      const jx = (rnd() - 0.5) * 0.014;
      return { fx: Math.min(1, Math.max(0, (t - start) / Math.max(1, end - start) + jx)), fy: (ti + 0.15 + rnd() * 0.7) / topics.length, x: rnd(), y: rnd(), c: e.kind, r: e.read_depth === 'full' || e.read_depth === 'ran' ? 1.7 : 1.15 };
    });
    const palette = new Map<string, string>();
    for (const p of pts) if (!palette.has(p.c)) palette.set(p.c, color(p.c));

    const resize = () => {
      const r = cv.getBoundingClientRect();
      w = r.width; h = r.height;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    const ro = new ResizeObserver(() => { resize(); if (reduce) draw(); });
    ro.observe(cv);

    const pad = 6;
    let frame = 0;
    function draw() {
      frame++;
      ctx.clearRect(0, 0, w, h);
      ctx.strokeStyle = ink;
      ctx.lineWidth = 1;
      ctx.setLineDash([1, 4]);
      for (let i = 1; i < topics.length; i++) {
        const y = Math.round(pad + (h - 2 * pad) * (i / topics.length)) + 0.5;
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
      }
      ctx.setLineDash([]);
      let settled = true;
      const k = reduce ? 1 : 0.06;
      for (const p of pts) {
        const tx = p.fx, ty = p.fy;
        p.x += (tx - p.x) * k; p.y += (ty - p.y) * k;
        if (Math.abs(tx - p.x) > 0.0005) settled = false;
        const wob = reduce || !settled ? 0 : Math.sin(frame * 0.012 + p.fy * 40 + p.fx * 13) * 0.6;
        ctx.fillStyle = palette.get(p.c)!;
        ctx.globalAlpha = 0.82;
        ctx.beginPath();
        ctx.arc(pad + p.x * (w - 2 * pad), pad + p.y * (h - 2 * pad) + wob, p.r, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      if (!reduce) raf = requestAnimationFrame(draw);
    }
    draw();
    return () => { cancelAnimationFrame(raf); ro.disconnect(); };
  }, [entries, times, start, end, topics]);

  return <canvas ref={ref} style={{ width: '100%', height, display: 'block' }} role="img"
    aria-label={`${entries.length} sources plotted by the time an agent added them and by topic`} />;
}
