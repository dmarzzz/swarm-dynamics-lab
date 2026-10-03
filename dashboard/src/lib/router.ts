import { useEffect, useState, useCallback } from 'react';

export interface Route { path: string; params: URLSearchParams }

function read(): Route {
  const raw = window.location.hash.replace(/^#/, '') || '/';
  const [path, q = ''] = raw.split('?');
  return { path: path || '/', params: new URLSearchParams(q) };
}

export function useRoute(): Route {
  const [r, setR] = useState(read);
  useEffect(() => {
    const on = () => setR(read());
    window.addEventListener('hashchange', on);
    return () => window.removeEventListener('hashchange', on);
  }, []);
  return r;
}

export function href(path: string, params?: Record<string, string | null | undefined>) {
  const q = new URLSearchParams();
  if (params) for (const [k, v] of Object.entries(params)) if (v) q.set(k, v);
  const s = q.toString();
  return `#${path}${s ? `?${s}` : ''}`;
}

/** Replace query params on the current path without adding history entries. */
export function useParamSetter(path: string) {
  return useCallback((next: Record<string, string | null | undefined>) => {
    const cur = read();
    const q = new URLSearchParams(cur.params);
    for (const [k, v] of Object.entries(next)) { if (v) q.set(k, v); else q.delete(k); }
    const s = q.toString();
    const url = `#${path}${s ? `?${s}` : ''}`;
    window.history.replaceState(null, '', url);
    window.dispatchEvent(new HashChangeEvent('hashchange'));
  }, [path]);
}
