"""AskSwarm: reusable, coverage-aware lexical swarm diagnostics."""
from .adapters import Event, git_log, task_events, wiki, swarmtraces, table, parse_time
from .core import analyze, gini, normalize, Clusterer, VERSION

__version__ = VERSION
__all__ = ["Event", "git_log", "task_events", "wiki", "swarmtraces", "table", "parse_time", "analyze", "gini", "normalize", "Clusterer"]
