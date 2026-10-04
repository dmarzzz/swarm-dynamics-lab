import { IdeaScoresProvider } from './components/IdeaScores';
import { lazy, Suspense, useEffect, type ComponentType } from 'react';
import './styles.css';
import './components/components.css';
import { useDataset } from './data/load';
import { useRoute } from './lib/router';
import { useTheme } from './lib/theme';
import { Overview } from './views/Overview';
import { Library } from './views/Library';
import { Agents } from './views/Agents';
import { Topics } from './views/Topics';
import { Timeline } from './views/Timeline';
import { ResearchPath } from './views/ResearchPath';
import { Threads } from './views/Threads';
import { ago, parseT } from './lib/format';
import { REPO_NAME, REPO_URL } from './lib/repo';
import { Mark } from './components/Mark';
const Contributions = lazy(() => import('./views/Contributions').then(m => ({ default: m.Contributions })));
const Questions = lazy(() => import('./views/Questions').then(m => ({ default: m.Questions })));

// Lane G's graph view mounts here once dashboard/src/graph/ exists. Optional at build time.
const graphMods = import.meta.glob<{ default?: ComponentType<{ className?: string }>; GraphView?: ComponentType<{ className?: string }> }>('./graph/index.tsx');
const GraphView = Object.values(graphMods)[0]
  ? lazy(() => Object.values(graphMods)[0]().then((m) => ({ default: (m.default ?? m.GraphView)! })))
  : null;

const NAV = [
  { path: '/', label: 'Overview' },
  { path: '/library', label: 'Library' },
  { path: '/topics', label: 'Topics' },
  { path: '/questions', label: 'Questions' },
  { path: '/contributions', label: 'Contributions' },
  { path: '/agents', label: 'Agents' },
  { path: '/timeline', label: 'Timeline' },
  { path: '/method', label: 'Research path' },
  ...(GraphView ? [{ path: '/graph', label: 'Graph' }] : []),
  { path: '/threads', label: 'X threads' },
];

export default function App() {
  const route = useRoute();
  const state = useDataset();
  useTheme();
  useEffect(() => { window.scrollTo({ top: 0 }); }, [route.path]);
  useEffect(() => {
    const cur = NAV.find((n) => n.path === route.path);
    document.title = cur && cur.path !== '/' ? `${cur.label} | Swarm Lab` : 'Swarm Lab, a research observatory';
  }, [route.path]);

  const gen = state.status === 'ready' ? parseT(state.data.summary.generated_at) : null;

  return (
    <IdeaScoresProvider><div className="shell">
      <a className="skip" href="#main">Skip to content</a>
      <header className="masthead">
        <div className="wrap">
          <a className="brand" href="#/" aria-label="Swarm Lab overview">
            <Mark className="brand-mark" />
            <span className="brand-name">Swarm Lab</span>
            <span className="brand-sub">research observatory</span>
          </a>
          <nav className="nav" aria-label="Views">
            {NAV.map((n) => (
              <a key={n.path} href={`#${n.path}`} aria-current={route.path === n.path ? 'page' : undefined}>{n.label}</a>
            ))}
          </nav>
          <div className="mast-right">
            {gen && (
              <span className="live" title={`Data exported ${new Date(gen).toLocaleString()}`}>
                <span className="live-dot" aria-hidden="true" />
                <span className="live-label">Updated {ago(gen)}</span>
              </span>
            )}
            <a className="icon-btn live-link" href="https://swarm-live.pages.dev/" title="swarm live">live</a>
          </div>
        </div>
      </header>

      <main id="main">
        {state.status === 'loading' && <Loading />}
        {state.status === 'error' && <LoadError error={state.error} />}
        {state.status === 'ready' && (
          <div key={route.path} className="view">
            {route.path === '/' && <Overview data={state.data} />}
            {route.path === '/library' && <Library data={state.data} params={route.params} />}
            {route.path === '/topics' && <Topics data={state.data} params={route.params} />}
            {route.path === '/questions' && <Suspense fallback={<Loading />}><Questions params={route.params} navigation={state.data.navigation} /></Suspense>}
            {route.path === '/contributions' && <Suspense fallback={<Loading />}><Contributions params={route.params} /></Suspense>}
            {route.path === '/agents' && <Agents data={state.data} />}
            {route.path === '/timeline' && <Timeline data={state.data} />}
            {route.path === '/method' && <ResearchPath data={state.data} />}
            {route.path === '/threads' && <Threads data={state.data} params={route.params} />}
            {route.path === '/graph' && GraphView && (
              <Suspense fallback={<Loading />}><div className="wrap graph-page"><GraphView /></div></Suspense>
            )}
            {!NAV.some((n) => n.path === route.path) && (
              <div className="wrap page-head">
                <p className="eyebrow"><span className="tick" />Not found</p>
                <h1 className="display">Nothing lives at <span className="mono">{route.path}</span>.</h1>
                <p className="lede"><a href="#/">Back to the overview</a>.</p>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <div className="wrap">
          <span>Built from <a href={REPO_URL}>{REPO_NAME}</a>. Every number on this page is computed from files in the repository.</span>
          {state.status === 'ready' && (
            <span className="mono">
              <a href={`${REPO_URL}/commit/${state.data.summary.head_sha}`}>{state.data.summary.head_sha.slice(0, 7)}</a>
            </span>
          )}
        </div>
      </footer>
    </div></IdeaScoresProvider>
  );
}

function Loading() {
  return (
    <div className="wrap page-head" aria-busy="true" aria-live="polite">
      <span className="sr-only">Loading research data</span>
      <div className="skel" style={{ width: 180, height: 12 }} />
      <div className="skel" style={{ width: 'min(760px, 90%)', height: 44, marginTop: 18 }} />
      <div className="skel" style={{ width: 'min(520px, 70%)', height: 44, marginTop: 10 }} />
      <div className="skel" style={{ width: '100%', height: 260, marginTop: 36 }} />
    </div>
  );
}

function LoadError({ error }: { error: string }) {
  return (
    <div className="wrap page-head">
      <p className="eyebrow"><span className="tick" />Data unavailable</p>
      <h1 className="display">The research export could not be read.</h1>
      <p className="lede">The dashboard reads <span className="mono">/data/*.json</span>, which CI writes on every push. The request failed with: <span className="mono">{error}</span>. Reload in a minute, or run <span className="mono">python3 dashboard/scripts/export.py</span> locally.</p>
    </div>
  );
}
