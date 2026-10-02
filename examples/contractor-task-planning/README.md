# Contractor planning: retrieving a grower's plots and their geometry, and registering the performed tasks

*eCrop API v1.1.0 — a contractor's planning system retrieves a grower's plots and plot geometry to
plan field work (phase 1, §3.1-3.3), and afterwards registers the tasks it actually performed on
those plots for the grower (phase 2, §3.4-3.7).*

## 1. Use case and starting points

| Actor / system | Role |
| --- | --- |
| Contractor employee | Plans field work for a grower on behalf of a contractor, using the contractor's own planning software |
| Contractor Planning System (CPS) | The contractor's own system; acts as the eCrop API client, retrieving a grower's plots and their geometry to support planning, and registering (and correcting) the tasks performed |
| eCrop server (crop registration platform) | Provides read access to a grower's plots and plot geometry to contractors the grower has granted access to, and accepts the tasks those contractors register on the grower's plots |
| Grower | Has already registered their plots (including geometry) on the platform, and granted this contractor access — no active role in this flow, it's a precondition. Receives the tasks the contractor registers on their plots |

**A contractor employee uses their Contractor Planning System (CPS) to retrieve the plots — and,
for each plot, its geometry — of a grower who has already registered their plots (including
geometry) on the platform and granted this contractor access, so the employee can plan field work
using both a plot's business attributes and its shape/location. After the work has been done, the
employee's CPS registers the task(s) performed on that plot for the grower — and, if needed,
corrects or deletes them later.**

## 2. Operations used

### 2.1 Core operations for this use case

**Phase 1 — planning (read):**

| Operation | Purpose | Why needed |
| --- | --- | --- |
| `GET /contractors/{contractorSchemeId}/{contractorId}/growers` | Discover which growers have granted this contractor access | Discovery start point — the CPS doesn't need to know a grower's id in advance |
| `GET /contractors/{...}/{..}/growers/{growerSchemeId}/{growerId}/plots` | List a grower's plots (business attributes) — each item already includes a `links` entry pointing at its geometry Feature | **Action 1.** The response carries everything needed for Action 2, so no separate geo-discovery step is needed per plot (see the design note below) |
| `GET /contractors/{...}/{..}/growers/{...}/{..}/plots/{plotSchemeId}/{plotId}` | Retrieve one specific plot, e.g. once the CPS already knows its id from an earlier sync | Same shape (and `links`) as a list item, just scoped to one plot |
| `GET {the plot's `links[rel=".../rel/plot-features"]`.href}` — i.e. `GET /collections/plots/items/{featureId}` on the plot-features server | Retrieve that plot's geometry (boundary, entryPoint, abLine) as a Feature | **Action 2.** The CPS follows the link it was just given — it never computes or guesses a `featureId` itself |

**Phase 2 — registering the performed tasks (write)**, all scoped to a plot of a grower the contractor
has been granted access to
(`/contractors/{...}/{..}/growers/{...}/{..}/plots/{plotSchemeId}/{plotId}/tasks`):

| Operation | Purpose | Why needed |
| --- | --- | --- |
| `POST .../plots/{plotSchemeId}/{plotId}/tasks` | Register a (non crop-specific) task, with its operations, performed on the plot | **Action 3.** The primary way to report work done. Re-posting a task with the same external id (`thirdPartyIds`) updates the previously posted task instead of creating a duplicate |
| `PUT .../tasks/{taskSchemeId}/{taskId}` | Update a previously registered task by replacing it as a whole; covers all updates of existing tasks | Preferred over re-posting when the CPS holds the complete, corrected task |
| `PATCH .../tasks/{taskSchemeId}/{taskId}` *(optional)* | Partially update a previously registered task using a JSON Patch document (RFC 6902, media type `application/json-patch+json`) | Optional, because PUT already covers all updates of existing tasks. Efficient for small corrections, e.g. changing the treated area of an operation from 25000 to 24500 m2 |
| `DELETE .../tasks/{taskSchemeId}/{taskId}` | Delete a previously registered task | For tasks registered by mistake or cancelled afterwards |

**Design note on "2 actions":** as of this spec version, `plot_200`/`plots_200` responses embed a
`links` array with a custom `rel="https://ecrop.agroconnect.nl/rel/plot-features"` entry pointing
straight at that plot's Feature — and the Feature links back the same way
(`rel="https://ecrop.agroconnect.nl/rel/plot"`), plus carries the originating `plotId` in
`properties`. That's what makes this a clean 2-call flow per plot: get the plot, follow its link.
See §2.2 for why the fuller OGC API Features discovery chain isn't part of this core flow.

### 2.2 Recommended (not required)

- `GET /health` — for the CPS's own monitoring.
- `GET /contractors/{...}/{..}/growers/{growerSchemeId}/{growerId}` — the grower's own details
  (e.g. display name), useful for the CPS's UI.
- `GET /`, `GET /conformance`, `GET /collections`, `GET /collections/plots` — the formal OGC API
  Features discovery chain (landing page → conformance → collections → collection metadata).
  Because the plot's own `links` array already hands the CPS a direct, followable URL to each
  plot's Feature, this case's core flow doesn't need this chain. A fully OGC-API-Features-
  conformant client would still do this once, at integration setup, to confirm which
  profiles/CRSs the server supports.

### 2.3 Explicitly out of scope for this phase

| Domain | Operations | Why out of scope |
| --- | --- | --- |
| Registering plots or crops | `POST`/`PUT`/`DELETE .../plots`, `.../crops` | The grower has already registered these; a contractor never registers a grower's own master data |
| Inbound deliveries | All `.../inbound-deliveries` operations | Different process domain |
| Direct (non-contractor) plot access | `GET /growers/{...}/{..}/plots(/{id})` | That's the grower's own access route (e.g. via their own FMS) — this case is specifically the contractor-scoped route |
| Supplier-scoped access | `/suppliers/*` | No supplier role in this case |
| Direct (non-contractor) task registration | `POST`/`PUT`/`PATCH`/`DELETE /growers/{...}/{..}/plots/{...}/{..}/tasks(...)` | That's the grower's own route (e.g. via their own FMS); a contractor uses the contractor-scoped task operations above |
| Tasks at other levels | `.../production-locations/.../tasks`, `.../growers/{...}/{..}/tasks`, crop-level tasks | The contractor-scoped task operations exist at plot level only |

## 3. Example flow

```mermaid
sequenceDiagram
    actor Employee as Contractor employee
    participant CPS as Contractor Planning System
    participant eCrop as eCrop server<br/>(crop registration platform)

    Note over CPS,eCrop: Grower has already registered plots (incl. geometry)<br/>and granted this contractor access

    Employee->>CPS: Open planning for a grower
    CPS->>eCrop: GET /contractors/{contractorSchemeId}/{contractorId}/growers
    eCrop-->>CPS: 200 OK (growers granted to this contractor)

    CPS->>eCrop: GET .../growers/{growerSchemeId}/{growerId}/plots
    activate eCrop
    eCrop-->>CPS: 200 OK (plots, each incl. a link to its geometry Feature)
    deactivate eCrop

    loop For each plot the employee wants to plan around
        Note over CPS,eCrop: Action 1 already done above (or via a single-plot GET)
        CPS->>eCrop: Action 2 - GET the plot's own links[rel=".../rel/plot-features"].href
        eCrop-->>CPS: 200 OK (Feature: boundary, entryPoint, abLine)
        CPS-->>CPS: Combine plot attributes + geometry for planning (e.g. on a map)
    end

    Employee->>CPS: Plan field work using the combined plot + geometry data

    Note over Employee,eCrop: Field work is executed ...

    Employee->>CPS: Confirm the work performed on a plot
    CPS->>eCrop: Action 3 - POST /contractors/{...}/growers/{...}/plots/{...}/tasks
    eCrop-->>CPS: 202 Accepted (Task, incl. server-assigned id)

    opt Correction needed afterwards
        Employee->>CPS: Correct the registered task
        alt Optional: small correction
            CPS->>eCrop: PATCH .../tasks/{taskSchemeId}/{taskId} (JSON Patch, optional)
        else Update (replace the whole task)
            CPS->>eCrop: PUT .../tasks/{taskSchemeId}/{taskId} (full TaskDetails)
        end
        eCrop-->>CPS: 202 Accepted (Task)
    end

    opt Task registered by mistake
        CPS->>eCrop: DELETE .../tasks/{taskSchemeId}/{taskId}
        eCrop-->>CPS: 204 No Content
    end
```

### 3.1 Discover authorized growers

```http
GET /contractors/nl.loonwerkportaal.codelist.guid/5d4e3f2a-1b0c-9d8e-7f6a-5b4c3d2e1f0a/growers
Major-Version: v1
User-Agent: contractor-planning-system/1.0
```

```json
[
  {
    "id": {
      "content": "e3c8a1b2-4f6e-4a2d-8e3b-9c1d2e3f4a5b",
      "schemeId": "nl.loonwerkportaal.codelist.guid"
    },
    "thirdPartyIds": [
      { "content": "09123559", "schemeId": "nl.kvk.codelist.kvknummer" }
    ],
    "name": "Kwekerij De Lier"
  }
]
```

### 3.2 Action 1 — retrieve a plot

```http
GET /contractors/nl.loonwerkportaal.codelist.guid/5d4e3f2a-1b0c-9d8e-7f6a-5b4c3d2e1f0a/growers/nl.loonwerkportaal.codelist.guid/e3c8a1b2-4f6e-4a2d-8e3b-9c1d2e3f4a5b/plots/nl.loonwerkportaal.codelist.guid/e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b
```

```json
{
  "id": {
    "content": "e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b",
    "schemeId": "nl.loonwerkportaal.codelist.guid"
  },
  "thirdPartyIds": [
    { "content": "APD03-AD-4094", "schemeId": "nl.rvo.codelist.perceelsnummer" }
  ],
  "name": "Tuin1, perceel6",
  "startDate": "2024-01-12",
  "endDate": "2024-12-14",
  "type": "CROPFIELD",
  "area": {
    "content": 6000,
    "unitCode": { "content": "MTK", "listId": "nl.agroconnect.codelist.cl020" }
  },
  "regularOrOrganic": { "content": "REGULAR", "listId": "nl.agroconnect.codelist.cl015" },
  "localSoilType": { "content": "CLAY", "listId": "nl.agroconnect.codelist.cl405" },
  "regulatorySoilType": { "content": "CLAY", "listId": "nl.agroconnect.codelist.cl405" },
  "links": [
    {
      "rel": "https://ecrop.agroconnect.nl/rel/plot-features",
      "href": "https://standard-api.agroconnect.nl/plot-features/v1/collections/plots/items/384912567",
      "type": "application/geo+json",
      "title": "Geo-information (boundary, entryPoint, abLine) as OGC feature"
    }
  ]
}
```

### 3.3 Action 2 — follow the link to the plot's geometry

Note this is on the separate plot-geometry server (`.../plot-features/v1`, not `.../ecrop/v1`) —
the `href` above already points there, so the CPS just follows it as given:

```http
GET https://standard-api.agroconnect.nl/plot-features/v1/collections/plots/items/384912567
```

```json
{
  "type": "Feature",
  "id": 384912567,
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [5.7519, 51.9485],
        [5.7811, 51.9485],
        [5.7811, 51.9665],
        [5.7519, 51.9665],
        [5.7519, 51.9485]
      ]
    ]
  },
  "properties": {
    "plotId": {
      "content": "e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b",
      "schemeId": "nl.loonwerkportaal.codelist.guid"
    },
    "name": "Tuin1, perceel6",
    "area": {
      "content": 6000,
      "unitCode": { "content": "MTK", "listId": "nl.agroconnect.codelist.cl020" }
    },
    "entryPoint": { "type": "Point", "coordinates": [5.7527, 51.9487] },
    "abLine": {
      "type": "LineString",
      "coordinates": [
        [5.7548, 51.9494],
        [5.7782, 51.9655]
      ]
    }
  },
  "links": [
    {
      "rel": "self",
      "href": "https://standard-api.agroconnect.nl/plot-features/v1/collections/plots/items/384912567",
      "type": "application/geo+json"
    },
    {
      "rel": "https://ecrop.agroconnect.nl/rel/plot",
      "href": "https://standard-api.agroconnect.nl/ecrop/v1/growers/nl.loonwerkportaal.codelist.guid/e3c8a1b2-4f6e-4a2d-8e3b-9c1d2e3f4a5b/plots/nl.loonwerkportaal.codelist.guid/e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b",
      "type": "application/json"
    }
  ]
}
```

The CPS now has both the plot's attributes (from §3.2) and its shape/location (from this
response) to plan the field work.

### 3.4 Action 3 — register the task performed on the plot

Once the work is done, the CPS registers it as a task with one or more operations on the plot from
§3.2. The server assigns the task's `id`; the CPS's own identification travels in `thirdPartyIds`.

```http
POST /contractors/nl.loonwerkportaal.codelist.guid/5d4e3f2a-1b0c-9d8e-7f6a-5b4c3d2e1f0a/growers/nl.loonwerkportaal.codelist.guid/e3c8a1b2-4f6e-4a2d-8e3b-9c1d2e3f4a5b/plots/nl.loonwerkportaal.codelist.guid/e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b/tasks
Major-Version: v1
User-Agent: contractor-planning-system/1.0
Content-Type: application/json
```

```json
{
  "thirdPartyIds": [
    { "content": "27575", "schemeId": "nl.my-cps.codelist.registratienummer" },
    { "content": "WB-2025-0412", "schemeId": "nl.my-cps.codelist.werkbonnummer" }
  ],
  "name": "Spraying task",
  "startDateTime": "2025-03-12T15:51:00+01:00",
  "endDateTime": "2025-03-12T16:45:00+01:00",
  "status": "COMPLETED",
  "operations": [
    {
      "thirdPartyIds": [
        { "content": "27575-1", "schemeId": "nl.my-cps.codelist.operatienummer" }
      ],
      "name": "Spraying operation",
      "startDateTime": "2025-03-12T15:51:00+01:00",
      "endDateTime": "2025-03-12T16:45:00+01:00",
      "type": { "content": "SPRAYING", "listId": "nl.agroconnect.codelist.cl127" },
      "technique": { "content": "SPRAYING", "listId": "nl.agroconnect.codelist.cl302" },
      "status": "COMPLETED",
      "area": {
        "content": 25000,
        "unitCode": { "content": "MTK", "listId": "nl.agroconnect.codelist.cl020" }
      },
      "equipmentAssignments": [
        {
          "equipment": {
            "thirdPartyIds": [
              { "content": "1234", "schemeId": "nl.my-cps.codelist.materieelnummer" }
            ],
            "name": "John Deere 6120M",
            "type": "Tractor"
          },
          "startDateTime": "2025-03-12T15:51:00+01:00",
          "endDateTime": "2025-03-12T16:45:00+01:00"
        }
      ],
      "workerAssignments": [
        {
          "worker": {
            "id": { "content": "4821", "schemeId": "nl.my-cps.codelist.medewerkernummer" },
            "name": "Jan Jansen",
            "jobTitle": "Machine operator"
          },
          "startDateTime": "2025-03-12T15:51:00+01:00",
          "endDateTime": "2025-03-12T16:45:00+01:00"
        }
      ]
    }
  ]
}
```

The ids the CPS supplies itself (`thirdPartyIds` of the task and its operations, equipment and
workers) use `nl.my-cps.*` schemes, while the ids the Loonwerkportaal assigns (such as the `id`
of the task below) use `nl.loonwerkportaal.*`.

The server answers `202 Accepted` with the registered task, now including its `id`:

```json
{
  "id": {
    "content": "9b1f4c2e-6d3a-4f8b-a7e5-2c0d9e8f1a3b",
    "schemeId": "nl.loonwerkportaal.codelist.guid"
  },
  "thirdPartyIds": [
    { "content": "27575", "schemeId": "nl.my-cps.codelist.registratienummer" },
    { "content": "WB-2025-0412", "schemeId": "nl.my-cps.codelist.werkbonnummer" }
  ],
  "name": "Spraying task",
  "startDateTime": "2025-03-12T15:51:00+01:00",
  "endDateTime": "2025-03-12T16:45:00+01:00",
  "status": "COMPLETED",
  "operations": [ "..." ]
}
```

The CPS keeps this `id` to address the task in the calls below. The `inputAllocations`,
`equipmentAssignments` and `workerAssignments` properties of an operation (see the OpenAPI
specification) can be used to register the products, equipment and workers used.

### 3.5 Correct part of the task — PATCH (optional)

When only a small detail was wrong, the CPS sends a JSON Patch document (RFC 6902, per AASG rule
P012). Here the treated area of the first operation is changed from 25000 to 24500 m2. The `test`
operation guards against concurrent changes: if the current value isn't 25000, the whole patch is
rejected.

```http
PATCH /contractors/nl.loonwerkportaal.codelist.guid/5d4e3f2a-1b0c-9d8e-7f6a-5b4c3d2e1f0a/growers/nl.loonwerkportaal.codelist.guid/e3c8a1b2-4f6e-4a2d-8e3b-9c1d2e3f4a5b/plots/nl.loonwerkportaal.codelist.guid/e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b/tasks/nl.loonwerkportaal.codelist.guid/9b1f4c2e-6d3a-4f8b-a7e5-2c0d9e8f1a3b
Major-Version: v1
User-Agent: contractor-planning-system/1.0
Content-Type: application/json-patch+json
```

```json
[
  { "op": "test",    "path": "/operations/0/area/content", "value": 25000 },
  { "op": "replace", "path": "/operations/0/area/content", "value": 24500 }
]
```

The server answers `202 Accepted` with the updated task.

### 3.6 Replace the task — PUT

When the CPS holds the complete, corrected task, it can replace the registered task as a whole by
sending the full task details (same body as in §3.4, with the corrections applied) with `PUT` and
`Content-Type: application/json` to the same `.../tasks/{taskSchemeId}/{taskId}` URI as in §3.5. The
server answers `202 Accepted` with the updated task.

### 3.7 Delete the task — DELETE

If the task was registered by mistake or the work was cancelled:

```http
DELETE /contractors/nl.loonwerkportaal.codelist.guid/5d4e3f2a-1b0c-9d8e-7f6a-5b4c3d2e1f0a/growers/nl.loonwerkportaal.codelist.guid/e3c8a1b2-4f6e-4a2d-8e3b-9c1d2e3f4a5b/plots/nl.loonwerkportaal.codelist.guid/e7f8a9b0-1c2d-3e4f-5a6b-7c8d9e0f1a2b/tasks/nl.loonwerkportaal.codelist.guid/9b1f4c2e-6d3a-4f8b-a7e5-2c0d9e8f1a3b
Major-Version: v1
User-Agent: contractor-planning-system/1.0
```

The server answers `204 No Content`. A `404 Not Found` means the task doesn't exist (anymore).

## 4. Still to be arranged

### 4.1 Security

The spec defines no `securitySchemes` yet. Specific to this case: `GET /contractors/{...}/{..}/growers`
already reflects *which* growers have granted a contractor access, but not how that grant is
established, authenticated, or revoked — that mandate-management process still needs to be
designed, along with whether a CPS authenticates as the contractor organisation as a whole, or as
the individual employee using it.

### 4.2 CRS choice for the planning UI

`GET .../collections/plots/items/{featureId}` defaults to `profile=rfc7946` (plain GeoJSON,
always WGS84), as used in §3.3. Since this CPS is meant to show a field on a map for planning,
it's worth deciding whether `profile=jsonfg` with `crs=EPSG:28992` (RD New) is a better default —
agricultural GPS/steering systems in the Netherlands typically work in RD New rather than WGS84.

### 4.3 No change notifications — polling only

If the grower adds/removes a plot, edits its geometry, or revokes the contractor's access after
the CPS has already cached plot data, there is no push/webhook mechanism in the spec to notify the
CPS. The CPS must re-poll `GET .../growers` and `GET .../growers/{...}/{..}/plots` periodically to
stay current, and needs its own policy for how long cached (possibly now-stale, or no-longer-
authorized) plot/geometry data may be used for planning before the next poll.

### 4.4 Task registration: processing and ownership

The task operations answer `202 Accepted`: the server has accepted the task, but the spec doesn't
define a status resource or callback to learn whether (asynchronous) processing succeeded or the
grower's system later rejected it. It is also still to be decided how the grower can see, accept or
contest the tasks a contractor registered on their plots, and whether a contractor may change or
delete only its own tasks (the contractor-scoped URI suggests so, but the spec doesn't enforce it).

### 4.5 Identifier schemes and code lists

The example payloads above use these `schemeId`/`listId` values (also used in the
`contractor-task-planning` distribution of the OpenAPI specification):

- `nl.loonwerkportaal.codelist.guid` — primary ids assigned by the Loonwerkportaal (growers, plots, tasks, ...)
- `nl.my-cps.codelist.*` — ids assigned by the contractor's own planning system: `registratienummer`
  and `werkbonnummer` (task), `operatienummer` (operation), `materieelnummer` (equipment),
  `medewerkernummer` (worker)
- `nl.rvo.codelist.perceelsnummer` — the plot number (RVO)
- `nl.agroconnect.codelist.cl020` for units, `nl.agroconnect.codelist.cl015`/`cl405` for the
  organic/soil-type code lists

These need to be confirmed as definitive, published schemes/code lists before production use.
