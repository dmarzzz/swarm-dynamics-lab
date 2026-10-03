import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';

const source = readFileSync(new URL('../src/data/navigation.ts', import.meta.url), 'utf8');
const { outputText } = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022 } });
const { matchesResearch, matchesHypothesis } = await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
const nav = {
  focus_areas: [{ id: 'immune-response', questions: ['SEC-07', 'SOC-23'] }],
  projects: [{ id: 'memory', questions: ['SEC-07', 'SOC-21'] }],
};
const sec = { id: 'SEC-07', area: 'fork-merge-security' };
const soc = { id: 'SOC-23', area: 'llm-agent-swarms' };
assert(matchesResearch(sec, nav));
assert(matchesResearch(sec, nav, '', 'immune-response', 'memory'));
assert(!matchesResearch(soc, nav, '', 'immune-response', 'memory'));
assert(!matchesResearch(sec, nav, 'llm-agent-swarms', 'immune-response'));
assert(matchesResearch(soc, nav, 'llm-agent-swarms', 'immune-response'));
assert(!matchesResearch(sec, nav, '', 'unknown'));
assert(!matchesResearch(sec, nav, '', '', 'unknown'));
const h = { topics: ['llm-agent-swarms'], focus_areas: ['immune-response'], projects: ['memory'], status: 'proposed' };
assert(matchesHypothesis(h, 'llm-agent-swarms', 'immune-response', 'memory'));
assert(!matchesHypothesis(h, 'fork-merge-security'));
assert(matchesHypothesis({ topics: [], focus_areas: [], projects: [] }));
assert(!matchesHypothesis({ topics: [], focus_areas: [], projects: [] }, '', 'immune-response'));
assert.equal(h.status, 'proposed');
console.log('Research navigation: intersections, unknown filters and explicit hypothesis tags passed.');
