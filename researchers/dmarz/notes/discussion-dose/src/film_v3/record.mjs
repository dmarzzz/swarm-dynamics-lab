// Record the film page frame by frame and encode it to the project's film format (h264 + silent aac, faststart).
// The page is a pure function of time (window.__seek), so every run produces the same frames.
//
//   node record.mjs <film.html> <out.mp4> --kit <brand dir> [--playwright <node_modules dir>] [--stills 12.5,60] [--jobs 4]
//
// --stills writes PNGs at those seconds next to the output and skips the encode (for checking frames).
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';
import { mkdirSync, rmSync, existsSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const flag = (name, fallback) => { const i = args.indexOf('--' + name); return i < 0 ? fallback : args[i + 1]; };
const [htmlPath, outPath] = args;
const kit = resolve(flag('kit', ''));
const jobs = parseInt(flag('jobs', '4'), 10);
const stills = flag('stills', '');
const require = createRequire(resolve(flag('playwright', join(kit, '..', 'node_modules')), 'x.js'));
const { chromium } = require('playwright');

const url = pathToFileURL(resolve(htmlPath)).href + '?record';
const browser = await chromium.launch({ headless: true });
const open = async () => {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(url); await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.fonts].map(f => f.load())));
  return page;
};
const first = await open();
const meta = await first.evaluate(() => window.__meta);
const shot = async (page, t, path) => { await page.evaluate(t => window.__seek(t), t); await page.screenshot({ path, type: 'png' }); };

if (stills) {
  const dir = dirname(resolve(outPath)); mkdirSync(dir, { recursive: true });
  for (const s of stills.split(',')) {                                   // a time in seconds, or a caption key plus an offset: C2+3
    const [key, off = '0'] = s.split('+');
    const t = key in meta.times ? meta.times[key] + parseFloat(off) : parseFloat(s);
    await shot(first, t, join(dir, `still-${s.replace('+', '_')}.png`)); console.log(`still ${s} @ ${t.toFixed(2)}s`); }
  console.log(JSON.stringify(meta)); await browser.close(); process.exit(0);
}

const frames = Math.round(meta.duration * meta.fps);
const dir = resolve(outPath) + '.frames'; rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
const pages = [first, ...(await Promise.all(Array.from({ length: jobs - 1 }, open)))];
let next = 0, done = 0;
await Promise.all(pages.map(async page => { for (;;) { const f = next++; if (f >= frames) return;
  await shot(page, f / meta.fps, join(dir, `f${String(f).padStart(5, '0')}.png`));
  if (++done % 300 === 0) console.log(`${done}/${frames} frames`); } }));
await browser.close();

// the mark: the kit's cube loop, small in the corner for the film, larger beside the name on the end card
const cube = join(kit, 'marks/cube/cube-loop-alpha.webm');
if (!existsSync(cube)) throw new Error('cube loop not found in ' + kit);
const { mark, mark2, end, duration } = meta;
const loop = ['-stream_loop', '-1', '-c:v', 'libvpx-vp9', '-i', cube];
const filter = [
  `[1:v]crop=380:380:0:0,scale=${mark.size}:${mark.size},format=rgba,fade=t=in:st=1.6:d=0.7:alpha=1,fade=t=out:st=${(end - 0.2).toFixed(2)}:d=0.45:alpha=1[m1]`,
  `[2:v]crop=380:380:0:0,scale=${mark2.size}:${mark2.size},format=rgba,fade=t=in:st=${(end + 0.5).toFixed(2)}:d=0.7:alpha=1[m2]`,
  `[0:v][m1]overlay=${mark.x}:${mark.y}:shortest=0[a]`,
  `[a][m2]overlay=${mark2.x}:${mark2.y}:shortest=0,format=yuv420p[v]`,
].join(';');
const ff = spawnSync('ffmpeg', ['-y', '-v', 'error', '-framerate', String(meta.fps), '-i', join(dir, 'f%05d.png'), ...loop, ...loop,
  '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
  '-filter_complex', filter, '-map', '[v]', '-map', '3:a', '-t', duration.toFixed(3),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', String(meta.fps), '-c:a', 'aac', '-b:a', '96k',
  '-movflags', '+faststart', resolve(outPath)], { stdio: 'inherit' });
if (ff.status !== 0) process.exit(ff.status || 1);
rmSync(dir, { recursive: true, force: true });
console.log(`wrote ${outPath}: ${frames} frames, ${duration.toFixed(1)} s`);
