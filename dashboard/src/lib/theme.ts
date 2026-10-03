import { useEffect, useState } from 'react';

type Theme = 'light' | 'dark';
const KEY = 'swarm-lab-theme';

function initial(): Theme {
  const saved = localStorage.getItem(KEY) as Theme | null;
  if (saved === 'light' || saved === 'dark') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(initial);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);
  const toggle = () => setTheme((t) => {
    const n = t === 'dark' ? 'light' : 'dark';
    localStorage.setItem(KEY, n);
    return n;
  });
  return { theme, toggle };
}
