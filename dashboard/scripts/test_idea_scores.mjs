import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';
const source = readFileSync(new URL('../src/lib/ideaScores.ts', import.meta.url), 'utf8');
const { outputText } = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022 } });
const h = await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
const rating = { dimensions: { visual: 0, practical: 0, theory: 0, novelty: 0 }, score: 0, rationale: 'Intentional zero', assessed_by: 'test', assessed_at: '2026-10-04', candidate_sha256: 'a' };
const data = { ideas: {
  'SOC-01': { candidate_sha256: 'a', ratings: { vishesh: rating, dmarz: null, shadow: null } },
  'SOC-02': { candidate_sha256: 'b', ratings: { vishesh: { ...rating, dimensions: {visual:100, practical:100, theory:100, novelty:100}, score:100 }, dmarz: null, shadow: null } },
  'SOC-03': { candidate_sha256: 'c', ratings: { vishesh: null, dmarz: null, shadow: null } },
} };
assert.equal(h.total({visual:100, practical:100, theory:100, novelty:100}),100);
assert.equal(h.total({visual:100, practical:0, theory:0, novelty:0}),30);
assert.equal(h.total({visual:0, practical:0, theory:0, novelty:10}),2);
assert(h.validRating(rating)); assert(h.validRating(null));
for (const value of [-1, 101, NaN, Infinity, '75', null]) assert(!h.validRating({...rating, dimensions:{...rating.dimensions, visual:value}}));
assert(!h.validRating({...rating, score:1}));
assert(!h.validRating({...rating, rationale:''}));
assert.equal(h.effectiveRating(data, {}, 'SOC-01','vishesh').score,0);
assert.equal(h.effectiveRating(data, {}, 'SOC-01','dmarz'),null);
assert.equal(h.effectiveRating(data, {vishesh:{'SOC-01':null}}, 'SOC-01','vishesh'),null);
assert.equal(h.effectiveRating(data, {}, 'SOC-02','vishesh').stale,true);
assert.deepEqual(h.sortIdeas([{id:'SOC-03'},{id:'SOC-02'},{id:'SOC-01'}],'vishesh',data,{}).map(x=>x.id),['SOC-01','SOC-02','SOC-03']);
const draft = {dmarz:{'SOC-01':{...rating, assessed_by:'dmarz/test'}}};
const exported = h.scoreExport(data, draft, 'dmarz');
assert.equal(exported.reviewer,'dmarz');
assert.equal(exported.ratings['SOC-01'].score,0);
assert.equal(exported.ratings['SOC-02'],null);
assert(!('stale' in exported.ratings['SOC-01']));
assert.equal(data.ideas['SOC-01'].ratings.dmarz,null);
assert.equal(h.scoreExport(data, {}, 'vishesh').ratings['SOC-02'].candidate_sha256,'a');
assert.deepEqual(h.parseDrafts(null),{});
assert.deepEqual(h.parseDrafts(JSON.stringify({schema:h.SCORE_STORAGE_KEY,rubric_version:h.RUBRIC_VERSION,ratings:draft})),draft);
assert.throws(()=>h.parseDrafts('{'));
assert.throws(()=>h.parseDrafts(JSON.stringify({schema:h.SCORE_STORAGE_KEY,rubric_version:h.RUBRIC_VERSION,ratings:{dmarz:{'SOC-01':{...rating,score:99}}}})));
const published=JSON.parse(readFileSync(new URL('../public/data/idea-scores.json',import.meta.url),'utf8'));
for(const idea of Object.values(published.ideas)) for(const r of Object.values(idea.ratings)) assert(h.validRating(r));
console.log('Idea-score tests passed: weights, NA/zero, invalid inputs, isolated drafts, stale content, export and published data.');
