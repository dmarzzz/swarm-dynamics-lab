import { useEffect } from 'react';

type Theme = 'dark';

/** Single dark theme to match swarm-live. Toggle kept as a no-op so call sites don't change. */
export function useTheme() {
  const theme: Theme = 'dark';
  useEffect(() => { document.documentElement.dataset.theme = theme; }, []);
  return { theme, toggle: () => {} };
}
