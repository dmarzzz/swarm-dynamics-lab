/** Run with `node dashboard/scripts/test_question_reviews.mjs`; no DOM or test runner required. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';

const source = readFileSync(new URL('../src/lib/questionReviews.ts', import.meta.url), 'utf8');
const { outputText, diagnostics } = ts.transpileModule(source, {
  compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022, strict: true },
  reportDiagnostics: true,
});
assert.equal(diagnostics?.length ?? 0, 0);
const helpers = await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
const {
  QUESTION_REVIEW_STORAGE_KEY, QUESTION_REVIEW_SCHEMA, parseReviewState,
  needsRecheck, mergeReviewImport, createReviewExport, updateReview, acknowledgeReview,
} = helpers;

const candidates = [
  { id: 'SOC-01', title: 'Revised question', candidate_sha256: 'a'.repeat(64), change: 'revised' },
  { id: 'SOC-02', title: 'Unchanged question', candidate_sha256: 'b'.repeat(64), change: 'unchanged' },
  { id: 'BUD-01', title: 'New question', candidate_sha256: 'c'.repeat(64), change: 'new' },
];
const knownIds = new Set(candidates.map(candidate => candidate.id));
const now = '2026-10-03T12:00:00.000Z';
const empty = () => parseReviewState(null, knownIds).state;
const tests = [];
function test(name, run) { tests.push([name, run]); }

test('keeps the standalone storage key and defaults', () => {
  assert.equal(QUESTION_REVIEW_STORAGE_KEY, 'swarm-lab-question-atlas-review-v1');
  assert.deepEqual(empty(), { reviewer: '', review: {} });
  assert.equal(needsRecheck(candidates[0], undefined), false);
});

test('preserves legacy decisions, notes and absent fingerprints', () => {
  const { state, warning } = parseReviewState(JSON.stringify({ reviewer: 'Ada', review: {
    'SOC-01': { status: 'Shortlist', notes: 'Old rationale', updated: 'old' },
    'SOC-02': { notes: 'Notes before picking a status' },
  } }), knownIds);
  assert.equal(warning, undefined);
  assert.equal(state.reviewer, 'Ada');
  assert.deepEqual(state.review['SOC-01'], { status: 'Shortlist', notes: 'Old rationale', updated: 'old' });
  assert.equal(state.review['SOC-02'].status, 'Unreviewed');
  assert.equal(needsRecheck(candidates[0], state.review['SOC-01']), true);
  assert.equal(needsRecheck(candidates[1], state.review['SOC-02']), false);
});

test('stale export and import round trips never acknowledge missing or old hashes', () => {
  const original = parseReviewState(JSON.stringify({ reviewer: 'Ada', review: {
    'SOC-01': { status: 'Discuss', notes: 'Needs a look' },
    'SOC-02': { status: 'Park', notes: 'Old version', candidate_sha256: 'd'.repeat(64) },
  } }), knownIds).state;
  const snapshot = JSON.stringify(original);
  const payload = createReviewExport(original, candidates, 'atlas-current', now);
  assert.equal(payload.schema, QUESTION_REVIEW_SCHEMA);
  assert.equal(payload.date, now);
  assert.equal(payload.reviewer, 'Ada');
  assert.equal(payload.review['SOC-01'].title, candidates[0].title);
  assert.equal(Object.hasOwn(payload.review['SOC-01'], 'candidate_sha256'), false);
  assert.equal(payload.review['SOC-02'].candidate_sha256, 'd'.repeat(64));
  const imported = mergeReviewImport(empty(), JSON.stringify(payload), candidates, 'atlas-current');
  assert.equal(imported.imported, 2);
  assert.equal(imported.atlasMismatch, false);
  assert.equal(needsRecheck(candidates[0], imported.state.review['SOC-01']), true);
  assert.equal(needsRecheck(candidates[1], imported.state.review['SOC-02']), true);
  assert.equal(JSON.stringify(original), snapshot);
});

test('current hashes clear recheck even when the card is marked revised', () => {
  const state = updateReview(empty(), candidates[0], { status: 'Shortlist' }, now);
  assert.equal(needsRecheck(candidates[0], state.review['SOC-01']), false);
  const imported = mergeReviewImport(empty(), createReviewExport(state, candidates, 'older-atlas', now), candidates, 'new-atlas');
  assert.equal(imported.atlasMismatch, true);
  assert.equal(needsRecheck(candidates[0], imported.state.review['SOC-01']), false);
});

test('imports known IDs only and keeps unrelated local reviews and reviewer', () => {
  const state = updateReview({ ...empty(), reviewer: 'Local reviewer' }, candidates[1], { status: 'Park' }, now);
  const imported = mergeReviewImport(state, { schema: QUESTION_REVIEW_SCHEMA, reviewer: 'Other reviewer', review: {
    'SOC-01': { status: 'Discuss', notes: 'Imported' },
    UNKNOWN: { status: 'invalid but unknown' },
  } }, candidates, 'atlas');
  assert.equal(imported.imported, 1);
  assert.equal(imported.state.reviewer, 'Local reviewer');
  assert.equal(imported.state.review['SOC-01'].status, 'Discuss');
  assert.equal(imported.state.review['SOC-02'].status, 'Park');
  assert.equal(imported.state.review.UNKNOWN, undefined);
  assert.equal(state.review['SOC-01'], undefined);
  const saved = parseReviewState('{"review":{"UNKNOWN":{},"__proto__":{"polluted":true}}}', knownIds);
  assert.deepEqual(saved.state.review, {});
  assert.equal({}.polluted, undefined);
});

test('rejects malformed imports atomically', () => {
  const state = updateReview(empty(), candidates[0], { notes: 'Keep me' }, now);
  const snapshot = JSON.stringify(state);
  for (const invalid of [
    '{', null, [], {}, { schema: 'other', review: {} },
    { schema: QUESTION_REVIEW_SCHEMA, review: [] },
    { schema: QUESTION_REVIEW_SCHEMA, review: { 'SOC-01': null } },
    { schema: QUESTION_REVIEW_SCHEMA, review: { 'SOC-01': [] } },
    { schema: QUESTION_REVIEW_SCHEMA, review: { 'SOC-02': { status: 'Park' }, 'SOC-01': { status: 'Accepted' } } },
  ]) assert.throws(() => mergeReviewImport(state, invalid, candidates, 'atlas'));
  assert.equal(JSON.stringify(state), snapshot);
});

test('present malformed text fields reject atomically without replacing notes or hashes', () => {
  const state = updateReview(empty(), candidates[0], { status: 'Shortlist', notes: 'Keep this rationale' }, now);
  const snapshot = JSON.stringify(state);
  for (const field of ['notes', 'updated', 'candidate_sha256']) {
    for (const invalid of [null, false, 42, [], {}, undefined]) {
      const payload = { schema: QUESTION_REVIEW_SCHEMA, review: {
        'SOC-02': { status: 'Discuss', notes: 'Valid addition before the bad entry' },
        'SOC-01': { status: 'Park', [field]: invalid },
      } };
      assert.throws(() => mergeReviewImport(state, payload, candidates, 'atlas'), /Invalid review fields/);
      assert.equal(JSON.stringify(state), snapshot);
      if (invalid !== undefined) {
        assert.throws(() => mergeReviewImport(state, JSON.stringify(payload), candidates, 'atlas'), /Invalid review fields/);
        assert.equal(JSON.stringify(state), snapshot);
      }
    }
  }
  const legacy = mergeReviewImport(state, { schema: QUESTION_REVIEW_SCHEMA, review: {
    'SOC-02': { status: 'Discuss' },
  } }, candidates, 'atlas');
  assert.deepEqual(legacy.state.review['SOC-02'], { status: 'Discuss', notes: '', updated: '' });
  assert.deepEqual(legacy.state.review['SOC-01'], state.review['SOC-01']);
  const recovered = parseReviewState(JSON.stringify({ review: {
    'SOC-01': { status: 'Shortlist', notes: 42, updated: null, candidate_sha256: false },
  } }), knownIds);
  assert.ok(recovered.warning);
  assert.deepEqual(recovered.state.review['SOC-01'], { status: 'Shortlist', notes: '', updated: '' });
});

test('malformed saved data recovers valid entries without throwing', () => {
  for (const raw of ['{', 'null', '[]', '3', '{"review":[]}', '{"review":null}']) {
    const result = parseReviewState(raw, knownIds);
    assert.ok(result.warning);
    assert.deepEqual(result.state, empty());
  }
  const result = parseReviewState(JSON.stringify({ reviewer: 3, review: {
    'SOC-01': { status: 'Shortlist', notes: 3, updated: null },
    'SOC-02': { status: false },
  } }), knownIds);
  assert.ok(result.warning);
  assert.deepEqual(result.state.review['SOC-01'], { status: 'Shortlist', notes: '', updated: '' });
  assert.equal(result.state.review['SOC-02'], undefined);
  assert.equal(result.state.reviewer, '');
});

test('new notes use the current fingerprint but edits to stale notes preserve staleness', () => {
  const fresh = updateReview(empty(), candidates[0], { notes: 'First look' }, now);
  assert.equal(fresh.review['SOC-01'].candidate_sha256, candidates[0].candidate_sha256);
  assert.equal(needsRecheck(candidates[0], fresh.review['SOC-01']), false);
  for (const fingerprint of [undefined, 'old-fingerprint']) {
    const old = parseReviewState(JSON.stringify({ review: { 'SOC-01': {
      status: 'Discuss', notes: 'Original', candidate_sha256: fingerprint,
    } } }), knownIds).state;
    const edited = updateReview(old, candidates[0], { notes: 'More thoughts' }, now);
    assert.equal(edited.review['SOC-01'].candidate_sha256, fingerprint);
    assert.equal(edited.review['SOC-01'].status, 'Discuss');
    assert.equal(edited.review['SOC-01'].updated, now);
    assert.equal(needsRecheck(candidates[0], edited.review['SOC-01']), true);
    assert.equal(old.review['SOC-01'].notes, 'Original');
    const confirmed = acknowledgeReview(edited, candidates[0], now);
    assert.equal(needsRecheck(candidates[0], confirmed.review['SOC-01']), false);
    assert.equal(confirmed.review['SOC-01'].notes, 'More thoughts');
    assert.equal(needsRecheck(candidates[0], edited.review['SOC-01']), true);
    const decided = updateReview(old, candidates[0], { status: 'Park' }, now);
    assert.equal(needsRecheck(candidates[0], decided.review['SOC-01']), false);
  }
});

test('export excludes unknown entries and preserves markup as ordinary data', () => {
  const state = updateReview(empty(), candidates[0], { notes: '<script>not executed</script>' }, now);
  state.review.UNKNOWN = { status: 'Park', notes: 'Not a card', updated: now };
  const payload = createReviewExport(state, candidates, 'atlas', now);
  assert.deepEqual(Object.keys(payload.review), ['SOC-01']);
  assert.equal(payload.review['SOC-01'].notes, '<script>not executed</script>');
});

test('empty changes and acknowledgement without a review do not create entries', () => {
  const state = empty();
  assert.equal(updateReview(state, candidates[0], {}, now), state);
  assert.equal(acknowledgeReview(state, candidates[0], now), state);
  const noted = updateReview(state, candidates[0], { status: undefined, notes: 'A thought' }, now);
  assert.equal(noted.review['SOC-01'].status, 'Unreviewed');
  const decided = updateReview(noted, candidates[0], { status: 'Park', notes: undefined }, now);
  assert.equal(decided.review['SOC-01'].notes, 'A thought');
});

for (const [name, run] of tests) {
  run();
  console.log(`PASS ${name}`);
}
console.log(`${tests.length} question-review tests passed.`);
