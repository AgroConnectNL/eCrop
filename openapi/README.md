# openapi

- [`ecrop.yaml`](ecrop.yaml) — the AgroConnect eCrop OpenAPI 3.0 specification, source of truth for the standard.

The eCrop OpenAPI spec can also be viewed online on SwaggerHub: [app.swaggerhub.com/apis-docs/vanraaijadvies/eCropAPI/1.1.0](https://app.swaggerhub.com/apis-docs/vanraaijadvies/eCropAPI/1.1.0?view=uiDocs)

## Business-case distributions

`ecrop.yaml` serves several business cases (see [`usecases/`](../usecases/)). Every operation carries an
`x-usecases` list (`all` = in every distribution, `unassigned` = in no distribution yet), and
[`redocly.yaml`](../redocly.yaml) has one `apis:` entry per business case. A distribution contains only the
operations of its business case, and only the request bodies, responses, parameters, schemas and examples
those operations need.

Build them into `dist/ecrop-<name>.yaml` (requires Node.js and Python with PyYAML):

```bash
python scripts/build-distribution.py                          # all business cases
python scripts/build-distribution.py contractor-task-planning  # one business case
```

Examples that must differ per business case (e.g. identifier schemes) are overridden in
[`usecases/<name>/examples.yaml`](../usecases/): whole entries of `components/examples`, plus the `example` of
named `components/schemas` and `components/parameters`.

The build also checks that the plot/feature examples still agree after the overrides are applied
(`scripts/check_consistency.py`): the `plot-features` link of a plot queries that plot's own id, the
`plotSchemeId`/`plotId` parameter examples match a plot that the Feature examples refer to, and the `plot`
link of a Feature ends with `/plots/{schemeId}/{id}` of its plot. A mismatch fails the build.

### Where the distributions are published

[`.github/workflows/publish.yml`](../.github/workflows/publish.yml) builds and lints all distributions:

- on every pull request that touches the specification, a use case or the scripts (build and lint only);
- on every push to `main`: published on GitHub Pages at <https://agroconnectnl.github.io/eCrop/>, where the
  documentation page has a selector for the complete specification and each business case, and the files are
  available at `https://agroconnectnl.github.io/eCrop/openapi/ecrop.yaml` and
  `https://agroconnectnl.github.io/eCrop/openapi/ecrop-<name>.yaml`;
- on every tag `v*` (e.g. `v1.1.0`): attached, together with `ecrop.yaml`, to the GitHub release of that tag,
  so implementers can pin a fixed version.

The generated files are not committed (`dist/` and `site/` are git-ignored).
