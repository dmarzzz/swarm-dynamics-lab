# Hackathon brief

Agents use this file to judge what is relevant. Filled 2026-10-04 by shadow/sol-submit (task
`admin-hackathon-brief`) from the event site swarmchasing.com (pages `/` and `/logistics/`, fetched
2026-10-03) as summarised in shadow's research brief. Anything the site does not state is marked "not
published" rather than guessed.

## Event

- Name: AI Village x Grove Research: AI Swarm Dynamics Hackathon.
- Dates and timezone: Saturday 3 and Sunday 4 October 2026, US Pacific time. Kickoff Saturday 11:00 PT
  (livestreamed; link in the event Slack).
- Location or online: 222 Dore St, San Francisco (SoMa), or online. Free to attend.
- Theme and prompt, verbatim: "Building the tools we wished we had for the Hugging Face incident." The site
  suggests (not required) these project types: swarm discovery in the wild; understanding tools
  (summarization, trajectory visualization); "pre-written questions you always want to ask about a
  multi-agent group"; agenthotline.ai-style whistleblowing; tracing how information spreads within a group;
  forensics beyond transcripts; aggregator datasets for meta-science of swarm incidents. "Your project might
  not even involve direct transcript analysis."
- Hosts: AI Village (theaidigest.org/village) and Grove Research (groveresearch.com). Organiser contact
  listed on the site: george@sage-future.org. Event Slack: swarmchasing (channels #general, #online,
  #find-teams, #announcements).

## Judging

- Criteria and weights: no published rubric. A panel of about 3 to 5 Grove Research and AI Village staff
  "and experts in the field". Online and in-person entries are judged identically. Decisions about one week
  after the event.
- Prizes: USD 3,000 across the top five (1,200 / 800 / 500 / 250 / 250). In-person teams: first USD 200 of
  compute reimbursed.
- Deliverable format (demo, paper, repo, video): one submission per team through the submission form (URL
  posted in the event Slack, not on the static site). The submission contains (a) a short write-up or video
  explaining the project, (b) a link to the GitHub repository with the code, (c) optionally, a write-up of
  real results found using the tool, (d) names and emails of all teammates. In-person demos Sunday 18:00 to
  19:00 PT, about 2 minutes per team, run from one shared machine, so everything must be pushed to GitHub
  beforehand. Team draft of the packet: `5-experiments/studies/shadow/submission/`.
- Submission deadline: Sunday 4 October 2026, 17:00 PT (00:00 UTC 5 October), for everyone including
  online teams.

## Constraints

- Allowed prior work and code: the site sets no restriction on prior work or reuse of existing code. Our
  own convention: everything built for the event lives in this repository from 2026-10-03 onward, and reused
  outside code is catalogued in `1-library/code/` with its licence.
- Compute available to the team: each researcher's own API accounts (Anthropic, OpenAI, OpenRouter) under
  the per-researcher budget rules in AGENTS.md; dmarz's approved cloud fleet (registered in the private
  `swarm-labs-agentops` repository, claimed per experiment); shadow's workstation for offline analysis.
  The organisers provide no compute beyond the in-person USD 200 reimbursement.
- Required tools, APIs or sponsors: none required. The organisers point at these datasets (optional): AI
  Village Hugging Face dataset `aidigestorg/ai-village` (gated, manual approval), the collusion.wiki dump,
  Transluce urlquery agent-activity catalogue, SwarmTraces, and Moltbook.

## Team

- dmarz
- vishesh
- shadow
