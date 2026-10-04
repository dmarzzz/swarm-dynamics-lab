# Always-five setup guide

Human asked for one document that describes how the fleet of coding agents is arranged tonight so that five
experiments always have a run in progress, written so that another team can reproduce it, with none of the
private specifics of the setup.

Wrote `notes/always-five/README.md` from the human's description. It covers the goal and
what counts as a live experiment, why the count drops, the roles, the run queue and the meaning of "ready",
the rules that shorten the gap between runs, the rules that keep runs honest, the model rules for the
strongest tier, the failures seen with the fix for each, what the human sees, and a reproduction checklist.
No model calls, no runs, no claims, no edits to any study.

Conflict with AGENTS.md, by the human's instruction: the work was done on branch `lane/always-five-doc`,
committed locally and held without a sync timer until the reviewer had read the whole file. The reviewer
then supplied the detection methods and fixes that the first draft lacked, and gave the word to push.

Privacy search run on the document before the commit: host and server name fragments, local paths, the
at sign, remote-shell commands, currency amounts, and digit groups shaped like addresses or ports. The only
digits in the document are the date and tonight's settings.

Not checked by me: the durations, the duty-cycle estimate and the failure accounts. They were observed by
the monitor session during the night and passed to me in writing. The setup order in the reproduction
checklist is the document's suggestion.

Next: nothing. The privacy search is rerun on the file as it stands on the main branch after the push.
