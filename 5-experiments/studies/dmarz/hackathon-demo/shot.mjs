// Stills for checking a scene.
//   node shot.mjs <scene id> 0.1,0.5,0.9      p values (0..1 through the scene) -> _shots/<id>-<p>.png
//   node shot.mjs film 3,12,40,80,110         seconds into the whole film      -> _shots/film-<t>.png
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const [id, list = '0.1,0.5,0.9'] = process.argv.slice(2);
if (!id) { console.error('usage: node shot.mjs <scene id | film> <p or seconds, comma separated>'); process.exit(2); }
const require = createRequire(resolve(process.env.PLAYWRIGHT_MODULES || join(homedir(), 'dmarz-brand-and-content-kit', 'node_modules'), 'x.js'));
const { chromium } = require('playwright');
const browser = await chromium.launch({ headless: true, args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist', '--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
page.on('console', m => { if (m.type() === 'error') console.log('page error:', m.text()); });
page.on('pageerror', e => console.log('page exception:', e.message));
await page.goto(pathToFileURL(join(here, 'index.html')).href + '?record' + (id === 'film' ? '' : '&only=' + id));
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => Promise.all([...document.fonts].map(f => f.load().catch(() => {}))));
const meta = await page.evaluate(() => window.__meta);
mkdirSync(join(here, '_shots'), { recursive: true });
for (const v of list.split(',')) {
  const t = id === 'film' ? parseFloat(v) : parseFloat(v) * meta.duration;
  await page.evaluate(t => window.__seek(t), t);
  const path = join(here, '_shots', `${id}-${v}.png`);
  await page.screenshot({ path, type: 'png' });
  console.log(path, `(t=${t.toFixed(2)}s)`);
}
await browser.close();
