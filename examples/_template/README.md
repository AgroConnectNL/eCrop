# <Business case name>

*eCrop API v<version> — <one-sentence scope: which platform/actor does what>*

## 1. Use case and starting points

<Describe the actors involved (e.g. grower, supplier, contractor) and the systems they act
through (bms-grower, bms-contractor, etc.). State the precise use case in one or two bold
sentences, scoped as narrowly as possible.>

## 2. Operations used

### 2.1 Core operations for this use case

| Operation | Purpose | Why needed |
| --- | --- | --- |
| `GET ...` | | |

### 2.2 Recommended (not required)

<e.g. `GET /health`, for monitoring/orchestration — see the Loonwerkportaal guide for the
reasoning.>

### 2.3 Explicitly out of scope for this phase

| Domain | Operations | Why out of scope |
| --- | --- | --- |
| | | |

## 3. Example flow

<Narrative walkthrough of the calls in order. Keep small payloads inline as fenced code blocks;
for larger or reused ones, put them in `payloads/` next to this file and link to them, e.g.
[`payloads/get-plot-feature.response.json`](payloads/get-plot-feature.response.json).>

## 4. Still to be arranged

<Anything outside the OpenAPI spec itself that still needs deciding for this case: security,
identifier schemes, code lists, etc. See
[`docs/guides/implementatie-instructie-loonwerkportaal.md`](../../docs/guides/implementatie-instructie-loonwerkportaal.md)
for the level of detail expected here.>
