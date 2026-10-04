import * as Dialog from '@radix-ui/react-dialog';
import type { Entry } from '../data/types';
import { DEPTH_LABEL, KIND_ONE, kindColor, teamColor, teamOf, topicName } from '../data/meta';
import { clockET, parseT } from '../lib/format';
import { href } from '../lib/router';
import { repoFile } from '../lib/repo';

export function EntryDrawer({ entry, byId, onClose, onOpen }: {
  entry: Entry | null; byId: Map<string, Entry>; onClose: () => void; onOpen: (id: string) => void;
}) {
  const t = entry ? parseT(entry.added_at) : null;
  const links = entry ? entry.links.map((id) => byId.get(id)).filter(Boolean) as Entry[] : [];
  const backlinks = entry ? [...byId.values()].filter((e) => e.links.includes(entry.id)).slice(0, 12) : [];
  const folder = entry ? ({ paper: 'papers', blog: 'blogs', thread: 'threads', code: 'code', dataset: 'datasets', talk: 'talks' } as const)[entry.kind] : '';
  return (
    <Dialog.Root open={!!entry} onOpenChange={(o) => !o && onClose()}>
      <Dialog.Portal>
        <Dialog.Overlay className="drawer-overlay" />
        <Dialog.Content className="drawer" aria-describedby={undefined} tabIndex={-1}
          onOpenAutoFocus={(ev) => { ev.preventDefault(); (ev.currentTarget as HTMLElement | null)?.focus(); }}>
          {entry && (
            <>
              <div className="drawer-top">
                <span className="drawer-kind"><i className="sw round" style={{ background: kindColor(entry.kind) }} />{KIND_ONE[entry.kind]}{entry.year ? `, ${entry.year}` : ''}</span>
                <Dialog.Close className="icon-btn" aria-label="Close">
                  <svg width="14" height="14" viewBox="0 0 14 14" stroke="currentColor" strokeWidth="1.3"><path d="M2 2l10 10M12 2L2 12" /></svg>
                </Dialog.Close>
              </div>
              <Dialog.Title className="drawer-title">{entry.title}</Dialog.Title>
              {entry.authors && <p className="drawer-authors">{entry.authors}</p>}

              <dl className="drawer-meta">
                <div><dt>Relevance</dt><dd><Dots n={entry.relevance ?? 0} /> <span className="num">{entry.relevance ?? 'n/a'}</span> of 5</dd></div>
                <div><dt>Read depth</dt><dd>{DEPTH_LABEL[entry.read_depth ?? ''] ?? entry.read_depth ?? 'n/a'}</dd></div>
                <div><dt>Added by</dt><dd><i className="sw round" style={{ background: teamColor(teamOf(entry.added_by)) }} /> <span className="mono">{entry.added_by}</span></dd></div>
                <div><dt>Added</dt><dd>{t ? `${clockET(t)} ET, ${new Date(t).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}` : 'unknown'}</dd></div>
              </dl>

              <div className="drawer-topics">
                {entry.topics.map((tp) => <a key={tp} className="pill" href={href('/topics', { t: tp })}>{topicName(tp)}</a>)}
              </div>

              <h3 className="drawer-h">Summary</h3>
              <p className="drawer-summary">{entry.summary ? (entry.summary.length >= 279 ? `${entry.summary.replace(/\s+\S*$/, '')}...` : entry.summary) : 'No summary written yet.'}</p>

              <div className="drawer-actions">
                {entry.url && <a className="btn" href={entry.url} target="_blank" rel="noreferrer">Open source <span aria-hidden="true">↗</span></a>}
                <a className="btn ghost" href={repoFile(`1-library/${folder}/${entry.id}.md`)} target="_blank" rel="noreferrer">Full catalogue entry</a>
              </div>

              {links.length > 0 && (
                <>
                  <h3 className="drawer-h">Cites in the library <span className="muted num">{links.length}</span></h3>
                  <ul className="drawer-links">
                    {links.map((l) => <li key={l.id}><button onClick={() => onOpen(l.id)}><i className="sw round" style={{ background: kindColor(l.kind) }} />{l.title}</button></li>)}
                  </ul>
                </>
              )}
              {backlinks.length > 0 && (
                <>
                  <h3 className="drawer-h">Cited by <span className="muted num">{backlinks.length}</span></h3>
                  <ul className="drawer-links">
                    {backlinks.map((l) => <li key={l.id}><button onClick={() => onOpen(l.id)}><i className="sw round" style={{ background: kindColor(l.kind) }} />{l.title}</button></li>)}
                  </ul>
                </>
              )}
              <p className="drawer-id mono faint">{entry.id}</p>
            </>
          )}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

export function Dots({ n, of = 5 }: { n: number; of?: number }) {
  return (
    <span className="dots" aria-hidden="true">
      {Array.from({ length: of }, (_, i) => <i key={i} className={i < n ? 'on' : ''} />)}
    </span>
  );
}
