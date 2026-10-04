# Latest diagnostic: D6 confirms direct API HTTP429

**HOLD.** [D6 post-mortem](reviews/D6-post.md) · [exact audit](reviews/D6-audit.json) · [native run](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-180640-faf466).

One request was attempted and rejected with HTTP429; the circuit stopped with no retry. The second reviewer format stayed unstarted. No model response, schema result or behavioral comparison was obtained. Actual charges are unknown; USD0.048640 newly reserved, USD4.917472 cumulative of8, USD3.082528 unreserved. Worker stopped and allocation released.

# Latest attempt: D5 acquisition failed; D3 remains the latest behavioral evidence

[Full D5 post-mortem](reviews/D5-post.md) · [Trace audit](reviews/D5-failure-audit.json) · [Reviewed replay](reviews/D5-failure-replay.html) · [Native run](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-164820-b6f158).

D5 assigned24 workflows but obtained0 usable responses in48 failed transport attempts. The exact provider status was not retained. This is an inconclusive acquisition failure, not evidence of poor procurement choices or an architecture effect. All48 usage records are missing: the actual bill is unknown. USD1.690512 was reserved; cumulative reservations are USD4.868832 of8, leaving3.131168. Worker stopped; no automatic retry.

## Previous behavioral result: D3

[D3 results and practical next changes](RESULTS-D3.md). All 90 required checks were populated, but only 76 were correct. All three workflows made 4/6 acceptable decisions; the added consistency instruction changed none. Chairs respected the model's blockers, but invented blockers caused two avoidable deferrals per arm. No execution failures or missing usage; 30 calls, $0.205670.

[Swarm Lab run and replay artifacts](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-054904-3252ed). D4 did not meet its launch gate and remains unrun. S1 remains unqualified. [D2](RESULTS-D2.md) and [Q4/D1](RESULTS-Q4-D1.md) are preserved separately.



[Offline D6 acquisition repairs and bounded next proposal](ITERATION-06-PREP.md): safe status telemetry, durable journal and first-failure stop implemented;72tests pass. Two requests maximum USD0.097280 proposed, not approved/admitted/launched.
