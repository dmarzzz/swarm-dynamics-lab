# Pre-request credential-path correction

The first invocation failed locally with FileNotFoundError before reading any credential or launching any HTTP request: the brief's `/home/shad0w/.openclaw/ocplatform.json` does not exist. The actual config is `/home/shad0w/.openclaw/openclaw.json`; it has the same named `anthropic-proxy` provider and its configured base URL is the explicitly authorized loopback port18811. Change only that local config path. No endpoint/model/key value is changed, no alternative provider is used. Regenerate input source hashes and commit before qualification. Zero requests preceded this amendment.

Source-model correction is already present in PREREG.md: the reading-rule result was GPT-4o-mini via OpenRouter, not a 7B model. Final FINDING will use the title and concise lead suitable for section7, Freeze on Claude, in researchers/shadow/SUBMISSION.md.
