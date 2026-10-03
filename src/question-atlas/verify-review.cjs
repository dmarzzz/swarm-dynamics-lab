// Run against a locally served, generated atlas. Uses an isolated browser profile.
// NODE_PATH must expose Playwright; Chrome must be installed.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(process.argv[2] || 'http://127.0.0.1:8767/review.html');
    const atlas = await page.evaluate(() => JSON.parse(document.getElementById('atlas-data').textContent));
    const revised = atlas.candidates.find(d => d.change === 'revised');
    const unchanged = atlas.candidates.find(d => d.change === 'unchanged');
    assert(revised && unchanged && atlas.changes.new.length);
    assert.equal(await page.locator('.candidate').count(), atlas.candidates.length);
    // Simulate the original v1 local review, which had no per-candidate fingerprint.
    await page.evaluate(({ revised, unchanged }) => localStorage.setItem('swarm-lab-question-atlas-review-v1', JSON.stringify({
      reviewer: 'Compatibility check', review: {
        [revised.id]: { status: 'Shortlist', notes: 'Keep this earlier reason' },
        [unchanged.id]: { status: 'Park', notes: 'Unchanged decision' }
      }
    })), { revised, unchanged });
    await page.reload();
    await page.locator('#changeFilter').selectOption('recheck');
    assert.equal(await page.locator('.candidate').count(), 1);
    assert.equal(await page.locator('#decision').inputValue(), 'Shortlist');
    assert.equal(await page.locator('#notes').inputValue(), 'Keep this earlier reason');
    await page.locator('#notes').fill('Revised note; still needs a decision check');
    assert.equal(await page.locator('#acknowledge').count(), 1);
    await page.locator('#acknowledge').click();
    assert.equal(await page.locator('.candidate').count(), 0);
    await page.locator('#clear').click();
    await page.locator(`[data-id="${revised.id}"]`).click();
    assert.equal(await page.locator('#decision').inputValue(), 'Shortlist');
    await page.reload();
    assert.equal(await page.locator('#notes').inputValue(), 'Revised note; still needs a decision check');
    assert.equal(await page.locator('#acknowledge').count(), 0);
    await page.locator('#changeFilter').selectOption('new');
    assert.equal(await page.locator('.candidate').count(), atlas.changes.new.length);
    await page.locator('#changeFilter').selectOption('revised');
    assert.equal(await page.locator('.candidate').count(), atlas.changes.revised.length);
    await page.locator('#clear').click();
    await page.locator('#area').selectOption('agent-budgets');
    assert.equal(await page.locator('.candidate').count(), atlas.candidates.filter(d => d.area === 'agent-budgets').length);
    // Old exports must retain notes and decisions, skip unknown IDs, and mark revisions.
    const note = '<img src=x onerror=alert(1)> literal reviewer text';
    await page.locator('#file').setInputFiles({ name: 'old-review.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify({
      schema: 'swarm-lab-question-review-v1', atlas_sha256: 'old-version', review: {
        [revised.id]: { status: 'Discuss', notes: note }, 'UNKNOWN-999': { status: 'Park' }
      }
    })) });
    await page.waitForFunction(() => document.getElementById('notice').textContent.includes('Imported 1'));
    await page.locator('#clear').click();
    await page.locator('#changeFilter').selectOption('recheck');
    assert.equal(await page.locator('.candidate').count(), 1);
    assert.equal(await page.locator('#notes').inputValue(), note);
    assert.equal(await page.locator('#notes img').count(), 0);
    await page.locator('#acknowledge').click();
    const downloadReady = page.waitForEvent('download');
    await page.locator('#export').click();
    const download = await downloadReady;
    const exported = JSON.parse(await fs.readFile(await download.path(), 'utf8'));
    assert.equal(exported.review[revised.id].candidate_sha256, revised.candidate_sha256);
    assert.equal(exported.review[revised.id].status, 'Discuss');
    assert.equal(exported.review[revised.id].notes, note);
    assert.equal(exported.review[unchanged.id].status, 'Park');
    assert(!exported.review['UNKNOWN-999']);
    await page.locator('#clear').click();
    await page.screenshot({ path: '/tmp/question-atlas-update-desktop.png', fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({ path: '/tmp/question-atlas-update-mobile.png', fullPage: true });
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({ candidates: atlas.candidates.length, changes: Object.fromEntries(Object.entries(atlas.changes).map(([k,v]) => [k,v.length])), preserved_v1_reviews: true, export_import: true, mobile_overflow: false, page_errors: errors }));
    await context.close();
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
