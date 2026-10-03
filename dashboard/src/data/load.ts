import { useEffect, useState } from 'react';
import type { Dataset } from './types';

const FILES = ['summary', 'library', 'timeline', 'agents', 'tasks', 'batches', 'surveys', 'hypotheses', 'experiments'] as const;
const OPTIONAL = new Set(['hypotheses', 'experiments', 'batches']);

let cache: Promise<Dataset> | null = null;

async function fetchJson(name: string) {
  const base = import.meta.env.BASE_URL || '/';
  const res = await fetch(`${base}data/${name}.json`, { cache: 'no-cache' });
  if (!res.ok) {
    if (OPTIONAL.has(name)) return [];
    throw new Error(`${name}.json returned ${res.status}`);
  }
  return res.json();
}

export function loadDataset(): Promise<Dataset> {
  if (!cache) {
    cache = Promise.all(FILES.map((f) => fetchJson(f))).then((parts) => {
      const out = Object.fromEntries(FILES.map((f, i) => [f, parts[i]])) as unknown as Dataset;
      out.library = out.library.map((e) => ({ ...e, topics: e.topics ?? [], links: e.links ?? [] }));
      return out;
    });
    cache.catch(() => { cache = null; });
  }
  return cache;
}

export type LoadState = { status: 'loading' } | { status: 'error'; error: string } | { status: 'ready'; data: Dataset };

export function useDataset(): LoadState {
  const [state, setState] = useState<LoadState>({ status: 'loading' });
  useEffect(() => {
    let alive = true;
    loadDataset()
      .then((data) => alive && setState({ status: 'ready', data }))
      .catch((e: unknown) => alive && setState({ status: 'error', error: String((e as Error)?.message ?? e) }));
    return () => { alive = false; };
  }, []);
  return state;
}
