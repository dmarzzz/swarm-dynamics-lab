"""Build a portable Markdown audit with its complete portfolio appendix."""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parents[1]
BASE='https://github.com/dmarzzz/swarm-lab/blob/main/researchers/dmarz/notes/completion-audit-2026-10-04/'
parts=[]
for name in ['README.md','PREVALENCE.md','PORTFOLIO.md']:
    text=(HERE/name).read_text()
    def target(match):
        label,path=match.group(1),match.group(2)
        if not path.startswith(('http://','https://','#','/')):path=BASE+path.removeprefix('./')
        return f'[{label}]({path})'
    parts.append(re.sub(r'\[([^\]]+)\]\(([^)]+)\)',target,text))
out=HERE/'src/out';out.mkdir(exist_ok=True)
(out/'completion-audit.md').write_text('\n\n---\n\n'.join(parts))
print(out/'completion-audit.md')
