// Record the film frame by frame (the page is a pure function of time) and encode h264 + silent aac, faststart.
// Frames are piped straight into ffmpeg in order, so nothing but the mp4 touches the disk.
//   node record.mjs [out.mp4] [--jobs 6] [--only <scene id>]
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const flag = (name, fallback) => { const i = args.indexOf('--' + name); return i < 0 ? fallback : args[i + 1]; };
const outPath = resolve(args[0] && !args[0].startsWith('--') ? args[0] : join(here, '_out', 'swarm-of-theseus-demo.mp4'));
const jobs = parseInt(flag('jobs', '6'), 10), only = flag('only', '');
const require = createRequire(resolve(process.env.PLAYWRIGHT_MODULES || join(homedir(), 'dmarz-brand-and-content-kit', 'node_modules'), 'x.js'));
const { chromium } = require('playwright');

const url = pathToFileURL(join(here, 'index.html')).href + '?record' + (only ? '&only=' + only : '');
const browser = await chromium.launch({ headless: true, args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist', '--allow-file-access-from-files'] });
const open = async () => {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('page exception:', e.message));
  await page.goto(url); await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.fonts].map(f => f.load().catch(() => {}))));
  return page;
};
const first = await open();
const meta = await first.evaluate(() => window.__meta);
const frames = Math.round(meta.duration * meta.fps);
mkdirSync(dirname(outPath), { recursive: true });

// the mark: the kit's cube loop laid on bottom right (the page hides its own copy when recording)
const m = meta.mark, cube = join(here, 'kit', 'cube-loop-alpha.webm');
const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(meta.fps), '-c:v', 'mjpeg', '-i', '-',
  '-stream_loop', '-1', '-an', '-c:v', 'libvpx-vp9', '-i', cube,
  '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
  '-filter_complex', `[1:v]crop=380:380:0:0,scale=${m.size}:${m.size},format=rgba[m];[0:v][m]overlay=${m.x}:${m.y}:shortest=0,scale=in_range=pc:out_range=tv,format=yuv420p[v]`,
  '-map', '[v]', '-map', '2:a', '-t', meta.duration.toFixed(3),
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
  '-r', String(meta.fps), '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', outPath], { stdio: ['pipe', 'inherit', 'inherit'] });
const exited = new Promise(r => ff.on('close', r));
ff.stdin.on('error', () => {});

const pages = [first, ...(await Promise.all(Array.from({ length: jobs - 1 }, open)))];
const ready = new Map(); let next = 0, written = 0, wake = () => {};
const writer = (async () => { while (written < frames) {
  if (!ready.has(written)) { await new Promise(r => { wake = r; }); continue; }
  const buf = ready.get(written); ready.delete(written); written++;
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (written % 300 === 0) console.log(`${written}/${frames} frames`); }
  ff.stdin.end(); })();
await Promise.all(pages.map(async page => { for (;;) { const f = next++; if (f >= frames) return;
  while (f - written > 240) await new Promise(r => setTimeout(r, 20));          // keep at most a few seconds in memory
  await page.evaluate(t => window.__seek(t), f / meta.fps);
  ready.set(f, await page.screenshot({ type: 'jpeg', quality: 95 })); wake(); } }));
await writer; await browser.close();
const code = await exited;
if (code !== 0) process.exit(code || 1);
console.log(`wrote ${outPath}: ${frames} frames, ${meta.duration.toFixed(1)} s`, JSON.stringify(meta.scenes));
