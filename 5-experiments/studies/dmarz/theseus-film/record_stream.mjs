// Record a film page straight into the encoder, with no frame files on disk.
// Same page contract, same mark overlay and same encode as ../discussion-dose/src/film_v3/record.mjs, which first writes
// every frame as a JPEG (about 5 GB for a four-minute film). Use this one when the disk cannot hold that.
//
//   node record_stream.mjs <film.html> <out.mp4> --kit <brand dir> [--playwright <node_modules dir>] [--jobs 4]
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { once } from 'node:events';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const flag = (name, fallback) => { const i = args.indexOf('--' + name); return i < 0 ? fallback : args[i + 1]; };
const [htmlPath, outPath] = args;
const kit = resolve(flag('kit', ''));
const jobs = parseInt(flag('jobs', '4'), 10);
const require = createRequire(resolve(flag('playwright', join(kit, '..', 'node_modules')), 'x.js'));
const { chromium } = require('playwright');

const url = pathToFileURL(resolve(htmlPath)).href + '?record';
const browser = await chromium.launch({ headless: true, args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] });
const open = async () => {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(url); await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.fonts].map(f => f.load())));
  return page;
};
const first = await open();
const meta = await first.evaluate(() => window.__meta);
if (Math.max(...meta.caps) >= 98) throw new Error('a caption is 98 characters or longer: ' + meta.caps.join(' '));
const frames = Math.round(meta.duration * meta.fps);

const { mark, mark2, end, duration } = meta;
const cube = join(kit, 'marks/cube/cube-loop-alpha.webm');
if (!existsSync(cube)) throw new Error('cube loop not found in ' + kit);
const CYCLE = 16, loop = ['-stream_loop', '-1', '-an', '-c:v', 'libvpx-vp9', '-i', cube];
const endOffset = (((10.2 - (end + 0.5)) % CYCLE) + CYCLE) % CYCLE;
const filter = [
  `[1:v]crop=380:380:0:0,scale=${mark.size}:${mark.size},format=rgba,fade=t=in:st=1.6:d=0.7:alpha=1,fade=t=out:st=${(end - 0.2).toFixed(2)}:d=0.45:alpha=1[m1]`,
  `[2:v]trim=start=${endOffset.toFixed(2)},setpts=PTS-STARTPTS,crop=380:380:0:0,scale=${mark2.size}:${mark2.size},format=rgba,fade=t=in:st=${(end + 0.5).toFixed(2)}:d=0.7:alpha=1[m2]`,
  `[0:v][m1]overlay=${mark.x}:${mark.y}:shortest=0[a]`,
  `[a][m2]overlay=${mark2.x}:${mark2.y}:shortest=0,scale=in_range=pc:out_range=tv,format=yuv420p[v]`,
].join(';');
const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(meta.fps), '-i', 'pipe:0', ...loop, ...loop,
  '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
  '-filter_complex', filter, '-map', '[v]', '-map', '3:a', '-t', duration.toFixed(3),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-r', String(meta.fps), '-c:a', 'aac', '-b:a', '96k',
  '-movflags', '+faststart', resolve(outPath)], { stdio: ['pipe', 'inherit', 'inherit'] });
const closed = once(ff, 'close');

// the pages render out of order; frames wait here until their turn, and a page that gets too far ahead waits too
const pages = [first, ...(await Promise.all(Array.from({ length: jobs - 1 }, open)))];
const ready = new Map(); let next = 0, written = 0, flushing = Promise.resolve();
const flush = () => flushing = flushing.then(async () => {
  while (ready.has(written)) { const buf = ready.get(written); ready.delete(written); written++;
    if (!ff.stdin.write(buf)) await once(ff.stdin, 'drain');
    if (written % 600 === 0) console.log(`${written}/${frames} frames`); } });
await Promise.all(pages.map(async page => { for (;;) { const f = next++; if (f >= frames) return;
  while (f - written > 48) await new Promise(r => setTimeout(r, 15));
  await page.evaluate(t => window.__seek(t), f / meta.fps);
  ready.set(f, await page.screenshot({ type: 'jpeg', quality: 100 })); flush(); } }));
await flush(); ff.stdin.end();
const [code] = await closed; await browser.close();
if (code !== 0) process.exit(code || 1);
console.log(`wrote ${outPath}: ${frames} frames, ${duration.toFixed(1)} s`);
